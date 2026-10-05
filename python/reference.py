"""CPU reference for the ImageThreading POP engine (docs/SPEC.md, section 4).

Standalone, outside TouchDesigner. It exists to validate the algorithm and to
give the GLSL engine a ground truth to compare against (same seed, same
parameters -> same path).

Example:
    python reference.py portrait.jpg --pegs-circle 200 --lines 3000 --out out/portrait
    python reference.py disk --lines 500 --out out/disk
    python reference.py portrait.jpg --pegs-file pegs.csv --out out/sculpture

Outputs (prefix given by --out):
    <out>.json          parameters, pegs (xyz + uv), path of each trail, scores
    <out>_render.png    front view of the threads (dark thread on white)
    <out>_residual.png  residual R at the end of the computation
    <out>.obj           3D polylines with the original XYZ of the pegs
"""

import argparse
import json
import math
import os
import time

import numpy as np
from PIL import Image, ImageDraw

MASK32 = np.uint32(0xFFFFFFFF)


# --------------------------------------------------------------------------
# Hash used for tie-breaking. Integer-only so the GLSL engine can reproduce it
# bit for bit (uint arithmetic wraps the same way).
# --------------------------------------------------------------------------

def wang_hash(x):
    x = np.asarray(x, dtype=np.uint32)
    with np.errstate(over="ignore"):
        x = (x ^ np.uint32(61)) ^ (x >> np.uint32(16))
        x = x * np.uint32(9)
        x = x ^ (x >> np.uint32(4))
        x = x * np.uint32(0x27D4EB2D)
        x = x ^ (x >> np.uint32(15))
    return x


def tie_hash(seed, iteration, candidates):
    with np.errstate(over="ignore"):
        h = wang_hash(np.uint32(seed) ^ wang_hash(np.uint32(iteration)))
        return wang_hash(h ^ np.asarray(candidates, dtype=np.uint32))


# --------------------------------------------------------------------------
# Inputs
# --------------------------------------------------------------------------

def load_luminance(source, resolution):
    """Return an (H, W) float32 array in [0, 1]. Row 0 is the BOTTOM of the
    image, so that +Y goes up like a TouchDesigner texture's V."""
    if source in SYNTHETIC:
        img = SYNTHETIC[source](resolution)
    else:
        img = Image.open(source).convert("L")
    w, h = img.size
    s = resolution / max(w, h)
    img = img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    lum = np.asarray(img, dtype=np.float32) / 255.0
    return np.ascontiguousarray(lum[::-1])


def _synthetic_disk(res):
    yy, xx = np.mgrid[0:res, 0:res] + 0.5
    r = np.hypot(xx - res / 2, yy - res / 2)
    return Image.fromarray(np.where(r < res * 0.3, 0, 255).astype(np.uint8))


def _synthetic_gradient(res):
    row = np.linspace(0, 255, res).astype(np.uint8)
    return Image.fromarray(np.tile(row, (res, 1)))


