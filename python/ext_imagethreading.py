"""Extension of the ImageThreading COMP (SPEC 3.2, 5.3).

Phases 1-2: layout helpers and limit checks. Reset / Step / Auto Reset / Build
Mode arrive with the engine (phases 5-6).

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
