"""Extension of the ImageThreading COMP (SPEC 3.2, 5.3).

Layout helpers, framing of the render, limit checks, Reset / Step of the
engine's Feedback POP loop (SPEC 5.3).

Attached by td/build_imagethreading.py:
    comp.par.ext0object = "op('./ext_imagethreading').module.ImageThreadingExt(me)"
"""


class ImageThreadingExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp

    # ---- layout (must match glsl/common.glsl) ---------------------------

    @property
    def Trails(self):
        return max(1, int(self.ownerComp.par.Trails.eval()))

    @property
    def LineCount(self):
        return max(0, int(self.ownerComp.par.Linecount.eval()))

    @property
    def TrailLen(self):
        """M: path entries (vertices) reserved per trail."""
        return -(-self.LineCount // self.Trails) + 1

    @property
    def OutputPoints(self):
        return self.Trails * self.TrailLen

    @property
    def StateSize(self):
        """Points of the state list: W x H of the working image."""
        img = self.ownerComp.op('image_prep')
        return img.width * img.height if img else 0

    # ---- engine loop (Feedback POP state_fb) ------------------------------

    def Reset(self):
        """Restart from the initial state: the Feedback POP has no Reset, so
        Initialize (snapshot of state_init) then Start on the next frame."""
        fb = self.ownerComp.op('state_fb')
        if fb is None:
            return
        fb.par.initializepulse.pulse()
        run("args[0].par.startpulse.pulse()", fb, delayFrames=1)

    def Step(self):
        """Pause (Play off) and advance the loop by one frame = Iterperframe iterations."""
        self.ownerComp.par.Play = False
        self.ownerComp.op('state_fb').par.steppulse.pulse()

    # ---- framing (render network) ----------------------------------------

    def ImageRect(self):
        """(cx, cy, w, h): rectangle covered by the image in world XY, i.e. the
        inverse of the peg mapping (SPEC 4.1, glsl/pegs_uv.comp). Used by the
        front camera. Reads the Analyze POP one frame late (no GPU stall)."""
        c = self.ownerComp
        img = c.op('image_prep')
        W, H = max(1, img.width), max(1, img.height)
        if c.par.Fit.eval() == 'manual':
            sx = c.par.Scalex.eval() or 1e-9
            sy = c.par.Scaley.eval() or 1e-9
            ox, oy = c.par.Offsetx.eval(), c.par.Offsety.eval()
            return ((0.5 - ox) / sx, (0.5 - oy) / sy, abs(1 / sx), abs(1 / sy))
        lo, hi = self._bounds()
        size = [max(hi[i] - lo[i], 1e-12) for i in (0, 1)]
        k = (1.0, 1.0)
        aspect = c.par.Aspect.eval()
        if aspect != 'stretch':
            ratio = (size[0] / size[1]) / (W / H)
            if aspect == 'fit':
                k = (ratio, 1.0) if ratio > 1 else (1.0, 1.0 / ratio)
            else:
                k = (1.0, 1.0 / ratio) if ratio > 1 else (ratio, 1.0)
        return (lo[0] + 0.5 * size[0], lo[1] + 0.5 * size[1], size[0] / k[0], size[1] / k[1])

    def _bounds(self):
        b = self.ownerComp.op('pegs_bounds')
        try:
            lo = tuple(b.point('Min', 0, delayed=True))
            hi = tuple(b.point('Max', 0, delayed=True))
            if len(lo) >= 2 and len(hi) >= 2:
                return lo, hi
        except Exception:
            pass
        return (-1.0, -1.0), (1.0, 1.0)     # before the first cook

    # ---- checks ---------------------------------------------------------

    def Check(self):
        """Return a list of problems with the current parameters (empty if OK)."""
        problems = []
        s = self.StateSize
        if s and self.OutputPoints > s:
            problems.append(
                f'Line Count + Trails too large for a {s}-pixel residual: '
                f'{self.OutputPoints} path entries > {s}. Raise Resolution or lower Line Count.')
        if s and 2 + 2 * self.Trails > s:
            problems.append('Too many Trails for the residual resolution.')
        pegs = self.ownerComp.op('in_pegs')
        if pegs is not None and pegs.numPoints() < 2:
            problems.append('Need at least 2 pegs.')
        return problems

    # No check in onInitTD: at that point the inputs have not cooked yet
    # (numPoints() is 0), which printed a false "Need at least 2 pegs".
