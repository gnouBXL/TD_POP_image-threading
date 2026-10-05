"""Build the ImageThreading COMP inside TouchDesigner 2025.3x (phases 1-2).

Usage, in TouchDesigner:
    1. Create a Text DAT, set its File parameter to this file
       (…/TD_POP_image-threading/td/build_imagethreading.py).
    2. Right-click the DAT > Run Script.

It (re)builds `ImageThreading` next to the Text DAT, plus a small demo
(`demo_image` + `demo_pegs` wired into it). Shaders and the extension are
loaded from the repository (glsl/, python/) into Text DATs with Sync to File,
so editing the repository files updates the network.

Phases 1-2 content (docs/SPEC.md, sections 3, 5.3 and 6):
    - custom parameters of every page;
    - XY -> UV mapping of the pegs (Analyze POP + GLSL POP), Output Pegs Only;
    - debug_overlay TOP: pegs drawn in UV over the image (phase 1 check);
    - engine state with a RANDOM path (Debug page, `Debugrandompath`), turned
      into Line Strips with the original XYZ (phase 2 check).

Parameter names come from docs.derivative.ca. Menu entries whose internal
name is not documented are chosen by label with set_menu(), which raises an
error listing the available entries if the guess is wrong: report that
message and the script gets fixed in one go.
"""

import os
import td

SCRIPT_DAT = me
NAME = 'ImageThreading'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def repo_root():
    f = SCRIPT_DAT.par.file.eval()
    if not f:
        raise RuntimeError('Set the File parameter of this Text DAT to td/build_imagethreading.py')
    if not os.path.isabs(f):
        f = os.path.join(project.folder, f)
    return os.path.dirname(os.path.dirname(os.path.abspath(f)))


def set_menu(par, *wanted):
    """Pick a menu entry by name or label (case-insensitive, exact then substring)."""
    names, labels = list(par.menuNames), list(par.menuLabels)
    for w in wanted:
        lw = w.lower()
        for n, l in zip(names, labels):
            if lw == n.lower() or lw == l.lower():
                par.val = n
                return n
    for w in wanted:
        lw = w.lower()
        for n, l in zip(names, labels):
            if lw in n.lower() or lw in l.lower():
                par.val = n
                return n
    raise ValueError(f'{par.owner.path}: {par.name} has no entry like {wanted}; '
                     f'entries: {list(zip(names, labels))}')


def make(comp, type_name, name, x, y):
    cls = getattr(td, type_name, None)
    if cls is None:
        raise RuntimeError(f'Unknown operator type {type_name}')
    n = comp.create(cls, name)
    n.nodeX, n.nodeY = x, y
    return n


def wire(src, dst, index=0):
    # Connect connector to connector: Connector.connect() rejects a COMP passed
    # as the target ("Invalid number or type of arguments"), an OP works only
    # for non-COMP sources.
    dst.inputConnectors[index].connect(src.outputConnectors[0])


def text_from_file(comp, name, path, x, y):
    n = make(comp, 'textDAT', name, x, y)
    n.par.file = path
    if hasattr(n.par, 'syncfile'):
        n.par.syncfile = True
    n.text = open(path, encoding='utf-8').read()
    n.viewer = False
    return n


def add_uniforms(n, uniforms):
    """uniforms: list of (name, glsl_type, [component expressions])."""
    n.seq.vec.numBlocks = len(uniforms)
    for i, (uname, utype, exprs) in enumerate(uniforms):
        getattr(n.par, f'vec{i}name').val = uname
        if hasattr(n.par, f'vec{i}type'):  # GLSL POPs; the GLSL TOP has no type (declared in the shader)
            set_menu(getattr(n.par, f'vec{i}type'), utype)
        for comp_name, e in zip('xyzw', exprs):
            getattr(n.par, f'vec{i}value{comp_name}').expr = e


def create_attrs(n, attrs):
    """attrs: list of (name, 'float'|'int', components) on the Create Attribs page."""
    n.seq.attr.numBlocks = len(attrs)
    for i, (aname, atype, ncomp) in enumerate(attrs):
        set_menu(getattr(n.par, f'attr{i}name'), 'custom')
        getattr(n.par, f'attr{i}customname').val = aname
        set_menu(getattr(n.par, f'attr{i}type'), *(('int', 'integer') if atype == 'int' else ('float',)))
        if ncomp > 1 or hasattr(n.par, f'attr{i}numcomps'):
            set_menu(getattr(n.par, f'attr{i}numcomps'), str(ncomp))


