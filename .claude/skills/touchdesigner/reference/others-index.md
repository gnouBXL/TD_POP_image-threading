# Index TOP / DAT / COMP / CHOP / MAT utiles

Même format que pops-index.md. Les anciens TOPs ne listent pas leurs paramètres dans le gabarit de la doc : utiliser `scripts/td_doc.py params <Page>` ou la page Common (`outputresolution`, `resolutionw/h`).

### In TOP — `in`
The In TOP is used to create a TOP input in a Component.

### Out TOP — `out`
The Out TOP is used to create a TOP output in a Component.

### Null TOP — `null`
The Null TOP has no effect on the image.

### Constant TOP — `constant`
The Constant TOP sets the red, green, blue, and alpha (r, g, b, and a) channels individually.

### Monochrome TOP — `mono`
The Monochrome TOP changes an image to greyscale colors.

### Level TOP — `level`
The Level TOP adjusts image contrast, brightness, gamma, black level, color range, quantization, opacity and more.

### Fit TOP — `fit`
The Fit TOP re-sizes its input to the resolution set on the Common Page using the method specified in the Fit parameter menu.

### Resolution TOP — `res`
The Resolution TOP changes the resolution of the TOP image.

### Over TOP — `over`
The Over TOP places Input1 'over' Input2.

### Composite TOP — `comp`
The Composite TOP is a multi-input TOP that will perform a composite operation for each input.

### Feedback TOP — `feedback`
The Feedback TOP can be used to create feedback effects in TOPs.

### GLSL TOP — `glsl`
The GLSL TOP renders a GLSL shader into a TOP image.
Params: `glslversion(glsl460)`, `mode`, `predat`, `vertexdat`, `pixeldat`, `computedat`, `compilebehavior(stalluntildone|threadedcheckerboard|threadedblack|threadedprevious)`, `errorbehavior(showcheckerboard|showblack|showprevious)`, `loaduniformnames`, `dispatchsize`, `outputaccess`, `type`, `depth`, `customdepth`, `autodispatchsize`, `clearoutputs`, `clearvalue`, `inputmapping`, `nval`, `inputextenduv`, `inputextendw`, `numcolorbufs`, `tops`, `simplexnoise`, `premultrgbbyalpha`, `color`, `color0name`, `color0rgb`, `color0alpha`, `vec`, `vec0name`, `vec0value`, `array`, `array0name`, `array0type(float|vec2|vec3|vec4)`, `array0chop`, `array0arraytype(uniformarray|texturebuffer)`, `matrix`, `matrix0name`, `matrix0value`, `ac`, `ac0name`, `ac0initvalue`, `ac0singlevalue`, `ac0chopvalue`, `const`, `const0name`, `const0value`, `buffer`, `buffer0pop`, `buffer0attrclass(point|vertex|primitive)`, `buffer0attr`, `buffer0name`

### POP to TOP — `poptoTOP`
The POP to TOP converts the points of a POP to the pixels of a TOP.
Params: `pop`, `rgbamode(pactive|custom)`, `extract(point|vertex|primitive)`, `attribscope`, `layout(square|wrapped|cropped|popdim)`, `dim(2d|3d)`, `depthtype(texture2darray|texture3d)`, `depth`, `rgba`

### Render TOP — `render`
The Render TOP is used to render all 3D scenes in TouchDesigner.
Params: `camera`, `multicamerahint`, `geometry`, `lights`, `antialias`, `bgcolor`, `premultrgbbyalpha`, `rendermode(cubemapods)`, `posside`, `negside`, `uvunwrapcoord(uv0|uv1|uv2|uv3|uv4|uv5|uv6|uv7)`, `uvunwrapcoordattrib`, `transparency(sortedblending|orderind|alphatocoverage)`, `depthpeel`, `transpeellayers`, `render`, `renderpulse`, `dither`, `coloroutputneeded`, `drawdepthonly`, `numcolorbufs`, `allowbufblending`, `depthformat`, `cullface`, `overridemat`, `polygonoffset`, `polygonoffsetfactor`, `polygonoffsetunits`, `overdraw`, `overdrawlimit`, `cropleft`, `cropleftunit(pixels|fraction|fractionaspect)`, `cropright`, `croprightunit(pixels|fraction|fractionaspect)`, `cropbottom`, `cropbottomunit(pixels|fraction|fractionaspect)`, `croptop`, `croptopunit(pixels|fraction|fractionaspect)`, `vec`, `vec0name`, `vec0value`, `uni0name`, `sampler`, `sampler0name`, `sampler0top`, `sampler0extendu(hold|zero|repeat|mirror)`, `sampler0extendv(hold|zero|repeat|mirror)`, `sampler0extendw(hold|zero|repeat|mirror)`, `sampler0filter(nearest|linear|mipmaplinear)`, `sampler0anisotropy(off|2x|4x|8x|16x)`, `image`, `image0name`, `image0arraylength`, `image0res`, `image0format(useoutput|rgba8fixed|srgba8fixed|rgba16float|rgba32float|_separator_|rgb10a2fixed|rgba16fixed|rgba11float|mono8fixed|mono16fixed|mono16float|mono32float|rg8fixed|rg16fixed|rg16float|rg32float|a8fixed|a16fixed|a16float|a32float|monoalpha8fixed|monoalpha16fixed|monoalpha16float|monoalpha32float)`, `image0type(texture2d|texture2darray|texture3d|texturecube)`, `image0depth`, `image0access(writeonly|readwrite)`

