"""CPU replay of glsl/engine.comp (and glsl/state_init.comp), in float32.

Not a second reference: it follows the SHADER's data layout and control flow
(flat state arrays R / Path / Score / Counters, round robin over trails, stuck
trails, history read back from Path, candidate ordering of the reduction,
DDA drawing that skips repeated pixels) so that the GLSL logic can be checked
against python/reference.py without TouchDesigner:

    python python/engine_emulator.py            # compares on the test images

The result of the workgroup reduction does not depend on how candidates are
split between threads (it is the best candidate for a total order), so a
sequential loop gives the same choice as the GPU.
"""

import math
import sys

import numpy as np

import reference as ref

F = np.float32
NONE = 0xFFFFFFFF


def wang(x):
    return int(ref.wang_hash(np.uint32(x & 0xFFFFFFFF)))


def tie_hash(seed, iteration, c):
    return wang(wang(seed ^ wang(iteration)) ^ c)


class EngineEmulator:
    def __init__(self, lum, alpha, pegs_uv, *, line_count, trails=1, line_opacity=0.1,
                 history_length=20, min_peg_dist=0.2, invert=False, seed=0):
        self.H, self.W = lum.shape
        S = self.W * self.H
        # state_init.comp (premultiplied color as in TouchDesigner)
        lp = (lum * alpha).astype(F)
        self.R = np.clip(F(1) - lp if invert else F(1) - alpha + lp, 0, 1).astype(F).ravel()
        self.Path = np.full(S, -1, np.int64)
        self.Score = np.zeros(S, F)
        self.Counters = np.zeros(S, np.int64)
        self.uv = np.asarray(pegs_uv, F)
        self.px = self.uv * np.array([self.W, self.H], F)
        self.L, self.T = int(line_count), max(1, int(trails))
        self.M = (self.L + self.T - 1) // self.T + 1
        self.a = F(line_opacity)
        self.Hh = min(max(int(history_length), 0), 256)
        self.min_dist = F(min_peg_dist)
        self.seed = int(seed) & 0xFFFFFFFF
        assert self.T * self.M <= S and 2 + 2 * self.T <= S

    # ---- helpers mirroring the shader -----------------------------------

    def sample(self, x, y):
        fx, fy = x - F(0.5), y - F(0.5)
        x0, y0 = np.floor(fx), np.floor(fy)
        tx, ty = (fx - x0).astype(F), (fy - y0).astype(F)
        x0, y0 = x0.astype(np.int64), y0.astype(np.int64)

        def texel(xi, yi):
            inside = (xi >= 0) & (yi >= 0) & (xi < self.W) & (yi < self.H)
            v = np.ones(xi.shape, F)
            v[inside] = self.R[yi[inside] * self.W + xi[inside]]
            return v
        one = F(1)
        return ((one - tx) * (one - ty) * texel(x0, y0) + tx * (one - ty) * texel(x0 + 1, y0)
                + (one - tx) * ty * texel(x0, y0 + 1) + tx * ty * texel(x0 + 1, y0 + 1)).astype(F)

    def seg_score(self, A, B):
        n = max(1, int(math.ceil(float(F(np.hypot(*(B - A).astype(F)))) - ref.EPS)))
        k = np.arange(1, n + 1, dtype=F)
        t = (k / F(n + 1)).astype(F)
        p = A[None, :] + (B - A)[None, :] * t[:, None]
        v = (F(0.5) - (self.sample(p[:, 0].astype(F), p[:, 1].astype(F)) + self.a)).astype(F)
        s = F(0)
        for x in v:                       # sequential float32 sum, like the shader loop
            s = F(s + x)
        return F(s / F(n))

    def too_close(self, i, j):
        return float(np.hypot(*(self.uv[i] - self.uv[j]))) < float(self.min_dist)

    def draw(self, a, b):
        p0 = self.px[a] - F(0.5)
        d = self.px[b] - F(0.5) - p0
        n = int(math.ceil(float(max(abs(d[0]), abs(d[1]))) - ref.EPS)) + 1
        prev = None
        for k in range(n):
            t = F(k) / F(n - 1) if n > 1 else F(0)
            q = tuple(np.floor((p0 + d * t).astype(F) + F(0.5 + ref.EPS)).astype(np.int64))
            if q == prev:
                continue
            prev = q
            if 0 <= q[0] < self.W and 0 <= q[1] < self.H:
                i = q[1] * self.W + q[0]
                self.R[i] = min(F(1), F(self.R[i] + self.a))

    @staticmethod
    def better(c1, c2):
        (s1, h1, i1), (s2, h2, i2) = c1, c2
        q1, q2 = math.floor(float(s1) * 65536.0 + 0.5), math.floor(float(s2) * 65536.0 + 0.5)
        if q1 != q2:
            return q1 > q2
        if h1 != h2:
            return h1 < h2
        return i1 < i2

    # ---- one pass of K iterations (engine.comp main) ---------------------

    def run_pass(self, K):
        L, T, M, N = self.L, self.T, self.M, len(self.uv)
        C, P = self.Counters, self.Path
        for _ in range(K):
            seg = int(C[0])
            trail = None
            if seg < L and N >= 2:
                for r in range(T):
                    t = (seg + r) % T
                    if C[2 + T + t] == 0:
                        trail = t
                        break
            if trail is None:
                break
            t = trail
            length = int(C[2 + t])
            if length + (2 if length == 0 else 1) > M:
                C[2 + T + t] = 1
                continue
            cur = int(P[t * M + length - 1]) if length > 0 else -1
            hist = [int(P[t * M + length - 1 - h]) for h in range(min(self.Hh, length))]
            iteration = int(C[1])

            best = (F(-1.0e4), NONE, NONE)
            if cur < 0:
                step = 1 + N // 100
                m = (N + step - 1) // step
                for p in range(m * m):
                    i, j = (p // m) * step, (p % m) * step
                    if i >= j or self.too_close(i, j):
                        continue
                    pid = i * N + j
                    cand = (self.seg_score(self.px[i], self.px[j]), tie_hash(self.seed, iteration, pid), pid)
                    if self.better(cand, best):
                        best = cand
            else:
                for j in range(N):
                    if j == cur or self.too_close(cur, j) or j in hist:
                        continue
                    cand = (self.seg_score(self.px[cur], self.px[j]), tie_hash(self.seed, iteration, j), j)
                    if self.better(cand, best):
                        best = cand
            if best[2] == NONE:
                C[2 + T + t] = 1
                continue
            a, b = (best[2] // N, best[2] % N) if cur < 0 else (cur, best[2])
            self.draw(a, b)
            base = t * M
            if cur < 0:
                P[base], self.Score[base] = a, 0
                P[base + 1], self.Score[base + 1] = b, best[0]
                C[2 + t] = 2
            else:
                P[base + length], self.Score[base + length] = b, best[0]
                C[2 + t] = length + 1
            C[0] += 1
            C[1] += 1

    def trails(self):
        return [[int(x) for x in self.Path[t * self.M: t * self.M + int(self.Counters[2 + t])]]
                for t in range(self.T)]


def compare(image, lines, trails=1, pegs=120, seed=0, resolution=96, invert=False):
    lum, alpha = ref.load_luminance(image, resolution)
    uv = ref.map_pegs_to_uv(ref.circle_pegs(pegs), lum.shape[1], lum.shape[0])
    r = ref.ThreadEngine(lum, uv, alpha=alpha, trails=trails, seed=seed, invert=invert)
    r.run(lines)
    e = EngineEmulator(lum, alpha, uv, line_count=lines, trails=trails, seed=seed, invert=invert)
    e.run_pass(lines + 10)
    same = 0
    for a, b in zip(r.trails, e.trails()):
        k = 0
        while k < min(len(a), len(b)) and a[k] == b[k]:
            k += 1
        same += k
    total = sum(len(x) for x in r.trails)
    rdiff = float(np.abs(r.R.ravel() - e.R).max())
    return same, total, rdiff


if __name__ == "__main__":
    cases = [("disk", 150, 1), ("gradient", 150, 1), ("letter", 150, 1), ("letter", 150, 3),
             ("disk", 120, 2, True)]
    ok = True
    for c in cases:
        image, lines, trails = c[:3]
        invert = len(c) > 3
        same, total, rdiff = compare(image, lines, trails, invert=invert)
        print(f"{image:9} lines={lines} trails={trails} invert={invert}: "
              f"identical prefix {same}/{total} vertices, max |R diff| = {rdiff:.2e}")
        ok &= same == total
    sys.exit(0 if ok else 1)