def P(name):
    """Expression reading a custom parameter of the COMP (evaluated value)."""
    return f'parent().par.{name}.eval()'


def setp(group, **attrs):
    """Set attributes (default, min, clampMin, normMax, menuNames…) on every Par of a ParGroup."""
    for par in group:
        for k, v in attrs.items():
            setattr(par, k, v)
    return group


# ---------------------------------------------------------------------------
# Custom parameters (SPEC 3.2)
# ---------------------------------------------------------------------------

def build_parameters(c):
    pg = c.appendCustomPage('Threading')
    setp(pg.appendInt('Linecount', label='Line Count'), default=2000, min=1, clampMin=True, normMax=10000)
    setp(pg.appendInt('Trails', label='Trails'), default=1, min=1, clampMin=True, normMax=8)
    setp(pg.appendFloat('Lineopacity', label='Line Opacity'), default=0.1, normMax=1)
    setp(pg.appendInt('Historylength', label='History Length'), default=20, min=0, clampMin=True, normMax=100)
    setp(pg.appendFloat('Minpegdist', label='Min Peg Distance'), default=0.2, normMax=1)
    setp(pg.appendToggle('Invert', label='Invert'), default=False)
    setp(pg.appendInt('Seed', label='Seed'), default=0, normMax=100)

    pg = c.appendCustomPage('Build')
    setp(pg.appendMenu('Buildmode', label='Build Mode'), menuNames=['progressive', 'allatonce'],
         menuLabels=['Progressive', 'All At Once'], default='progressive')
    setp(pg.appendInt('Iterperframe', label='Iterations Per Frame'), default=10, min=0, clampMin=True, normMax=200)
    pg.appendPulse('Step', label='Step')
    pg.appendPulse('Reset', label='Reset')
    setp(pg.appendToggle('Autoreset', label='Auto Reset'), default=True)

    pg = c.appendCustomPage('Image Mapping')
    setp(pg.appendMenu('Fit', label='Fit'), menuNames=['bounds', 'manual'],
         menuLabels=['Bounds', 'Manual'], default='bounds')
    setp(pg.appendXY('Scale', label='Scale'), default=1)
    pg.appendXY('Offset', label='Offset')
    setp(pg.appendMenu('Aspect', label='Aspect'), menuNames=['fit', 'fill', 'stretch'],
         menuLabels=['Fit', 'Fill', 'Stretch'], default='fit')
    setp(pg.appendInt('Resolution', label='Resolution'), default=256, min=8, clampMin=True, normMax=1024)

    pg = c.appendCustomPage('Output')
    setp(pg.appendRGB('Color', label='Color'), default=0)
    setp(pg.appendToggle('Pegsonly', label='Output Pegs Only'), default=False)

    pg = c.appendCustomPage('Debug')
    setp(pg.appendToggle('Debugrandompath', label='Random Path (no engine)'), default=True)
    setp(pg.appendFloat('Debugpegradius', label='Overlay Peg Radius'), default=3, normMax=10)

    for par in c.customPars:
        if not par.isPulse:
            par.val = par.default


# ---------------------------------------------------------------------------
# Network (SPEC 5.3)
# ---------------------------------------------------------------------------

