"""Parameter Execute DAT of the ImageThreading COMP (watches its custom parameters).

Reset / Step pulses, and Auto Reset when a parameter that changes the result
is edited (SPEC 3.2). Changes of the input image or pegs are not detected yet:
press Reset after changing them.
"""

# Parameters whose change invalidates the computed threads.
RESET_PARS = {
    'Linecount', 'Trails', 'Lineopacity', 'Historylength', 'Minpegdist', 'Invert', 'Seed',
    'Buildmode', 'Fit', 'Scalex', 'Scaley', 'Offsetx', 'Offsety', 'Aspect', 'Resolution',
    'Debugrandompath',
}


def _ext(par):
    return par.owner.ext.ImageThreadingExt


def onPulse(par):
    if par.name == 'Reset':
        _ext(par).Reset()
    elif par.name == 'Step':
        _ext(par).Step()


def onValueChange(par, prev):
    if par.name in RESET_PARS and par.owner.par.Autoreset.eval():
        _ext(par).Reset()


def onValuesChanged(changes):
    return


def onExpressionChange(par, val, prev):
    return


def onExportChange(par, val, prev):
    return


def onEnableChange(par, val, prev):
    return


def onModeChange(par, val, prev):
    return