def _synthetic_letter(res):
    img = Image.new("L", (res, res), 255)
    d = ImageDraw.Draw(img)
    t = max(2, res // 10)
    # a blocky "A"
    d.line([(res * 0.2, res * 0.85), (res * 0.5, res * 0.15)], fill=0, width=t)
    d.line([(res * 0.8, res * 0.85), (res * 0.5, res * 0.15)], fill=0, width=t)
    d.line([(res * 0.33, res * 0.6), (res * 0.67, res * 0.6)], fill=0, width=t)
    return img


SYNTHETIC = {
    "disk": _synthetic_disk,
    "gradient": _synthetic_gradient,
    "letter": _synthetic_letter,
}


def circle_pegs(count, radius=1.0, start_angle=0.0):
    a = start_angle + 2 * np.pi * np.arange(count) / count
    return np.stack([radius * np.cos(a), radius * np.sin(a), np.zeros(count)], axis=1)


def load_pegs_file(path):
    """CSV (x,y,z per line, optional header) or .npy of shape (N, 2|3)."""
    if path.endswith(".npy"):
        p = np.load(path)
    else:
        p = np.genfromtxt(path, delimiter=",", dtype=np.float64)
        if np.isnan(p[0]).all():
            p = p[1:]
    p = np.atleast_2d(p)[:, :3]
    if p.shape[1] == 2:
        p = np.concatenate([p, np.zeros((len(p), 1))], axis=1)
    return p


# --------------------------------------------------------------------------
# Image mapping (SPEC 4.1): peg XY -> UV, Z ignored
# --------------------------------------------------------------------------

def map_pegs_to_uv(P, img_w, img_h, fit="bounds", aspect="fit",
                   scale=(1.0, 1.0), offset=(0.0, 0.0)):
    xy = P[:, :2].astype(np.float64)
    if fit == "manual":
        return xy * np.asarray(scale) + np.asarray(offset)

    lo, hi = xy.min(axis=0), xy.max(axis=0)
    size = np.maximum(hi - lo, 1e-12)
    uv = (xy - lo) / size                       # bounds -> [0,1]^2 (stretch)
    if aspect == "stretch":
        return uv

    # Keep the image undistorted relative to the peg cloud.
    bounds_aspect = size[0] / size[1]
    image_aspect = img_w / img_h
    ratio = bounds_aspect / image_aspect        # >1: bounds wider than image
    if aspect == "fit":                         # whole image inside the bounds
        k = np.array([ratio, 1.0]) if ratio > 1 else np.array([1.0, 1.0 / ratio])
    else:                                       # "fill": bounds inside the image
        k = np.array([1.0, 1.0 / ratio]) if ratio > 1 else np.array([ratio, 1.0])
    return (uv - 0.5) * k + 0.5


# --------------------------------------------------------------------------
# Engine (SPEC 4.2 - 4.6)
# --------------------------------------------------------------------------

class ThreadEngine:
    def __init__(self, lum, pegs_uv, *, line_opacity=0.1, history_length=20,
                 min_peg_dist=0.2, invert=False, seed=0, trails=1):
        self.H, self.W = lum.shape
        self.R = (1.0 - lum if invert else lum).astype(np.float32).copy()
        self.uv = np.asarray(pegs_uv, dtype=np.float64)
        self.px = self.uv * np.array([self.W, self.H])   # pixel space
        self.a = float(line_opacity)
        self.history_length = int(history_length)
        self.min_peg_dist = float(min_peg_dist)
        self.seed = int(seed)
        self.trails = [[] for _ in range(max(1, int(trails)))]
        self.scores = [[] for _ in self.trails]
        self.dead = [False] * len(self.trails)
        self.iteration = 0
        self.segment_count = 0
        # Pairwise UV distances: used for the "too close" exclusion.
        d = self.uv[:, None, :] - self.uv[None, :, :]
        self.too_close = np.hypot(d[..., 0], d[..., 1]) < self.min_peg_dist
        np.fill_diagonal(self.too_close, True)

    # ---- sampling --------------------------------------------------------

    def sample(self, x, y):
        """Bilinear sample of R at pixel coordinates (pixel centers at i+0.5).
        Outside the image, R = 1: nothing to draw there."""
        fx, fy = x - 0.5, y - 0.5
        x0, y0 = np.floor(fx).astype(np.int64), np.floor(fy).astype(np.int64)
        tx, ty = fx - x0, fy - y0
        out = np.zeros_like(x, dtype=np.float32)
        for dx, dy, w in ((0, 0, (1 - tx) * (1 - ty)), (1, 0, tx * (1 - ty)),
                          (0, 1, (1 - tx) * ty), (1, 1, tx * ty)):
            xi, yi = x0 + dx, y0 + dy
            inside = (xi >= 0) & (xi < self.W) & (yi >= 0) & (yi < self.H)
            v = np.ones_like(out)
            v[inside] = self.R[yi[inside], xi[inside]]
            out += w * v
        return out

    def score_from(self, a_idx, b_idx):
        """Vectorized SPEC 4.3 for segments a_idx[k] -> b_idx[k]."""
        A, B = self.px[a_idx], self.px[b_idx]
        n = np.maximum(1, np.ceil(np.hypot(*(B - A).T))).astype(np.int64)
        S = int(n.max())
        k = np.arange(1, S + 1)[None, :]
        t = k / (n[:, None] + 1.0)
        valid = k <= n[:, None]
        x = A[:, 0:1] + (B[:, 0:1] - A[:, 0:1]) * t
        y = A[:, 1:2] + (B[:, 1:2] - A[:, 1:2]) * t
        v = 0.5 - (self.sample(x, y) + self.a)
        return np.where(valid, v, 0.0).sum(axis=1) / n

    # ---- drawing ---------------------------------------------------------

    def segment_pixels(self, i, j):
        """DDA raster of a 1 px line: one pixel per step along the major axis.
        Each pixel appears once, so the GPU can write it without races."""
        (x0, y0), (x1, y1) = self.px[i] - 0.5, self.px[j] - 0.5
        n = int(math.ceil(max(abs(x1 - x0), abs(y1 - y0)))) + 1
        t = np.linspace(0.0, 1.0, n)
        xi = np.rint(x0 + (x1 - x0) * t).astype(np.int64)
        yi = np.rint(y0 + (y1 - y0) * t).astype(np.int64)
        keep = (xi >= 0) & (xi < self.W) & (yi >= 0) & (yi < self.H)
        return xi[keep], yi[keep]

    def draw(self, i, j):
        xi, yi = self.segment_pixels(i, j)
        self.R[yi, xi] = np.minimum(1.0, self.R[yi, xi] + self.a)

    # ---- selection -------------------------------------------------------

    def pick(self, scores, candidates):
        best = scores.max()
        tied = candidates[scores == best]
        if len(tied) > 1:
            tied = tied[[np.argmin(tie_hash(self.seed, self.iteration, tied))]]
        return int(tied[0]), float(best)

    def best_start(self):
        N = len(self.uv)
        sub = np.arange(0, N, 1 + N // 100)
        ii, jj = np.meshgrid(sub, sub, indexing="ij")
        mask = (ii < jj) & ~self.too_close[ii, jj]
        ii, jj = ii[mask], jj[mask]
        if len(ii) == 0:
            return None
        scores = self.score_from(ii, jj)
        pair_id = ii * N + jj          # unique id for tie-breaking
        best_id, best = self.pick(scores, pair_id)
        return best_id // N, best_id % N, best

    def best_next(self, trail):
        current = trail[-1]
        allowed = ~self.too_close[current].copy()
        if self.history_length > 0:
            allowed[trail[-self.history_length:]] = False
        candidates = np.flatnonzero(allowed)
        if len(candidates) == 0:
            return None
        scores = self.score_from(np.full(len(candidates), current), candidates)
        return self.pick(scores, candidates)

    def step(self):
        """Add ONE segment, to the trails in turn (SPEC 4.6). False if stuck."""
        t = self.segment_count % len(self.trails)
        for _ in range(len(self.trails)):
            if not self.dead[t]:
                break
            t = (t + 1) % len(self.trails)
        else:
            return False

        trail = self.trails[t]
        if not trail:
            res = self.best_start()
            if res is None:
                self.dead[t] = True
                return self.step()
            i, j, score = res
            trail.append(i)
            self.scores[t].append(0.0)
        else:
            res = self.best_next(trail)
            if res is None:
                self.dead[t] = True
                return self.step()
            j, score = res
            i = trail[-1]
        trail.append(j)
        self.scores[t].append(score)
        self.draw(i, j)
        self.iteration += 1
        self.segment_count += 1
        return True

    def run(self, line_count, progress_every=0):
        while self.segment_count < line_count:
            if not self.step():
                print(f"stopped early: no valid candidate after {self.segment_count} segments")
                break
            if progress_every and self.segment_count % progress_every == 0:
                print(f"  {self.segment_count}/{line_count}")


# --------------------------------------------------------------------------
# Outputs
# --------------------------------------------------------------------------

def render_front(engine, size, opacity, invert):
    """Front (orthographic XY) view, like the target image. Each pixel is
    covered by `count` translucent threads: coverage = 1 - (1 - opacity)^count."""
    # Frame = image area plus any peg outside it, with the image's aspect ratio.
    pix = engine.uv * np.array([engine.W, engine.H])
    lo = np.minimum(pix.min(axis=0), 0.0)
    hi = np.maximum(pix.max(axis=0), [engine.W, engine.H])
    k = (size - 1) / (hi - lo).max()
    w, h = (np.ceil((hi - lo) * k).astype(int) + 1)
    pts = (pix - lo) * k
    count = np.zeros((h, w), dtype=np.int32)
    for trail in engine.trails:
        for a, b in zip(trail, trail[1:]):
            (x0, y0), (x1, y1) = pts[a], pts[b]
            n = int(math.ceil(max(abs(x1 - x0), abs(y1 - y0)))) + 1
            t = np.linspace(0.0, 1.0, n)
            xi = np.floor(x0 + (x1 - x0) * t).astype(np.int64)
            yi = np.floor(y0 + (y1 - y0) * t).astype(np.int64)
            keep = (xi >= 0) & (xi < w) & (yi >= 0) & (yi < h)
            np.add.at(count, (yi[keep], xi[keep]), 1)
    coverage = 1.0 - (1.0 - min(max(opacity, 0.0), 1.0)) ** count
    bg, ink = (0.0, 255.0) if invert else (255.0, 0.0)
    out = bg + (ink - bg) * coverage
    return Image.fromarray(np.clip(out[::-1], 0, 255).astype(np.uint8))


def write_outputs(prefix, engine, P, params, elapsed):
    os.makedirs(os.path.dirname(os.path.abspath(prefix)), exist_ok=True)
    data = {
        "params": params,
        "elapsed_s": round(elapsed, 3),
        "segments": engine.segment_count,
        "pegs": [{"P": [float(c) for c in p], "uv": [float(c) for c in uv]}
                 for p, uv in zip(P, engine.uv)],
        "trails": [{"path": [int(i) for i in tr],
                    "score": [round(s, 6) for s in sc]}
                   for tr, sc in zip(engine.trails, engine.scores)],
    }
    with open(prefix + ".json", "w") as f:
        json.dump(data, f)

    with open(prefix + ".obj", "w") as f:
        f.write("# ImageThreading reference: original peg XYZ, one polyline per trail\n")
        base = 1
        for tr in engine.trails:
            for i in tr:
                f.write("v %f %f %f\n" % tuple(P[i]))
            if len(tr) > 1:
                f.write("l " + " ".join(str(base + k) for k in range(len(tr))) + "\n")
            base += len(tr)

    render_front(engine, params["render_size"], params["render_opacity"],
                 params["invert"]).save(prefix + "_render.png")
    r = engine.R[::-1]
    Image.fromarray((np.clip(r, 0, 1) * 255).astype(np.uint8)).save(prefix + "_residual.png")


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", help="image file, or a synthetic test: " + ", ".join(SYNTHETIC))
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--pegs-circle", type=int, default=200, help="N pegs on a circle (default)")
    g.add_argument("--pegs-file", help="CSV x,y,z or .npy exported from a POP")
    ap.add_argument("--lines", type=int, default=2000, help="Line Count")
    ap.add_argument("--trails", type=int, default=1)
    ap.add_argument("--opacity", type=float, default=0.1, help="Line Opacity (a)")
    ap.add_argument("--history", type=int, default=20, help="History Length")
    ap.add_argument("--min-dist", type=float, default=0.2, help="Min Peg Distance (UV)")
    ap.add_argument("--invert", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--resolution", type=int, default=256)
    ap.add_argument("--fit", choices=["bounds", "manual"], default="bounds")
    ap.add_argument("--aspect", choices=["fit", "fill", "stretch"], default="fit")
    ap.add_argument("--scale", type=float, nargs=2, default=(1.0, 1.0))
    ap.add_argument("--offset", type=float, nargs=2, default=(0.0, 0.0))
    ap.add_argument("--render-size", type=int, default=800)
    ap.add_argument("--render-opacity", type=float, default=None,
                    help="thread opacity in the render (default: --opacity)")
    ap.add_argument("--out", default="out/result", help="output prefix")
    args = ap.parse_args()

    lum = load_luminance(args.image, args.resolution)
    P = load_pegs_file(args.pegs_file) if args.pegs_file else circle_pegs(args.pegs_circle)
    uv = map_pegs_to_uv(P, lum.shape[1], lum.shape[0], args.fit, args.aspect,
                        args.scale, args.offset)

    engine = ThreadEngine(lum, uv, line_opacity=args.opacity, history_length=args.history,
                          min_peg_dist=args.min_dist, invert=args.invert, seed=args.seed,
                          trails=args.trails)
    t0 = time.perf_counter()
    engine.run(args.lines, progress_every=max(1, args.lines // 10))
    elapsed = time.perf_counter() - t0

    params = {k: v for k, v in vars(args).items()}
    params["render_opacity"] = args.render_opacity if args.render_opacity is not None else args.opacity
    params["peg_count"] = len(P)
    write_outputs(args.out, engine, P, params, elapsed)
    print(f"{engine.segment_count} segments, {len(P)} pegs, {elapsed:.2f}s -> {args.out}.*")


if __name__ == "__main__":
    main()