def build_network(c, root):
    glsl = os.path.join(root, 'glsl')
    X = 200

    # ---- inputs / outputs ----------------------------------------------
    in_image = make(c, 'inTOP', 'in_image', 0, 400)
    in_pegs = make(c, 'inPOP', 'in_pegs', 0, 0)
    if hasattr(in_pegs.par, 'connectorder'):
        in_pegs.par.connectorder = 1

    # ---- shaders and extension -----------------------------------------
    sx = -3 * X
    text_from_file(c, 'shader_common', os.path.join(glsl, 'common.glsl'), sx, 600)
    text_from_file(c, 'shader_pegs_uv', os.path.join(glsl, 'pegs_uv.comp'), sx, 450)
    text_from_file(c, 'shader_state_init', os.path.join(glsl, 'state_init.comp'), sx, 300)
    text_from_file(c, 'shader_build_threads', os.path.join(glsl, 'build_threads.comp'), sx, 150)
    text_from_file(c, 'shader_trail_id', os.path.join(glsl, 'trail_id.comp'), sx, 0)
    text_from_file(c, 'shader_debug_overlay', os.path.join(glsl, 'debug_overlay.frag'), sx, -150)
    text_from_file(c, 'ext_imagethreading', os.path.join(root, 'python', 'ext_imagethreading.py'), sx, -300)

    # ---- working image (used for the residual from phase 3 on) ---------
    image_prep = make(c, 'resolutionTOP', 'image_prep', X, 400)
    wire(in_image, image_prep)
    image_prep.par.outputresolution = 'custom'
    side = (f"{P('Resolution')} / max(op('in_image').width, op('in_image').height)")
    image_prep.par.resolutionw.expr = f"max(1, round(op('in_image').width * {side}))"
    image_prep.par.resolutionh.expr = f"max(1, round(op('in_image').height * {side}))"
    if hasattr(image_prep.par, 'highqualresize'):
        image_prep.par.highqualresize = True

    # ---- pegs: XY -> UV (phase 1) --------------------------------------
    pegs_bounds = make(c, 'analyzePOP', 'pegs_bounds', X, -150)
    wire(in_pegs, pegs_bounds)
    set_menu(pegs_bounds.par.attrclass, 'point')
    pegs_bounds.par.inputattrs = 'P'
    for t, v in (('min', True), ('max', True), ('avg', False), ('centroid', False),
                 ('size', False), ('appendattrname', False)):
        if hasattr(pegs_bounds.par, t):
            setattr(pegs_bounds.par, t, v)

    pegs_uv = make(c, 'glslPOP', 'pegs_uv', 2 * X, 0)
    wire(in_pegs, pegs_uv, 0)
    wire(pegs_bounds, pegs_uv, 1)
    pegs_uv.par.computedat = 'shader_pegs_uv'
    set_menu(pegs_uv.par.attrclass, 'point')
    set_menu(pegs_uv.par.numthreadsmode, 'auto')
    create_attrs(pegs_uv, [('PegUV', 'float', 2)])
    add_uniforms(pegs_uv, [
        ('uFit', 'int', ["parent().par.Fit.menuIndex"]),
        ('uAspect', 'int', ["parent().par.Aspect.menuIndex"]),
        ('uScale', 'vec2', [P('Scalex'), P('Scaley')]),
        ('uOffset', 'vec2', [P('Offsetx'), P('Offsety')]),
        ('uImageRes', 'vec2', ["op('image_prep').width", "op('image_prep').height"]),
    ])

    debug_overlay = make(c, 'glslTOP', 'debug_overlay', 2 * X, 550)
    wire(in_image, debug_overlay)
    debug_overlay.par.pixeldat = 'shader_debug_overlay'
    debug_overlay.seq.buffer.numBlocks = 1
    debug_overlay.par.buffer0pop = 'pegs_uv'
    set_menu(debug_overlay.par.buffer0attrclass, 'point')
    debug_overlay.par.buffer0attr = 'PegUV'
    debug_overlay.par.buffer0name = 'PegUV'
    add_uniforms(debug_overlay, [
        ('uRadius', 'float', [P('Debugpegradius')]),
        ('uDotColor', 'vec4', ['1', '0.1', '0.1', '1']),
    ])

    # ---- engine state (phase 3 residual; random path for phase 2) ------
    residual_init = make(c, 'toptoPOP', 'residual_init', 2 * X, 400)
    residual_init.par.input0top = 'image_prep'
    set_menu(residual_init.par.rgba, 'color')
    set_menu(residual_init.par.input0filter, 'nearest')
    set_menu(residual_init.par.pixelsamplingloc, 'pixelcentered')
    set_menu(residual_init.par.surftype, 'none')

    state_init = make(c, 'glslPOP', 'state_init', 3 * X, 300)
    wire(residual_init, state_init, 0)
    wire(pegs_uv, state_init, 1)
    state_init.par.computedat = 'shader_state_init'
    set_menu(state_init.par.attrclass, 'point')
    set_menu(state_init.par.numthreadsmode, 'auto')
    create_attrs(state_init, [('R', 'float', 1), ('Path', 'int', 1),
                              ('Score', 'float', 1), ('Counters', 'int', 1)])
    add_uniforms(state_init, [
        ('uInvert', 'int', [f"int({P('Invert')})"]),
        ('uLineCount', 'int', [P('Linecount')]),
        ('uTrails', 'int', [P('Trails')]),
        ('uSeed', 'int', [P('Seed')]),
        ('uDebugRandom', 'int', [f"int({P('Debugrandompath')})"]),
    ])
    # Phases 4-7 insert the engine (Feedback loop / All At Once) here.
    state = make(c, 'nullPOP', 'state', 4 * X, 300)
    wire(state_init, state)

    # ---- output: path -> Line Strips (phase 2) -------------------------
    trail_len = f"(-(-{P('Linecount')} // max(1, {P('Trails')})) + 1)"

    threads_points = make(c, 'glsladvancedPOP', 'threads_points', 5 * X, 150)
    wire(state, threads_points, 0)
    wire(pegs_uv, threads_points, 1)
    threads_points.par.computedat = 'shader_build_threads'
    set_menu(threads_points.par.shaderdispatchmode, 'single')
    set_menu(threads_points.par.numthreadsmode, 'outputpoint')
    set_menu(threads_points.par.maxpointsmode, 'custom', 'set', 'manual')
    threads_points.par.maxpoints.expr = f"max(1, {P('Trails')}) * {trail_len}"
    set_menu(threads_points.par.pointcountinfo, 'fromparams')
    threads_points.par.ptoutputattrs = 'P Color Score'
    create_attrs(threads_points, [('PegIndex', 'int', 1), ('Step', 'int', 1),
                                  ('StepNorm', 'float', 1), ('LineStripIndex', 'int', 1)])
    add_uniforms(threads_points, [
        ('uTrails', 'int', [P('Trails')]),
        ('uTrailLen', 'int', [trail_len]),
        ('uColor', 'vec4', [P('Colorr'), P('Colorg'), P('Colorb'), P('Lineopacity')]),
    ])

    threads_clean = make(c, 'attributePOP', 'threads_clean', 6 * X, 150)
    wire(threads_points, threads_clean)
    threads_clean.par.deletepoint = 'R Path Counters'

    threads_strips = make(c, 'linebreakPOP', 'threads_strips', 7 * X, 150)
    wire(threads_clean, threads_strips)
    set_menu(threads_strips.par.connecmode, 'onelinestrip')
    threads_strips.par.uselinestripindex = True
    threads_strips.par.linestripindexname = 'LineStripIndex'

    threads_trailid = make(c, 'glslPOP', 'threads_trailid', 8 * X, 150)
    wire(threads_strips, threads_trailid)
    threads_trailid.par.computedat = 'shader_trail_id'
    set_menu(threads_trailid.par.attrclass, 'primitive')
    set_menu(threads_trailid.par.numthreadsmode, 'auto')
    create_attrs(threads_trailid, [('TrailId', 'int', 1)])

    output_select = make(c, 'switchPOP', 'output_select', 9 * X, 0)
    wire(threads_trailid, output_select, 0)
    wire(pegs_uv, output_select, 1)
    output_select.par.index.expr = f"1 if {P('Pegsonly')} else 0"

    out = make(c, 'outPOP', 'out_threads', 10 * X, 0)
    wire(output_select, out)
    out.display = out.render = True

    return out