### Text DAT — `text`
The Text DAT lets you edit free-form, multi-line ASCII text.

### Parameter Execute DAT — `parexec`
The Parameter Execute DAT runs a script when a parameter of any operator changes state.

### Execute DAT — `execute`
The Execute DAT lets you edit scripts and run them based on conditions.

### OP Execute DAT — `opexec`
The OP Execute DAT runs a script when the state of an operator changes.

### Base COMP — `base`
The Base Component has no panel parameters and no 3D object parameters.

### Container COMP — `container`
The Container Component groups together any number of button, slider, field, container and other Panel Components to build an interface.

### Geometry COMP — `geo`
The Geometry Component is a 3D surface that you see and render in TouchDesigner with a Render TOP.

### Camera COMP — `cam`
The Camera Component is a 3D object that acts like real-world cameras.

### Line MAT — `lineMAT`
The Line MAT renders 3D line segments, dots and vectors.
Params: `depthinterpolationmodel(scurve|inversedistance)`, `inversedistanceexponent`, `distancenear`, `distancefar`, `widthnear`, `widthfar`, `widthaffectedbyfov`, `widthbias`, `widthsteepness`, `widthlinearize`, `colorbias`, `colorsteepness`, `colorlinearize`, `liftdirection(alongcamerazaxis|alongnormal|towardcamera)`, `liftscale`, `numptsincircle`, `drawlines`, `linejointtype(round|miter|bevel)`, `miterthreshold`, `linestartcaptype(round|square|triangle|arrow|none)`, `lineendcaptype(round|square|triangle|arrow|none)`, `linenearcolor`, `linenearalpha`, `specifylinefarcolor`, `linefarcolor`, `linefaralpha`, `drawpoints`, `pointtype(circle|sphere|circlesprite|square|cone)`, `pointsizemultiplier`, `pointnearcolor`, `pointnearalpha`, `specifypointfarcolor`, `pointfarcolor`, `pointfaralpha`, `pointliftdirection(towardcamera|alongnormal)`, `pointliftscale`, `drawvectors`, `scale`, `vectorstartcaptype(round|square|triangle|arrow|none)`, `vectorendcaptype(round|square|triangle|arrow|none)`, `vectortaperstrength`, `vectornearcolor`, `vectornearalpha`, `specifyvectorfarcolor`, `vectorfarcolor`, `vectorfaralpha`, `roundwidth`, `roundheight`, `squarewidth`, `squareheight`, `trianglewidth`, `triangleheight`, `arrowwidth`, `arrowheight`, `arrowtaillength`, `endcapwidthmultiplier`, `endcapheightmultiplier`, `startcappullback`, `endcappullback`, `lineposatt`, `linewidthatt`, `linecoloratt`, `pointposatt`, `pointsizeatt`, `pointcoloratt`, `vectoratttype(sopattrib|instanceattribsop|instanceattribworld)`, `vectoratt(N|P|Cd|uv)`, `vectorcusattribidx`

### Info CHOP — `info`
The Info CHOP gives you extra information about a node.

### POP to CHOP — `poptoCHOP`
POP to CHOP converts POP attributes to CHOP channels.
Params: `active`, `pop`, `downloadtype(immediate|nextframe)`, `extract(points|vertices|primitives)`, `thinoutrange`, `thinrangestart`, `thinrangelength`, `thinstep`, `thinrandom`, `thinrandomseed`, `nameformat(basic|precise)`, `typesuffix`, `attribscope`, `renscope`, `group`, `invertgroup`, `rate`

### POP to DAT — `poptoDAT`
The POP to DAT converts, using the Extract menu, a POP's points or primitives to a table of points (one row per point), or a table of primitives (one row per primitive), or a table of vertices (one row per vertex).
Params: `active`, `pop`, `downloadtype(immediate|nextframe)`, `extract(points|vertices|primitives|detail|dimensions)`, `attrib`, `primitivetype`, `transpose`, `thinoutrange`, `thinrangestart`, `thinrangelength`, `thinstep`, `thinrandom`, `thinrandomseed`, `group`, `invertgroup`, `grpcol(none|onecolumn|colpergrp)`