# ---------------------------------------------------------------------------
# Render network (outside the COMP): see the result without building it by hand
# ---------------------------------------------------------------------------

RENDER_OPS = ('view_geo', 'view_mat', 'view_target', 'view_cam_front', 'view_cam_orbit',
              'view_front', 'view_orbit')


def build_render(parent_comp, it, x, y):
    """Front orthographic view (where the image appears) + orbiting perspective view.

    The threads are unlit lines: no light needed. Front camera framing comes
    from ImageThreadingExt.ImageRect() (image rectangle in world XY).
    """
    X = 200
    rect = f"op('{it.name}').ImageRect()"      # promoted extension method: (cx, cy, w, h)

    # Geometry COMP: its In POP receives the threads, Null POP is rendered.
    geo = make(parent_comp, 'geometryCOMP', 'view_geo', x + 2 * X, y)
    for child in list(geo.children):
        child.destroy()
    gin = make(geo, 'inPOP', 'in_threads', 0, 0)
    gout = make(geo, 'nullPOP', 'threads', 200, 0)
    wire(gin, gout)
    gout.display = gout.render = True
    wire(it, geo, 0)

    # Line MAT: color and alpha from the Color attribute (alpha = Line Opacity),
    # alpha blending, no depth test so every thread accumulates.
    mat = make(parent_comp, 'lineMAT', 'view_mat', x + 2 * X, y - 2 * X)
    mat.par.linecoloratt = 'Color'
    mat.par.linenearcolorr = mat.par.linenearcolorg = mat.par.linenearcolorb = 1
    mat.par.linenearalpha = 1
    mat.par.widthnear = 1
    mat.par.widthfar = 1
    mat.par.drawpoints = False
    mat.par.blending = True
    set_menu(mat.par.srcblend, 'source alpha', 'sa')
    set_menu(mat.par.destblend, 'one minus source alpha', 'omsa')
    mat.par.depthtest = False
    mat.par.depthwriting = False
    geo.par.material = mat.name

    # Front camera: orthographic, centered on the image, width = image width.
    front = make(parent_comp, 'cameraCOMP', 'view_cam_front', x + 2 * X, y + 2 * X)
    set_menu(front.par.projection, 'ortho')
    front.par.tx.expr = f'{rect}[0]'
    front.par.ty.expr = f'{rect}[1]'
    front.par.tz = 1000
    front.par.near = 0.01
    front.par.far = 10000
    front.par.orthowidth.expr = f'{rect}[2]'

    # Orbit camera: circles the image center, always looking at it.
    target = make(parent_comp, 'nullCOMP', 'view_target', x + 3 * X, y + 2 * X)
    target.par.tx.expr = f'{rect}[0]'
    target.par.ty.expr = f'{rect}[1]'
    orbit = make(parent_comp, 'cameraCOMP', 'view_cam_orbit', x + 4 * X, y + 2 * X)
    dist = f'1.6 * max({rect}[2], {rect}[3])'
    angle = 'math.radians(absTime.seconds * 15)'     # 15 degrees per second
    orbit.par.tx.expr = f'{rect}[0] + {dist} * math.sin({angle})'
    orbit.par.ty.expr = f'{rect}[1] + 0.25 * {dist}'
    orbit.par.tz.expr = f'{dist} * math.cos({angle})'
    orbit.par.lookat = target.name
    orbit.par.near = 0.01
    orbit.par.far = 10000

    # Renders. Background: white (black with Invert), like the reference render.
    bg = f"0 if op('{it.name}').par.Invert else 1"
    for name, cam, nx in (('view_front', front, 5), ('view_orbit', orbit, 6)):
        r = make(parent_comp, 'renderTOP', name, x + nx * X, y)
        r.par.camera = cam.name
        r.par.geometry = geo.name
        r.par.lights = ''
        r.par.outputresolution = 'custom'
        r.par.resolutionw = 1024
        if name == 'view_front':   # image aspect ratio
            r.par.resolutionh.expr = f"max(1, round(1024 * {rect}[3] / max({rect}[2], 1e-9)))"
        else:
            r.par.resolutionh = 576
        for i, comp_name in enumerate('rgb'):
            getattr(r.par, f'bgcolor{comp_name}').expr = bg
        r.par.bgcolora = 1
        r.viewer = True
    return geo


# ---------------------------------------------------------------------------

def build():
    root = repo_root()
    parent_comp = SCRIPT_DAT.parent()
    old = parent_comp.op(NAME)
    x, y = (old.nodeX, old.nodeY) if old else (SCRIPT_DAT.nodeX + 300, SCRIPT_DAT.nodeY)
    if old:
        old.destroy()
    for n in ('demo_image', 'demo_pegs') + RENDER_OPS:
        if parent_comp.op(n):
            parent_comp.op(n).destroy()

    c = make(parent_comp, 'baseCOMP', NAME, x, y)
    c.comment = 'ImageThreading POP — built by td/build_imagethreading.py'
    build_parameters(c)
    build_network(c, root)

    c.seq.ext.numBlocks = max(1, c.seq.ext.numBlocks)
    c.par.ext0object = "op('./ext_imagethreading').module.ImageThreadingExt(me)"
    c.par.ext0promote = True
    c.par.reinitextensions.pulse()

    # Demo inputs: default Movie File In image + 200 pegs on a circle.
    img = make(parent_comp, 'moviefileinTOP', 'demo_image', x - 300, y + 100)
    pegs = make(parent_comp, 'circlePOP', 'demo_pegs', x - 300, y - 100)
    pegs.par.divs = 200
    set_menu(pegs.par.connectivity, 'none')
    wire(img, c, 0)
    wire(pegs, c, 1)

    build_render(parent_comp, c, x, y)

    problems = c.errors(recurse=True)
    print(f'{c.path} built from {root}')
    if problems:
        print('Errors after build:\n' + problems)
    return c


build()
