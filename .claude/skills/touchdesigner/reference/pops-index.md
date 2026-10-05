# Index des POPs (TouchDesigner 2025.3x)

Généré depuis docs.derivative.ca par `scripts/td_doc.py index`. Pour chaque opérateur : nom, `opType` Python (pour `comp.create()`), première phrase de la doc, noms Python des paramètres. Entre parenthèses : valeurs de menu (`par.menuNames`).

### Accumulate POP — `accumulatePOP`
The Accumulate POP takes an attribute from the input, and creates a new attribute whose values in each point are the sum of the values in the input attribute of the previous points.
Params: `attrclass(point|vertex|primitive)`, `inputattrscope`, `scantype(inclusive|exclusive)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Alembic In POP — `alembicPOP`
The Alembic In POP loads and plays back [http://www.alembic.io/ Alembic] file geometry and multi-frame sequences.
Params: `file`, `objectpath(*|/box_object1/color1)`, `loadtype(immediate|nextframe)`, `xform(none|staticlocalxform|staticworldxform|dynamicxform)`, `interp`, `loadfile`, `shiftanimationstart`, `sampleratemode(filefps|custom)`, `samplerate`, `playmode(lockedtotimeline|specifyindex|sequential)`, `initialize`, `start`, `cue`, `cuepoint`, `play`, `index`, `speed`, `trim`, `tstart`, `tend`, `textendleft(hold|cycle|mirror)`, `textendright(hold|cycle|mirror)`

### Alembic Out POP — `alembicoutPOP`
The Alembic Out POP writes POP contents to an Alembic .abc file.
Params: `input`, `input0pop`, `input0objname`, `input0idname`, `input0velname`, `input0ptattrname`, `input0vertattrname`, `input0primattrname`, `uniquesuff`, `n`, `leadingzerosdigits`, `file`, `fps`, `limitlength`, `length`, `record`, `recordpulse`, `pause`, `addframe`, `maxactive`, `includeprim`, `texcoordattrib`, `unchangedtopology`, `abcfps`, `abc3dtex`

### Analyze POP — `analyzePOP`
The Analyze POP analyzes any point, vertex or primitive attributes of a POP, and outputs a single point containing the resulting statistics.
Params: `attrclass(point|vertex|primitive)`, `group`, `numgroupelements`, `inputattrs(*)`, `appendattrname`, `combine(off|add|sub|mul|div|avg|min|max|len)`, `avg`, `centroid`, `min`, `max`, `size`, `minindex`, `maxindex`, `sum`, `rmspower`, `numpointsvertsprims`, `numprimsbatch`, `dimension`, `pattrvals(none|avg|centroid|min|max)`

### Attribute Combine POP — `filter`
The Attribute Combine POP takes multiple POP inputs and lets you choose attributes from each input by name or by pattern matching, and send the attributes to the output.
Params: `attrclass(point|vertex|primitive)`, `lengthmismatchnotif`, `duplicateattrs(autorename|keepfirst|keeplast|replaceattribs)`, `input`, `input0pop`, `input0attrs(*)`, `input0renameto`

### Attribute Convert POP — `attributeconvertPOP`
The Attribute Convert POP lets you copy a POP attribute from one "attribute class" to another.
Params: `convertop(none|pointtovert|verttopoint|pointtoprim|primtopoint|verttoprim|primtovert)`, `inputattrs(*)`, `newattrs`, `deleteorig`, `notificationifexists(ignore|warning|error)`, `overrideifexists`

### Attribute POP — `attributePOP`
The Attribute POP lets you:
Params: `attrclass(point|vertex|primitive)`, `group`, `notificationifexists(ignore|warning|error)`, `overrideifexists`, `premultcolor`, `attr`, `attr0name`, `attr0customname`, `attr0type`, `attr0numcomps(1|2|3|4)`, `attr0isarray`, `attr0arraysize`, `attr0value`, `matattr`, `matattr0name`, `matattr0numrows`, `matattr0numcols`, `matattr0isarray`, `matattr0qualifier(none|transformMatrix)`, `ren`, `ren0from`, `ren0to`, `dup`, `dup0name`, `dup0new`, `deletepoint(*)`, `deletevert(*)`, `deleteprim(*)`

### Blend POP — `blendPOP`
The Blend POP lets you blend together an attribute that occurs in all of it input POPs, such as the P attribute of all the inputs.
Params: `blendtype(off|avg|add|mul|min|max|differencing|proportional|proportionalsmoothed)`, `lengthmismatchnotif`, `weightchop`, `pointattrscope(*)`, `primattrscope(*)`, `vertattrscope(*)`, `input`, `input0pop`, `input0weight`, `map`, `map0op`, `map0element`, `map0parm(input0weight)`, `map0combineop(set|mult|add)`

### Box POP — `boxPOP`
The Box POP creates 6-sided boxes.
Params: `surftype(none|points|triangles|quads)`, `uniquepoints`, `modifybounds`, `size`, `roundcorners`, `cornerradius`, `depth`, `anchoru`, `anchorv`, `anchorw`, `t`, `r`, `scale`, `normal(none|pointNormals|vertNormals|primNormals)`, `texture(none|pointNormals|vertNormals)`, `texmethod(boxinside|faceinside|cubemapinside|boxoutside|faceoutside|cubemapoutside)`, `extenduv`, `color(none|pointColor|vertColor|primColor)`

### CHOP to POP — `choptoPOP`
The CHOP to POP takes CHOP channels and lets you convert them to attributes of a POP.
Params: `chop`, `surftype(none|points|linestrip|lines)`, `overridenumpoints`, `interpolate`, `specifypos`, `startpos`, `endpos`, `closed`, `chanssel(spec|precisenamessuffix|precisenames)`, `chanscope`, `attrscope(P|P(0)|P(1)|P(2)|Color|Color(0)|Color(1)|Color(2)|Color(3)|N|N(0)|N(1)|N(2)|Tex|Tex(0)|Tex(1)|Tex(2))`, `attrs`, `attr`, `attr0chanscope`, `attr0name`, `attr0type`, `attr0defaultval`

### CPlusPlus POP — `cplusplusPOP`
The CPlusPlus POP allows you to make custom POP operators by writing your own plugin using C++.
Params: `plugin`, `reinit`, `unloadplugin`

### Cache Blend POP — `cacheblendPOP`
The Cache Blend POP takes a reference to a Cache POP and outputs a blend of its cached data sets based on a Cache Index parameter and the Cache Weight parameter of the each of the sequential blocks.
Params: `cachepop`, `chop`, `indexchan`, `indexchanunit(indices|frames|seconds)`, `weightchan`, `interp`, `cache`, `cache0index`, `cache0weight`

### Cache POP — `cachePOP`
The Cache POP receives POP data every frame in its input and holds the most recent frames of data (up to Cache Size) in GPU memory.
Params: `active`, `alwayscook`, `cachesize`, `step`, `outputindex`, `interp`, `reset`

### Cache Select POP — `cacheselectPOP`
The Cache Select POP takes a reference to a Cache POP and outputs one of its cached data sets based on the Cache Index parameter.
Params: `cachepop`, `index`, `interp`

### Circle POP — `circlePOP`
The Circle POP creates a number of points in a circle, ellipse or arc, and optionally connects them as a line strip, a set of triangles, separate 2-point lines, or unconnected as point primitives.
Params: `connectivity(none|points|surface|linestrip|lines)`, `orient(xy|yz|zx)`, `modifybounds`, `rad`, `divs`, `closed`, `angle`, `anchoru`, `anchorv`, `t`, `r`, `scale`, `normal(none|pointNormals)`, `normaldirection(default|radial|tangent)`, `tangent(none|pointNormals)`, `tangentdirection(radial|Tangent)`, `texture(none|pointNormals|vertNormals)`

### Connectivity POP — `connectivityPOP`
The Connectivity POP is intended to re-connect the input's points with a set of new primitives, similar to what the Grid POP or Torus POP does to their sets of points.
Params: `surftype(none|points|lines|linestrips|linestripperplane|zigzagperplane|spiralperplane|triangles|alttriangles|quads)`, `firstdim`, `seconddim`, `firstdimclosed`, `seconddimclosed`, `reorderpoints`

### Convert POP — `convertPOP`
The Convert POP is a general utility that keeps the points of the input, but reconnects them in various ways as primitives.
Params: `convert(none|deleteprims|topointprims|linestripstolines|tolinestrips|quadstotriangles|closelinestrips|openlinestrips|reversevertorder|uniquereorderpoints|cpureadback)`

### Copy POP — `copyPOP`
The Copy POP makes copies of its input using (1) the Number of Copies parameter that specifies the number of copies to make with the transform applied to each copy, and (2) a second-input Template POP where a copy is placed at each point of the template.
Params: `ncy`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`, `scale`, `copyid`, `lookat`, `upvector`, `forwarddir(posx|negx|posy|negy|posz|negz)`, `vlength`, `dimension(morethanone|always)`, `dotemplatematrix`, `templatexord(srt|str|rst|rts|tsr|trs)`, `templaterord(xyz|xzy|yxz|yzx|zxy|zyx)`, `dotemplatetranslate`, `dotemplaterotate`, `dotemplatescale`, `dotemplatepivot`, `dotemplaterotateto`, `templaterottoord(rottoxform|rotaterotto|rottorotate)`, `instanceforward(posx|negx|posy|negy|posz|negz)`, `vecattr`, `upvectoratype(attribute|constant)`, `upattr`, `upconstant`, `templateid`, `doattr`, `templateattr`, `templateattr0op(copy|mul|add|subtract)`, `templateattr0dest(point|vertex|primitive)`, `templateattr0names(*)`

### Curve POP — `curvePOP`
The Curve POP is used to generate a curve in XY (Z=0) that can be used as a lookup curve for a Lookup Attribute POP or elsewhere.
Params: `totallength`, `outputcurve(points|linestrip|colorstrip)`, `normalizeu`, `symmetric`, `parsize(1|2|3|4)`, `startu`, `seg`, `seg0type(constant|linear|easein|easeout|easeinout|bezier)`, `seg0u`, `seg0specstartval`, `seg0startval`, `seg0endval`, `seg0alpha`, `seg0beta`, `seg0slopein`, `seg0slopeout`, `applylookup`, `lookupindexattr`, `fromlow`, `tolow`, `extendleft`, `lookup`, `lookup0multiply`, `lookup0add`, `lookup0combineop(set|add|mult|min|max)`, `lookup0outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `lookup0overrideautoattr`, `lookup0attrtype(float|double|int|uint|dir|ddir)`, `lookup0attrnumcomps(1|2|3|4)`, `lookup0attrdefaultval`, `extendright(hold|slope|cycle|mirror)`

### DAT to POP — `dattoPOP`
The DAT to POP converts DAT tables into POP geometry.
Params: `pointsdat`, `createpointprim`, `cnvrtallpointcols`, `pointgroupnamescol`, `attr`, `attr0columnstype(name|number)`, `attr0columns`, `attr0outputscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth|Tex.i01)`, `attr0overrideauto`, `attr0type`, `attr0isarray`, `attr0arraysize`, `primitivesdat`, `primtype(fromcolumn|points|lines|triangles|quads|linestrips)`, `primtypecol`, `primvertices`, `cnvrtallprimcols`, `primgroupnamescol`, `primattr`, `primattr0columnstype(name|number)`, `primattr0columns`, `primattr0outputscope(N|Color|Color.rgb|Tex|Tex.i01|PointScale|LineWidth)`, `primattr0overrideauto`, `primattr0type`, `primattr0isarray`, `verticesdat`, `cnvrtallvertcols`, `vertattr`, `vertattr0columnstype(name|number)`, `vertattr0columns`, `vertattr0outputscope(N|Color|Color.rgb|Tex|Tex.i01|PointScale|LineWidth)`, `vertattr0overrideauto`, `vertattr0type`, `vertattr0isarray`, `detailsdat`, `dimensionsdat`, `dimcol`

### DMX Fixture POP — `dmxfixturePOP`
The DMX Fixture POP constructs DMX universes from a POP input, and is used in conjunction with a DMX Out POP to send DMX to a device.
Params: `active`, `autolayout`, `routingtable`, `net`, `subnet`, `universe`, `channel`, `changap`, `quantizeuni(off|fixture|component)`, `dmxchan`, `dmxchan0name`, `dmxchan0valuetype(point|primitive)`, `dmxchan0valuesource(constant|attribute)`, `dmxchan0group`, `dmxchan0numcomps(1|2|3|4)`, `dmxchan0value`, `dmxchan0attr`, `dmxchan0valueres(b8|b16|b24|b32)`, `dmxchan0normalized`, `dmxchan0merge`, `dmxchan0interleavebytes`

### DMX Out POP — `dmxoutPOP`
The DMX Out POP can send to DMX, Art-Net, sACN, [https://www.colorkinetics.com/global/learn/optics-matter KiNET], or FTDI devices.
Params: `active`, `interface(serial|enttecusbpro|enttecusbpromk2|artnet|sacn|kinet)`, `rate`, `fixture`, `fixture0active`, `fixture0pop`, `serialport(com3)`, `dmxkingport(default)`, `device(*)`, `multicast`, `netaddress`, `localaddress(192.168.178.150|10.2.0.2)`, `localport`, `customport`, `netport`, `priority`, `sendartsync`, `artsynctimeout`, `cid`, `source`, `kinetversion(v1|v2)`, `customkinetport`, `kinetport`, `routingtable`, `usemultipliers`, `multiplier`, `multiplier0dmxchannels`, `multiplier0value`

### Delete POP — `deletePOP`
The Delete POP removes (or keeps) points or primitives using 5 methods found on the Attribute, Thin, Pattern, Group and Bounding pages.
Params: `invert(dele|keep|delete)`, `entity(primitive|point)`, `linestripbehavior(delpointoflinestrip|splitlinestrip|dellinestrip)`, `cpureadback`, `attr`, `attr0combine(and|or|xor|nand|nor)`, `attr0inattr`, `attr0func(lt|lte|gt|gte|eq|ne)`, `attr0value`, `attr0invert`, `thinenabled`, `thinoutrange`, `thinrangestart`, `thinrangelength`, `thinstep`, `thinrandom`, `thinrandomseed`, `thininvert`, `pattern`, `pattern0combine(and|or|xor|nand|nor)`, `pattern0pattern(*|0-50|0-50:2|[*]|[*:4]|[0-49]|[0-49:2]|^[*:4]|[*:5:7]|[1,4,9]|1 4 [7-9])`, `pattern0invert`, `group`, `group0combine(and|or|xor|nand|nor)`, `group0name`, `group0invert`, `bound`, `bound0combine(and|or|xor|nand|nor)`, `bound0inattr`, `bound0type(boundingbox|boundingsphere)`, `bound0translate`, `bound0rotate`, `bound0scale`, `bound0invert`

### Dimension POP — `dimensionPOP`
The Dimension POP can alter the dimensions of a POP.
Params: `mode(reorderdims|setdims)`, `dimorder`, `dim`, `dim0number`

### Extrude POP — `extrudePOP`
The Extrude POP is a gives apparent "thickness" to line strips, triangles or quads.
Params: `group`, `axis(normal|x|y|z)`, `distance`, `taper`, `peredge`, `maxprimsperpoint`, `normal(none|pointNormals|vertNormals)`, `cpureadback`, `map`, `map0op`, `map0element`, `map0parm(distance|taper)`, `map0combineop(set|mult|add)`

### Facet POP — `facetPOP`
The Facet POP does operations to make points ve shared between multiple primitives, or create new points so that the points are not shared.
Params: `group`, `operation(none|unique|cusp|conspoints)`, `angle`, `dist`, `maxtries`, `removedegenerate`, `removeunusedpoints`, `technique(bruteforce|sharedmemory|spatialgrid|spatialgridpervoxel)`, `gridres`, `specifybbox`, `bbox`, `computenormals`, `cpureadback`

### Feedback POP — `feedbackPOP`
The Feedback POP receives the output of another POP called the “target” POP, from the previous frame, i.e.
Params: `targetpop`, `initializepulse`, `startpulse`, `play`, `preroll`, `donepulse`, `usememlimit`, `inputmul`

### Field POP — `fieldPOP`
The Field POP adds a Weight attribute that determines how much each point is within a 3D shape.
Params: `attrclass(point|vertex|primitive)`, `fieldattrscope`, `specpop`, `mode(sphere|box|torus|tubeinfinite|tubecapped|tuberounded|capsule|xplane|yplane|zplane|parabola|lineprojection)`, `size`, `rad`, `height`, `roundness`, `pointa`, `pointb`, `strength`, `exponent`, `transitionrange`, `transitionalign`, `transitiontype(linear|smoothstep|easeinout)`, `absvalue`, `invert`, `torange`, `deletezeros`, `linestripbehavior(delpointoflinestrip|splitlinestrip|dellinestrip)`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`, `weight`, `signeddistance`, `perfieldweights`, `perfielddistances`, `combineop(none|add|mult)`, `combineentity(weight|signeddistance)`, `combineattr`, `combineoutputattr(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `combineoverrideautoattr`, `combineattrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `combineattrnumcomps(1|2|3|4)`, `combineattrdefaultval`

### File In POP — `fileinPOP`
The File In POP reads a file and converts it into a POP in GPU memory.
Params: `file`, `flipfacing`, `refresh`, `inputcolorspace(automatic|srgb|srgblinear|rec601ntsc|rec709|rec2020|rec2020st2084pq|rec2020hlg|dcip3|dcip3d60|displayp3d65|displayp3d65linear|aces2065-1|acescg|acesproxy|passthrough)`, `inputreferencewhite(default|sdr|hdr|ui)`

### File Out POP — `fileoutPOP`
The File Out POP allows you to write out POP contents to different file types.
Params: `type(file|filesequence)`, `objectfiletype(obj|exr|ply|spz|e57)`, `uniquesuff`, `n`, `leadingzerosdigits`, `file`, `fps`, `limitlength`, `length`, `record`, `recordpulse`, `pause`, `addframe`, `maxactive`, `includeprim`, `texcoordattrib`, `outputcolorspace(srgb|srgblinear|rec601ntsc|rec709|rec2020|rec2020st2084pq|rec2020hlg|dcip3|dcip3d60|displayp3d65|aces2065-1|acescg|acesproxy|passthrough)`, `attr`, `attr0name`, `attr0fields`

### Force Radial POP — `forceradialPOP`
The Force Radial POP is used in a Particle POP loop and outputs a float3 attribute named PartForce that sums a set of forces defined in the Force Radial POP.
Params: `specpop`, `pos`, `direction`, `radial`, `radialstrength`, `axial`, `axialr`, `axialstrength`, `spiral`, `spiralr`, `spiralstrength`, `planar`, `planarexponent`, `planarstrength`, `falloff(scurve|power|inversedistance|none)`, `falloffsteepness`, `falloffbias`, `falloffexponent`, `falloffradius`, `falloffplateau`, `fallofflimitrange`, `globforce`, `globforcemult`, `windspeed`, `windspeedmult`, `map`, `map0op`, `map0element`, `map0parm(globforce|globforcex|globforcey|globforcez|globforcemult|windspeed|windspeedx|windspeedy|windspeedz|windspeedmult)`, `map0combineop(set|mult|add)`

### GLSL Advanced POP — `glsladvancedPOP`
Refer to the Write GLSL POPs article for more info on using this POP.
Params: `computedat`, `shaderdispatchmode(single|perprimbatch)`, `numelems`, `numelemspop`, `numelemsclass`, `workgroupsize`, `dispatchsize`, `numthreadsbatchmode(inputvert|inputprim|outputvert|outputprim)`, `ptoutputattrs(*)`, `primoutputattrs(*)`, `vertoutputattrs(*)`, `outputaccess(writeonly|readwrite)`, `initoutputattrs`, `prevpassoutput`, `npasses`, `input`, `input0pops`, `simplexnoise(performance|quality)`, `numthreadsmode(inputpoint|inputvert|inputprim|outputpoint|outputvert|outputprim|numelems|numelemsattrib|manual)`, `render`, `maxpointsmode`, `pointcountinfo(input|fromattrs|fromparams)`, `pointcountmode(input|zero|set)`, `pointcountpop`, `pointcountclass`, `maxtrianglesmode`, `maxquadsmode`, `maxlinestripsmode`, `maxlsvertsmode`, `maxlinesmode`, `maxpointprimsmode`, `lsinfoupdate(auto|zero|manual)`, `lsinfopop`, `lsinfoclass`, `lsindexpop`, `lsindexclass`, `lsmaxvertsoverride`, `initoutputprims(none|copy|zero)`, `topoinfo(input|fromattrs|fromparams)`, `topoinfopop`, `topoinfoclass(point|vertex|primitive)`, `trianglecountmode`, `quadcountmode`, `linestripcountmode`, `lsvertcountmode`, `linecountmode`, `pointprimcountmode`, `extraout`, `extraout0name`, `extraout0pop`, `extraout0ptattrs`, `extraout0primattrs`, `extraout0vertattrs`, `extraout0outputaccess(writeonly|readwrite)`, `extraout0prevpassoutput`, `extraout0copyinputattrs`, `attr`, `attr0class(point|vertex|primitive)`, `attr0name`, `attr0type`, `attr0isarray`, `attr0arraysize`, `attr0value`, `matattr`, `matattr0class(point|vertex|primitive)`, `matattr0name`, `matattr0numrows`, `matattr0numcols`, `matattr0isarray`, `matattr0arraysize`, `matattr0qualifier(none|transformMatrix)`, `premultcolor`, `color`, `color0name`, `color0rgb`, `color0alpha`, `vec`, `vec0name`, `vec0type(float|vec2|vec3|vec4|double|dvec2|dvec3|dvec4|int|ivec2|ivec3|ivec4|uint|uvec2|uvec3|uvec4)`, `vec0value`, `sampler`, `sampler0name`, `sampler0top`, `sampler0extendu(hold|zero|repeat|mirror)`, `sampler0extendv(hold|zero|repeat|mirror)`, `sampler0extendw(hold|zero|repeat|mirror)`, `sampler0filter(nearest|linear)`, `array`, `array0name`, `array0type(float|vec2|vec3|vec4)`, `array0chop`, `array0arraytype(uniformarray|texturebuffer)`, `matrix`, `matrix0name`, `matrix0value`, `tempbuffer`, `tempbuffer0name`, `tempbuffer0initval`, `const`, `const0name`, `const0value`

### GLSL Copy POP — `glslcopyPOP`
The GLSL Copy POP lets you make copies of the geometry of the first input POP, and apply custom GLSL code to each copy.
Params: `ncy`, `ptcomputedat`, `ptoutputattrs(*)`, `vertcomputemethod(default|custom)`, `vertcomputedat`, `vertoutputattrs(*)`, `primcomputemethod(default|custom)`, `primcomputedat`, `primoutputattrs(*)`, `dimension(morethanone|always)`, `simplexnoise(performance|quality)`, `attr`, `attr0class(point|vertex|primitive)`, `attr0name`, `attr0type`, `attr0isarray`, `attr0arraysize`, `matattr`, `matattr0class(point|vertex|primitive)`, `matattr0name`, `matattr0numrows`, `matattr0numcols`, `matattr0isarray`, `matattr0arraysize`, `matattr0qualifier(none|transformMatrix)`, `premultcolor`, `color`, `color0name`, `color0rgb`, `color0alpha`, `vec`, `vec0name`, `vec0type(float|vec2|vec3|vec4|double|dvec2|dvec3|dvec4|int|ivec2|ivec3|ivec4|uint|uvec2|uvec3|uvec4)`, `vec0value`, `sampler`, `sampler0name`, `sampler0top`, `sampler0extendu(hold|zero|repeat|mirror)`, `sampler0extendv(hold|zero|repeat|mirror)`, `sampler0extendw(hold|zero|repeat|mirror)`, `sampler0filter(nearest|linear)`, `array`, `array0name`, `array0type(float|vec2|vec3|vec4)`, `array0chop`, `array0arraytype(uniformarray|texturebuffer)`, `matrix`, `matrix0name`, `matrix0value`, `tempbuffer`, `tempbuffer0name`, `tempbuffer0initval`, `const`, `const0name`, `const0value`, `buffer`, `buffer0pop`, `buffer0attrclass(point|vertex|primitive)`, `buffer0attr`, `buffer0name`

### GLSL Create POP — `glslcreatePOP`
This POP is deprecated and will be removed.
Params: `computedat`, `primtype(triangle|quads|lines|points)`, `maxprims`, `indirect`, `numthreadsmode(auto|manual)`, `workgroupsize`, `dispatchsize`, `pops`, `vec`, `vec0name`, `vec0type(float|vec2|vec3|vec4|double|dvec2|dvec3|dvec4|int|ivec2|ivec3|ivec4|uint|uvec2|uvec3|uvec4)`, `vec0value`, `sampler`, `sampler0name`, `sampler0top`, `sampler0extendu(hold|zero|repeat|mirror)`, `sampler0extendv(hold|zero|repeat|mirror)`, `sampler0extendw(hold|zero|repeat|mirror)`, `sampler0filter(nearest|linear)`, `array`, `array0name`, `array0type(float|vec2|vec3|vec4)`, `array0chop`, `matrix`, `matrix0name`, `matrix0value`, `ac`, `ac0name`, `ac0singlevalue`, `const`, `const0name`, `const0value`

### GLSL POP — `glslPOP`
This POP allows you to modify input attributes with GLSL.
Params: `computedat`, `attrclass(point|vertex|primitive)`, `numthreadsmode(auto|otherinputelements|numelems|numelemsattrib|manual)`, `threadsinput`, `numelems`, `numelemspop`, `numelemsclass`, `workgroupsize`, `dispatchsize`, `outputattrs(*)`, `outputaccess(writeonly|readwrite)`, `initoutputattrs`, `prevpassoutput`, `npasses`, `input`, `input0pops`, `simplexnoise(performance|quality)`, `attr`, `attr0name`, `attr0type`, `attr0isarray`, `attr0arraysize`, `attr0value`, `matattr`, `matattr0name`, `matattr0numrows`, `matattr0numcols`, `matattr0isarray`, `matattr0arraysize`, `matattr0qualifier(none|transformMatrix)`, `premultcolor`, `color`, `color0name`, `color0rgb`, `color0alpha`, `vec`, `vec0name`, `vec0type(float|vec2|vec3|vec4|double|dvec2|dvec3|dvec4|int|ivec2|ivec3|ivec4|uint|uvec2|uvec3|uvec4)`, `vec0value`, `sampler`, `sampler0name`, `sampler0top`, `sampler0extendu(hold|zero|repeat|mirror)`, `sampler0extendv(hold|zero|repeat|mirror)`, `sampler0extendw(hold|zero|repeat|mirror)`, `sampler0filter(nearest|linear)`, `array`, `array0name`, `array0type(float|vec2|vec3|vec4)`, `array0chop`, `array0arraytype(uniformarray|texturebuffer)`, `matrix`, `matrix0name`, `matrix0value`, `tempbuffer`, `tempbuffer0name`, `tempbuffer0initval`, `const`, `const0name`, `const0value`, `asname`, `colpop`, `buildflag(fastbuild|fasttrace)`, `opaquecolgeo`

### GLSL Select POP — `glslselectPOP`
The GLSL Select POP allows you to select one of the Extra Output POPs that can be made available with a GLSL Advanced POP.
Params: `pop`, `name`

### Grid POP — `gridPOP`
The Grid POP creates rows and columns of points in a plane, and optionally creates multiple slices of points resulting in a 3D grid.
Params: `surftype(none|points|lines|linestrips|triangles|alttriangles|quads)`, `modifybounds`, `size`, `cols`, `rows`, `slices`, `uniquepoints`, `seed`, `random`, `randomsizefit`, `line`, `plane`, `anchoru`, `anchorv`, `anchorw`, `t`, `r`, `scale`, `normal(none|pointNormals|vertNormals|primNormals)`, `texture(none|point|vert)`, `dimension(morethanone|rowscolsalways|rowscolsslicesalways)`

### Group POP — `groupPOP`
The Group POP lets you put sets of points or primitives into named groups so that you can then use the groups in other POPs, such as the Transform POP to affect only the elements of particular groups.
Params: `grname`, `entity(primitive|point)`, `debugcolor`, `attr`, `attr0combine(and|or|xor|nand|nor)`, `attr0inattr`, `attr0func(lt|lte|gt|gte|eq|ne)`, `attr0value`, `attr0invert`, `thinenabled`, `thinoutrange`, `thinrangestart`, `thinrangelength`, `thinstep`, `thinrandom`, `thinrandomseed`, `thininvert`, `pattern`, `pattern0combine(and|or|xor|nand|nor)`, `pattern0pattern(*|*:4|0-50|0-50:2)`, `pattern0invert`, `group`, `group0combine(and|or|xor|nand|nor)`, `group0name`, `group0invert`, `bound`, `bound0combine(and|or|xor|nand|nor)`, `bound0inattr`, `bound0type(usebbox|usebsphere)`, `bound0translate`, `bound0rotate`, `bound0scale`, `bound0invert`, `cnvttype(topoint|toprim)`, `cnvtgroup`, `cnvtname`, `preserve`, `oldname`, `newname`, `deletename`

### Histogram POP — `histogramPOP`
The Histogram POP takes an attribute from its input, creates an output with one attribute (Count attribute) and a specified number of points (Number of Bins parameter), and for each input point, adds 1 to one of the bins.
Params: `attrclass(point|vertex|primitive)`, `inputattrscope`, `useinputrange`, `inputrange`, `outputbinval`, `quantize(floor|round|ceiling)`, `outsiderange(clamp|discard|extrabins)`, `numbins`, `countattr`

### Import Select POP — `importselectPOP`
The Import Select POP is used to import and load the geometry types primitives defined in USD COMP and FBX COMP.
Params: `parent`, `geometry`, `reload`, `blendshape`, `comptang`, `useparentanim`, `shiftanimationstart`, `sampleratemode(filefps|custom)`, `samplerate`, `playmode(lockedtotimeline|specifyindex|sequential)`, `initialize`, `start`, `cue`, `cuepoint`, `play`, `index`, `speed`, `trim`, `tstart`, `tend`, `textendleft(hold|cycle|mirror)`, `textendright(hold|cycle|mirror)`

### In POP — `inPOP`
The In POP gets data from a POP that is connected to one of the inputs of the In POP's parent component.
Params: `label`, `connectorder`

### Limit POP — `limitPOP`
The Limit POP takes any attribute and lets you clamp to a lower-upper range, or takes values outside the range and loops them so they are withing the range, or similarly zig-zags the values within the range.
Params: `attrclass(point|vertex|primitive)`, `group`, `inputattrscope`, `parsize(1|2|3|4)`, `mintype(off|clamp|loop|zigzag|off|clamp|loop|zigzag)`, `maxtype(off|clamp|loop|zigzag|off|clamp|loop|zigzag)`, `min`, `max`, `positive`, `castto(auto|float|int)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `quantize(off|floor|round|ceiling|gt0|gteq0|eq0|neq0|lteq0|lt0|off|floor|round|ceiling|gt0|gteq0|eq0|neq0|lteq0|lt0)`, `quantstep`, `quantoffset`

### Line Break POP — `linebreakPOP`
The Line Break POP creates new line strips from the points and line strips of its input.
Params: `connecmode(noconnec|onelinestrip|inputlinestrips)`, `uselinebreak`, `uselinestripindex`, `useinputlinebreaks`, `everyn`, `n`, `bydistancethreshold`, `distancethreshold`, `distancethresholdattr`, `outputlinebreakattr`, `outputlines`, `linetype(linestrip|lines)`, `cpureadback`

### Line Divide POP — `linedividePOP`
The Line Divide POP takes any set of line strips, and for each it generates a new line strip that is subdivided using various interpolation methods.
Params: `divmethod(none|linestrip|segment|dist|curvature)`, `divs`, `mindist`, `maxdist`, `minmaxbias`, `byedge`, `addctrlpointattr`, `maxverts`, `interpmethodpersegment`, `interpmethod(linear|cardinal|bspline|cubicbeziertang|cubicbezier|quadraticbezier)`, `useweight`, `usetanin`, `usetanout`, `usetaninconst`, `clamped`, `tension`, `resamplemethod(none|linestrip|dist|keyframes)`, `resampledivs`, `indvarattr`, `indvarstep`, `resamplemaxverts`, `maxtries`, `rmvunusedpts`, `resamplemaxdist`

### Line Metrics POP — `linemetricsPOP`
You can add metrics attributes to Line Strips.
Params: `attrclass(point|vertex)`, `dispnext`, `dispprev`, `distnext`, `distprev`, `dirnext`, `dirprev`, `tangent`, `curvature`, `angleperdist`, `continuousdir`, `maxneighbors`, `normal`, `binormal`, `quaternion`, `rotmat`, `transformmat`, `useinputorient`, `diststart`, `distend`, `diststartnorm`, `distendnorm`, `primlen`, `primlenprim`, `pointindex`, `numverts`, `vertindexnorm`, `linestripindex`, `lsindexnorm`

### Line POP — `linePOP`
The Line POP generates a line strip where you create a set of points using parameters, and then (optionally) subdivides each segment using various interpolation methods.
Params: `output(subdivlines|ctrlpoints)`, `multiplelinestrips`, `interpmethodpersegment`, `interpmethod(linear|cardinal|bspline|cubicbeziertang|cubicbezier|quadraticbezier)`, `tension`, `enableweights`, `enabletangent`, `enablepointrepeat`, `closed`, `premultcolor`, `attr`, `attr0name(custom|n|color|tex|pointscale|linewidth)`, `attr0customname`, `attr0type(float|double|int|uint|dir|ddir)`, `attr0numcomps(1|2|3|4)`, `attr0value`, `pt`, `pt0pos`, `pt1pos`, `divmethod(linestrip|segment|defpersegment|distseg)`, `divs`, `dist`, `addctrlpointattr`, `resamplemethod(none|linestrip|dist|keyframes)`, `resampledivs`, `resampledist`, `indvarattr(P(0))`, `indvarstep`, `resamplemaxverts`, `maxtries`

### Line Resample POP — `lineresamplePOP`
The Line Resample POP will take a set of line strips, and for each one, resample the line strip in one of four methods: number of Divisions per Line Strip, a specified Distance between Points, point separation based on the curvature of the line strip at each of the original points (By Curvature), an
Params: `resamplemethod(none|linestrip|dist|curvature|keyframes)`, `resampledivs`, `resamplemindist`, `resamplemaxdist`, `resampleminmaxbias`, `interpolation(linear|cardinal)`, `usectrlpoints`, `indvarattr`, `indvarstep`, `lsmaxverts`, `maxtries`, `rmvunusedpts`

### Line Smooth POP — `linesmoothPOP`
The Line Smooth POP smooths line strips by blending the positions of adjacent points along a line strip.
Params: `attrclass(point|vertex)`, `inputattrscope`, `prediv`, `maxdivdist`, `maxverts`, `filtermethod(dist|point)`, `filtertype(gaussian|box)`, `filterdist`, `filtersize`, `effect`, `endpointsfixed`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `resamplemethod(none|dist|curvature)`, `resamplemindist`, `resamplemaxdist`, `resampleminmaxbias`, `maxtries`, `map`, `map0op`, `map0element`, `map0parm(filterdist|filtersize)`, `map0combineop(set|mult|add)`

### Line Thick POP — `linethickPOP`
THis POP has been removed.
Params: `camera`, `cameraaspect`, `depthinterpolationmodel(scurve|inversedistance)`, `inversedistanceexponent`, `distancenear`, `distancefar`, `widthnear`, `widthfar`, `widthaffectedbyfov`, `widthbias`, `widthsteepness`, `widthlinearize`, `colorbias`, `colorsteepness`, `colorlinearize`, `liftdirection(towardcamera|alongnormal)`, `liftscale`, `numptsincircle`, `id`, `drawlines`, `linejointtype(round|miter|bevel)`, `miterthreshold`, `linestartcaptype(round|square|triangle|arrow|none)`, `lineendcaptype(round|square|triangle|arrow|none)`, `linenearcolor`, `linenearalpha`, `specifylinefarcolor`, `linefarcolor`, `linefaralpha`, `drawvectors`, `attribute(N|P|Color|uv)`, `scale`, `vectorstartcaptype(round|square|triangle|arrow|none)`, `vectorendcaptype(round|square|triangle|arrow|none)`, `vectortaperstrength`, `vectornearcolor`, `vectornearalpha`, `specifyvectorfarcolor`, `vectorfarcolor`, `vectorfaralpha`, `roundwidth`, `roundheight`, `squarewidth`, `squareheight`, `trianglewidth`, `triangleheight`, `arrowwidth`, `arrowheight`, `arrowtaillength`, `endcapwidthmultiplier`, `endcapheightmultiplier`, `startcappullback`, `endcappullback`

### Lookup Attribute POP — `lookupattributePOP`
The Lookup Attribute POP in its simplest form takes an attribute of the first input (the Lookup Index Attribute(s)) with values in the 0-1 range, and for each point of the first input, uses the value as an index into attributes of the second input (the Value Attributes of the lookup curve).
Params: `attrclass(point|vertex|primitive)`, `group`, `lookupindexattr`, `indexunit(normalized|pointindex)`, `cyclic`, `interpolate`, `indexfromlow`, `indextolow`, `extendleft`, `lookup`, `lookup0valueattr`, `lookup0fromlow`, `lookup0fromhigh`, `lookup0tolow`, `lookup0tohigh`, `lookup0outputattrscope(P|N|Color|Color.i012|Tex|PointScale|LineWidth|Color.rgb)`

### Lookup Channel POP — `lookupchannelPOP`
The Lookup Channel POP in its simplest form takes an attribute (the Lookup Attribute) with values in the 0-1 range and for each point, uses the attribute value as an index into the channels of a CHOP, pulling one interpolated value for each channel, and placing those values into POP attributes.
Params: `attrclass(point|vertex|primitive)`, `group`, `chop`, `lookupindexattr`, `indexunit(normalized|sampleindex)`, `cyclic`, `interpolate`, `extendleft`, `lookup`, `lookup0chanscope`, `lookup0fromlow`, `lookup0fromhigh`, `lookup0tolow`, `lookup0tohigh`, `lookup0outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `lookup0overrideautoattr`, `lookup0attrtype(float|double|int|uint|dir|ddir)`, `lookup0attrnumcomps(1|2|3|4)`, `lookup0attrdefaultval`

### Lookup Texture POP — `lookuptexturePOP`
The Lookup Texture POP in its simplest form takes two attributes (the Lookup Attribute U and the Lookup Attribute V) with values in the 0-1 range and for each point, uses the attribute value as an index into the pixels of a TOP, pulling the four RGBA values, and placing those values into POP attribu
Params: `attrclass(point|vertex|primitive)`, `group`, `top`, `indexunit`, `pixelcentered`, `cyclic`, `inputextend`, `interpolate`, `usedepthoffset`, `channelmask`, `fromlow`, `fromhigh`, `tolow`, `tohigh`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `lookupindexattr0`, `lookupindexattr1`, `lookupindexattr2`, `lookupindexoffset`

### Math Combine POP — `mathcombinePOP`
The Math Combine POP can do numerous math operations in one node, and is an expansion of the more elementary Math POP and Math Mix POP.
Params: `attrclass(point|vertex|primitive)`, `lengthmismatchnotif`, `group`, `angleunit(deg|rad|cycle)`, `input`, `input0pop`, `input0attrs(*)`, `input0renameto`, `vec`, `vec0name`, `vec0type(float|float2|float3|float4|double|double2|double3|double4|int|int2|int3|int4|uint|uint2|uint3|uint4)`, `vec0value`, `premultcolor`, `color`, `color0name`, `color0rgb`, `color0alpha`, `attr`, `attr0name`, `attr0type`, `attr0defaultval`, `pre`, `pre0scope`, `pre0parsize(1|2|3|4)`, `pre0order(multaddop|addmultop|opmultadd|opaddmult)`, `pre0mult`, `pre0add`, `pre0oper(none|abs|sign|sqrt|square|inverse|floor|round|ceil|int|fract|degrees|radians|normalize|exp10|exp2|exp|log10|log2|ln|sin|cos|tan|asin|acos|atan|dbtopow|powtodb|dbtoamp|amptodb)`, `pre0quantize(off|floor|round|ceiling|gt0|gteq0|eq0|neq0|lteq0|lt0)`, `pre0resultscope(Color|Color.rgb|N|Tex)`, `comb`, `comb0oper(none|copya|abs|sign|sqrt|square|inverse|floor|round|ceil|int|fract|normalize|exp10|exp2|exp|log10|log2|ln|sin|cos|tan|asin|acos|atan|degrees|radians|length|compadd|compsub|compmult|compdiv|compavg|compmin|compmax|add|asubb|bsuba|mult|adivb|bdiva|apowerb|logba|avg|min|max|mod|intadivb|gt|gte|lt|lte|eq|ne|atan2|dot|angle|cross|reflect|aaddbmultc|amultbaddc|aaddbaddc|amultbmultc|rangefrom|rangeto|mix|ifelse|loop|zigzag|clamp|smoothstep|bltealtc|bltaltec|bltaltec|bltaltec|refract)`, `comb0scopea`, `comb0scopeb`, `comb0scopec`, `comb0result(Color|Color.rgb|N|Tex)`, `post`, `post0scope`, `post0parsize(1|2|3|4)`, `post0fromlow`, `post0fromhigh`, `post0tolow`, `post0tohigh`, `post0quantize(off|floor|round|ceiling|gt0|gteq0|eq0|neq0|lteq0|lt0)`, `post0castto(auto|float|int)`, `post0result(Color|Color.rgb|N|Tex)`, `delattrs`, `delnewattrs`, `outputsecondary(*)`

### Math Mix POP — `mathmixPOP`
The Math Mix POP can do a series of math operations in one node.
Params: `lengthmismatchnotif`, `group`, `angleunit(deg|rad|cycle)`, `input`, `input0pop`, `attrclass(point|vertex|primitive)`, `vec`, `vec0name`, `vec0type(float|float2|float3|float4|double|double2|double3|double4|int|int2|int3|int4|uint|uint2|uint3|uint4)`, `vec0value`, `premultcolor`, `color`, `color0name`, `color0rgb`, `color0alpha`, `comb`, `comb0oper(none|copya|abs|sign|sqrt|square|inverse|floor|round|ceil|int|fract|normalize|exp10|exp2|exp|log10|log2|ln|sin|cos|tan|asin|acos|atan|degrees|radians|length|compadd|compsub|compmult|compdiv|compavg|compmin|compmax|add|asubb|bsuba|mult|adivb|bdiva|apowerb|logba|avg|min|max|mod|intadivb|gt|gte|lt|lte|eq|ne|atan2|dot|angle|cross|reflect|aaddbmultc|amultbaddc|aaddbaddc|amultbmultc|rangefrom|rangeto|mix|ifelse|loop|zigzag|clamp|smoothstep|bltealtc|bltaltec|bltaltec|bltaltec|refract|dbtopow|powtodb|dbtoamp|amptodb|rgbtohsv|hsvtorgb)`, `comb0scopea`, `comb0scopeb`, `comb0scopec`, `comb0result(Color|Color.rgb|N|Tex)`, `delattrs`, `delnewattrs`

### Math POP — `mathPOP`
The Math POP takes one attribute of its input, does some math operations, and outputs to any existing attribute or a new attribute.
Params: `attrclass(point|vertex|primitive)`, `group`, `inputattrscope`, `angleunit(deg|rad|cycle)`, `parsize(1|2|3|4)`, `preoper(none|abs|sign|sqrt|square|inverse|floor|round|ceil|int|fract|degrees|radians|normalize|exp10|exp2|exp|log10|log2|ln|sin|cos|tan|asin|acos|atan|dbtopow|powtodb|dbtoamp|amptodb|length|compadd|compsub|compmult|compdiv|compavg|compmin|compmax)`, `preadd`, `mult`, `postadd`, `postoper(none|abs|sign|sqrt|square|inverse|floor|round|ceil|int|fract|degrees|radians|normalize|exp10|exp2|exp|log10|log2|ln|sin|cos|tan|asin|acos|atan|dbtopow|powtodb|dbtoamp|amptodb|length|compadd|compsub|compmult|compdiv|compavg|compmin|compmax)`, `fromlow`, `fromhigh`, `tolow`, `tohigh`, `quantize(off|floor|round|ceiling|gt0|gteq0|eq0|neq0|lteq0|lt0)`, `castto(auto|float|int)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Merge POP — `mergePOP`
The Merge POP merges together the points, vertices amd primitives of all its inputs into one output.
Params: `uniquegroupname`, `groupentity(primitive|point)`, `group`, `input`, `input0pop`, `input0groupentity(point|vertex|primitive)`, `input0group`

### Neighbor POP — `neighborPOP`
The Neighbor POP uses the P attribute to find, for each point of the input, the closest points to it.
Params: `nebrtype(distance|connected)`, `maxdistance`, `distribution(default|unique|closest|random)`, `numhashbuckets`, `outputhash`, `nebroutput(nebr|avg|weightedavg)`, `maxneighbors`, `nebrs`, `numnebrs`, `dodist`, `maxnebrsavg`, `incquerypt`, `addprefix`, `castintstofloats`, `nebrptattrs(*)`

### Noise POP — `noisePOP`
The Noise POP affects every point with a noise field, which can be thought of as smooth, randomly-rising and falling values in 3D space.
Params: `noiselookupattrib`, `type(perlin2d|perlin3d|perlin4d|simplex2d|simplex3d|simplex4d)`, `noisesize(1|2|3|4)`, `seed`, `period`, `harmon`, `spread`, `gain`, `parsize(1|2|3|4)`, `amp`, `exp`, `offset`, `attrclass(point|vertex|primitive)`, `group`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`, `t4d`, `noise`, `gradient`, `curl3d`, `curl2d`, `combineop(none|add|mult|translatealongnormal)`, `combineentity(noise|curl3d|curl2d)`, `combineattrscope`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `computenormals`, `mode(performance|quality)`, `map`, `map0op`, `map0element`, `map0parm(period|offset|amp|exp|spread|gain)`, `map0combineop(set|mult|add)`

### Normal POP — `normalPOP`
The Normal POP lets you create “normal vectors” and “tangent vectors” based on the incoming set of triangles or quads.
Params: `nml(noaction|alwayscompute|computeifnone|remove)`, `inputposattrn`, `attrclass(point|vertex|primitive)`, `nmlweighting(average|angleWeighted|areaweighted)`, `compnmltech(atomicfloat|atomiccompswap|loopprims)`, `maxprimsperpoint`, `angle`, `outputattrscopen(P|N|Color|Color.i012|Tex|PointScale|LineWidth)`, `overrideautoattrn`, `attrtypen(float|double|int|uint|dir|ddir)`, `attrnumcompsn(1|2|3|4)`, `attrdefaultvaln`, `tang(noaction|alwayscompute|computeifnone|remove)`, `inputposattrt`, `inputnormalattr`, `inputtexattrib`, `comptangtech(atomicfloat|atomiccompswap)`, `outputattrscopet(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattrt`, `attrtypet(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcompst(1|2|3|4)`, `attrdefaultvalt`

### Normalize POP — `normalizePOP`
The Normalize POP can re-scale all your XYZ position values to be in the 0-1 range, and it can do that to any attribute.
Params: `attrclass(point|vertex|primitive)`, `inputattrscope`, `parsize(1|2|3|4)`, `aspectcorrect`, `replace`, `errval`, `mode`, `bias`, `lookupcurve`, `exp`, `tolow`, `tohigh`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Null POP — `nullPOP`
The Null POP does nothing - it passes its input to its output unchanged.
Params: `bypass`

### OAK Select POP — `oakselectPOP`
The OAK Select POP can receive point cloud data.
Params: `active`, `chop`, `stream`, `cachesize`

### Out POP — `outPOP`
The Out POP outputs data to POPs outside its parent component.
Params: `selectpop`, `label`, `connectorder`

### Particle POP — `particlePOP`
The Particle POP is used for creating and controlling motion of "particles" for particle system simulations.
Params: `targetpop`, `createpointprim`, `pointidreuse(loop|unused|none)`, `maxparticles`, `emissionmode(rate|attr)`, `birthrate`, `birthattr`, `rndinputpts`, `life`, `lifevariance`, `randomseed`, `timeintegration`, `jitterbirthtime`, `jitterbirthpos`, `initvelocity`, `initmass`, `initdrag`, `damping`, `initializepulse`, `startpulse`, `play`, `speed`, `preroll`, `donepulse`, `attrs(*)`, `renameto`, `usedeathattr`, `attr`, `attr0name`, `attr0type`, `attr0value`, `map`, `map0op`, `map0element`, `map0parm(life|lifevariance|damping|initvelocity|initvelocityx|initvelocityy|initvelocityz|initmass|initdrag)`, `map0combineop(set|mult|add)`

### Pattern POP — `patternPOP`
The Pattern POP is a generator that makes simple line strip shapes using elementary math functions in X, Y and Z.
Params: `numpoints`, `cyclic`, `connectivity(none|linestrip|lines|points)`, `parsize(1|2|3|4)`, `type`, `seed`, `numcycles`, `steppercycle`, `bias`, `phase`, `exp`, `fromlow`, `fromhigh`, `tolow`, `tohigh`, `reverse`, `linebreakcycle`, `closed`, `outputlinebreakattr`, `texture(off|rampstartend|ramppercycle)`, `combineop(set|add|mult)`, `combineattrscope`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `attrclass(point|vertex|primitive)`, `group`

### Phaser POP — `phaserPOP`
The Phaser POP works like the Phaser CHOP.
Params: `phaseattrscope`, `fract`, `parsize(1|2|3|4)`, `edge`, `reversephase`, `smoothstep`, `castto(auto|float|int)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `attrclass(point|vertex|primitive)`, `fromlow`, `fromhigh`, `tolow`, `tohigh`

### Plane POP — `planePOP`
The Plane POP creates rows and columns of points in a planar grid shape.
Params: `surftype(none|points|rows|cols|rowcol|triangles|alttriangles|quads)`, `linetype(linestrip|lines)`, `orient(xy|yz|zx)`, `modifybounds`, `size`, `cols`, `rows`, `anchoru`, `anchorv`, `t`, `r`, `scale`, `normal(none|pointNormals|vertNormals)`, `texture(none|point|vert)`

### Point File In POP — `pointfileinPOP`
The Point File In POP loads 3D point data into POPs from either a single file or a sequence of files.
Params: `file`, `reload`, `createpointprim`, `maxpointsenable`, `splat(none|auto|custom|ply|spz)`, `maxpoints`, `positionfields(x|y|z|nx|ny|nz|r|g|b|a)`, `normalfields(x|y|z|nx|ny|nz|r|g|b|a)`, `texturefields(x|y|z|nx|ny|nz|r|g|b|a)`, `colorfields(x|y|z|nx|ny|nz|r|g|b|a)`, `attr`, `attr0fields(x|y|z|nx|ny|nz|r|g|b|a)`, `attr0name`, `attr0isarray`, `attr0arraysize`, `attr0qualifier(none|color|dir|quat)`, `inputcolorspace(automatic|srgb|srgblinear|rec601ntsc|rec709|rec2020|rec2020st2084pq|rec2020hlg|dcip3|dcip3d60|displayp3d65|displayp3d65linear|aces2065-1|acescg|acesproxy|passthrough)`, `inputreferencewhite(default|sdr|hdr|ui)`, `thinoutrange`, `thinrangestart`, `thinrangelength`, `thinstep`, `thinrandom`, `thinrandomseed`, `rerange`, `rerange0scope(P|P.i01|Color|Color.rgb|N)`, `rerange0parsize(1|2|3|4)`, `rerange0fromlow`, `rerange0fromhigh`, `rerange0tolow`, `rerange0tohigh`

### Point Generator POP — `pointgeneratorPOP`
The Point Generator POP creates a specified number of points, either randomly or in a pattern, on the surface of shape or within the volume of a closed shape.
Params: `shape(sphere|box|torus|tube|rectangle|circle|line)`, `createpointprim`, `numpoints`, `distribution(volume|surface)`, `random`, `seed`, `orient(default|xy|yz|zx)`, `size`, `radius`, `height`, `pointa`, `pointb`, `normal(none|pointNormals|vertNormals|primNormals)`, `normaldirection(default|random)`, `dotangent(off|default|randomtonormal|random)`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`

### Point POP — `pointPOP`
The Point POP is similar to the Primitive POP but it creates points only and has no inputs.
Params: `createp`, `createpointprim`, `attr`, `attr0name(custom|n|color|tex|pointscale|linewidth)`, `attr0customname`, `attr0type(float|double|int|uint|dir|ddir)`, `attr0numcomps(1|2|3|4)`, `pt`, `pt0pos`

### Polygonize POP — `polygonizePOP`
The Polygonize POP takes as input a TOP that is a 3D texture (see Texture 3D TOP), or a POP that is arranged as a 3-dimensoinal grid of points (See Dimension) and creates a 3D polygonal surface that encloses pixels or points exceeding a specified threshold.
Params: `inputattrscope`, `posattrib`, `top`, `channel(luminance|red|green|blue|alpha|rgbaverage|average|rgbmax|max)`, `resmult`, `inside(lteq|gt)`, `threshold`, `extend(hold|zero|repeat|mirror)`, `uniquepoints`, `rerangep`, `tolow`, `tohigh`, `nmlmethod(none|gradient|surface)`, `nmlstepmul`, `texture`, `allocfract`, `cpureadback`

### Primitive POP — `primitivePOP`
The Primitive POP lets you manually create primitives.
Params: `keep`, `addpts`, `premultcolor`, `attr`, `attr0name(custom|n|color|tex|pointscale|linewidth)`, `attr0customname`, `attr0type(float|double|int|uint|dir|ddir)`, `attr0numcomps(1|2|3|4)`, `attr0value`, `pt`, `pt0pos`, `method(none|set|pattern)`, `setprimtype(none|points|lines|triangles|quads|linestrip|closedlinestrip)`, `set(all|group|skip)`, `n`, `prim`, `prim0type(none|points|lines|triangles|quads|linestrip|closedlinestrip)`, `prim0pattern`, `unusedpointsop(donothing|remove|pointprims)`, `cpureadback`

### Projection POP — `projectionPOP`
The Projection POP takes a float3 3D spatial attribute, like P, and outputs to a float3 attribute, transforming the attribute between cartesian (orthographic), polar, cylindrical, and perspective coordinate systems.
Params: `attrclass(point|vertex|primitive)`, `group`, `inputattrscope`, `fromcoordsys(cartesian|spherical|cylindrical|screenspace|ndc)`, `tocoordsys(cartesian|spherical|cylindrical|screenspace|ndc)`, `angunit(deg|rad|cycle|norm)`, `camera`, `aspectcorrectuv`, `aspect`, `fov`, `depthnear`, `depthfar`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Proximity POP — `proximityPOP`
The Proximity POP connects points to nearby points in its first input within a specified near/far distance.
Params: `maxdist`, `mindist`, `maxlinesperpoint`, `uniformdist`, `maxtempneighbors`, `duplines(donothing|avoid|delete)`, `numhashbuckets`, `output(lines|points)`, `linedir`, `linelength`, `endptattrs`, `origin(first|second)`, `remunusedpoints`, `cpureadback`

### Quantize POP — `quantizePOP`
The Quantize POP takes any attribute of its input, quantizes the values to integers or any step size, or it converts values to logical 0 or 1 values, and then outputs the resuting values to the same attribute, any other existing attribute or a new attribute.
Params: `attrclass(point|vertex|primitive)`, `group`, `inputattrscope`, `parsize(1|2|3|4)`, `quantize(off|floor|round|ceiling|gt|gteq|eq|neq|lteq|lt|off|floor|round|ceiling|gt|gteq|eq|neq|lteq|lt)`, `quantstep`, `quantoffset`, `quantcompare`, `castto(auto|float|int)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Random POP — `randomPOP`
The Random POP takes its input and either (1) generates a new attribute containing random values, or (2) sets, adds or multiplies an existing attribute by a random value for each point.
Params: `extrapts`, `type(constant|twovalues|uniform|uniformdiscrete|direction|insidesphere|normal|exponential|lognormal|cauchylorentz|customramp|none|gaussian)`, `chop`, `randomsize(1|2|3|4)`, `seed`, `parsize(1|2|3|4)`, `amp`, `exp`, `offset`, `valuea`, `valueb`, `valuebproba`, `clamp`, `minval`, `maxval`, `conedir`, `coneangle`, `combineop(set|add|mult|translatealongnormal)`, `combineattrscope`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `attrclass(point|vertex|primitive)`, `group`, `computenormals`, `map`, `map0op`, `map0element`, `map0parm(amp|exp|offset|valuea|valueb|valuebproba|stepval|minval|maxval|conedir|conedirx|conediry|conedirz|coneangle)`, `map0combineop(set|mult|add)`

### Ray POP — `rayPOP`
The Ray POP casts a ray from each points of the input, in the direction defined by the Ray Attribute, and outputs new attributes that report what each ray hits.
Params: `rayattrib`, `negateray`, `numbounces`, `connectpoints`, `limitraylength`, `trimray`, `hwraytracing(off|fastbuild|fasttrace)`, `opaque`, `anyhit`, `hitnormal`, `doreflectedray`, `dist`, `farhit`, `numhits`, `inside`, `hitprimindex`, `barycoords`, `scale`, `lift`, `hitpointattrscope(*)`, `hitprimattrscope(*)`, `hitvertattrscope(*)`

### ReRange POP — `rerangePOP`
The ReRange POP takes any attribute of its input, re-ranges its values, and outputs them to the same attribute, any other existing attribute or a new attribute.
Params: `attrclass(point|vertex|primitive)`, `group`, `inputattrscope`, `parsize(1|2|3|4)`, `fromlow`, `fromhigh`, `tolow`, `tohigh`, `castto(auto|float|int)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Rectangle POP — `rectanglePOP`
The Rectangle POP creates a 4-point rectangle with optional rounded corners, and outputs it as a line strip, a pair of triangles, a quad, separate 2-point lines, unconnected point primitives, or without any primitives.
Params: `surftype(none|point|lines|linestrips|triangles|quads)`, `modifybounds`, `orient(xy|yz|zx|cam)`, `camera`, `distfromcam`, `cameraaspect`, `size`, `roundcorners`, `cornerradius`, `cornersides`, `anchoru`, `anchorv`, `t`, `r`, `scale`, `normal(none|pointNormals)`, `texture(none|point|vert)`, `texturefit(fill|best|outside)`

### Revolve POP — `revolvePOP`
The Revolve POP generates a surface of revolution from any set of line strips.
Params: `axis(auto|x|y|z)`, `autopivot`, `p`, `surftype(none|points|rows|cols|rowcol|triangles|alttriangles|quads)`, `divs`, `texture(none|pointNormals|vertNormals)`, `normal(none|pointNormals|vertNormals)`

### SOP to POP — `soptoPOP`
The SOP to POP converts the SOP 3D geometry to POP geometry.
Params: `sop`, `polygons(ignore|triangulated|closedlinestrip)`, `mesh(ignore|quads|rows|cols|rowscols|points)`, `inputcolorspace(automatic|srgb|srgblinear|rec601ntsc|rec709|rec2020|rec2020st2084pq|rec2020hlg|dcip3|dcip3d60|displayp3d65|displayp3d65linear|aces2065-1|acescg|acesproxy|passthrough)`, `inputreferencewhite(default|sdr|hdr|ui)`

### Script POP — `scriptPOP`
The Script POP can build a complete POP as a generator (no input) or a filter of its input POPs.

### Select POP — `selectPOP`
The Select POP takes individual attributes from its single input and outputs the attributes unchanged.
Params: `pop`, `pointattrscope(*)`, `primattrscope(*)`, `vertattrscope(*)`

### Skin Deform POP — `skindeformPOP`
(needs to be updated) A popular way to deform geometry based on Transforms or a full skeleton is called Skinning.
Params: `mode(skindeformgeo|skindeformattrib|skindeformattribscopepos|skindeformattribscopevec)`, `attrclass(point|vertex|primitive)`, `inputattrscope`, `bonepaths`, `bonebindposes`, `delcaptattrs`, `skelrootpath`, `vlength`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Skin POP — `skinPOP`
The Skin POP takes any 2-dimensional (or more) arrangement of data (for example three line strips of 20 point each) and connects them together as a mesh of triangles or quads.
Params: `skinops(all|group|skip)`, `inc`, `closed`, `outputquads`

### Sort POP — `sortPOP`
The Sort POP sorts the point list and/or the primitive list based on the position P or any attribute component.
Params: `ptmethod(none|byattrib|seed|prox|vector|object)`, `pointattr`, `pointuint(notuint|uint4|uint8|uint12|uint16|uint20|uint24|uint28|uint32)`, `pointseed`, `pointprox`, `pointdir`, `pointobj`, `pointrev`, `pointshift`, `pointoffset`, `primmethod(none|byptattrib|byprimattrib|seed|prox|vector|object)`, `primattr`, `primuint(notuint|uint4|uint8|uint12|uint16|uint20|uint24|uint28|uint32)`, `primseed`, `primprox`, `primdir`, `primobj`, `primrev`, `primshift`, `primoffset`

### Sphere POP — `spherePOP`
The Sphere POP creates spherical shapes in two different forms: Geodesic type creates a set of triangles of equally-spaced points which can be recursively divided giving more detail, and Grid type where you specify rows and columns of points similar to latitude/longitude lines.
Params: `type(geodesic|grid|tetrahedron|sharedpoles)`, `geodesictype(none|point|triangles)`, `surftype(none|point|rows|cols|rowcol|triangles|alttriangles|quads)`, `linetype(linestrip|lines)`, `orient(x|y|z)`, `modifybounds`, `rad`, `freq`, `fuse`, `fusetechnique(bruteforce|sharedmemory|spatialgrid)`, `cols`, `rows`, `anchoru`, `anchorv`, `anchorw`, `t`, `r`, `scale`, `normal(none|pointNormals|vertNormals)`, `texture(none|pointtexcoord|vertextexcoord)`, `texmethod(equirectangularin|equirectangularout|equiazimuth)`, `fov`, `sharedpolessurftype(none|point|rows|cols|rowcol|triangles|alttriangles|quadsandtriangles)`, `closedu`, `angleu`, `texrangeu(partial|full)`, `anglev`, `texrangev(partial|full)`

### Sprinkle POP — `sprinklePOP`
The Sprinkle POP creates points either on the surface of the input POP or within the volume of the input POP.
Params: `createpointprim`, `seed`, `method(perprim|volume|volumedeterministic|volnondeterministic|vol)`, `numpoints`, `attemptsperpoint`, `raydirmode(constant|random)`, `raydir`, `hwraytracing(off|fastbuild|fasttrace)`, `pointattrscope(*)`, `primattrscope(*)`, `vertattribscope(*)`

### Subdivide POP — `subdividePOP`
The Subdivide POP subdivides and smooths a surface.
Params: `iterations`, `creaseweight`, `simplecoeffs`, `cpureadback`

### Switch POP — `switchPOP`
The Switch POP lets you choose one of the inputs, and outputs the input unchanged.
Params: `index`, `extend(clamp|loop|zigzag)`, `blend`, `lengthmismatchnotif`, `pointattrscope(*)`, `primattrscope(*)`, `vertattrscope(*)`, `input`, `input0pop`

### TOP to POP — `toptoPOP`
Position and Active is a shortcut for P in RGB, and alpha is set to 1 for active pixels (pixels with a valid attribute value).
Params: `rgba(color|pactive|pos|depth|height|custom)`, `maxpointsenable`, `input`, `input0top`, `input0chanscope(r|g|b|a)`, `input0attrscope(P|P.i01)`, `input0filter(nearest|linear|highquality)`, `attr`, `attr0name`, `attr0type`, `attr0defaultval`, `surftype(none|points|lines|linestrips|triangles|alttriangles|quads)`, `line`, `plane`, `uniquepoints`, `t`, `overridesize`, `size`, `overrideres`, `res`, `pixelsamplingloc(edgetoedge|pixelcentered)`, `texture(none|point|vert)`, `dimension(morethanone|rowscolsalways|rowscolsslicesalways)`, `rerangefromlow`, `rerangetolow`, `camera`, `overridecamera`, `viewanglemethod(horfov|vertfov|focallengths)`, `fov`, `focallengths`, `center`, `deletenear`, `depthnear`, `deletefar`, `depthfar`, `linestripbehavior(delpointoflinestrip|splitlinestrip|dellinestrip)`, `dispscale`

### Text POP — `textPOP`
The Text POP creates geometry from any [http://en.wikipedia.org/wiki/TrueType TrueType] or [http://en.wikipedia.org/wiki/OpenType OpenType] font that is installed on the system, or any TrueType/OpenType font file on disk.
Params: `connectivity(triangles|linestrips)`, `bridgeholes`, `mode(text|specdat)`, `text`, `specdat`, `specchop`, `scalefonttobboxheight`, `breaklang`, `readingdirection(lefttoright|righttoleft)`, `wordwrap`, `wordwrapsize`, `smartpunct`, `levelofdetail`, `font`, `fontfile`, `typeface`, `fontsize`, `keepfontratio`, `tracking`, `linespacing`, `alignx(left|center|right)`, `aligny(bottom|center|top|baseline)`, `fontcolor`, `fontalpha`, `extrude`, `extrudedepth`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`

### Texture Map POP — `texturemapPOP`
The Texture Map POP creates the Tex attribute which is used to apply texture maps to surfaces, or to position procedurally-generated textures to surfaces.
Params: `group`, `transforminput`, `inputtexattr`, `posattr`, `axis(x|y|z)`, `fov`, `centermode(bbcenter|manual)`, `center`, `camera`, `cameraaspect`, `applyto(natural|point|vertex)`, `s`, `offset`, `angle`, `fixseams`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `texmethod(xyznorm|xyzposition|cylin|face|facefitoutside|equirectangularin|equirectangularout|equiazimuth|persp|triplanar)`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `scaletwo`, `p`

### Time Filter POP — `timefilterPOP`
The Time Filter POP filters attribute values over time to smooth out noise and jitter.
Params: `active`, `alwayscook`, `attrclass(point|primitive|vertex)`, `attrs(*)`, `renameto`, `type(none|gaussian|triangle|box|oneeuro)`, `width`, `inc`, `cutoff`, `speedcoeff`, `slopecutoff`, `filterreset`, `fillmissedframes`, `attrmatch`, `attrname`, `uintmax(uint4|uint8|uint12|uint16|uint20|uint24|uint28|uint32)`, `maxelements`, `lagtype(none|value|amplitude)`, `lag`, `overshoot`, `clampslope`, `slope`, `clampaccel`, `accel`, `snap`, `lagreset`, `freeze`, `freezereset`, `map`, `map0op`, `map0element`, `map0parm(width|cutoff|speedcoeff|slopecutoff|freeze|lag|lag0|lag1|overshoot|overshoot0|overshoot1|slope|slope0|slope1|accel|accel0|accel1|snapthreshold)`, `map0combineop(set|mult|add)`

### Topology POP — `topologyPOP`
The Topology POP gives finer control on how to combine existing points and topology (vertices and primitives), as well as their memory allocation.
Params: `maxpointsmode`, `pointcountinfo(input|fromparams|fromattrs)`, `pointcountpop`, `pointcountclass`, `render`, `primsourcemode(input|specpop)`, `primmode(topo|attr)`, `primspop`, `pointindexattrclass`, `vertattrmode(none|primsource|specpop)`, `vertattrpop`, `vertattrclass(point|vertex|primitive)`, `primattrmode(none|primsource|specpop)`, `primattrpop`, `primattrclass(point|vertex|primitive)`, `topology(ref|copy)`, `maxtrianglesmode`, `maxquadsmode`, `maxlinestripsmode`, `maxlsvertsmode`, `maxlinesmode`, `maxpointprimsmode`, `lsinfofromprimsource`, `lsinfoupdate(auto|manual)`, `lsinfopop`, `lsinfoclass`, `lsindexpop`, `lsindexclass`, `lsmaxvertsoverride`, `topoinfo(primsource|fromparams|fromattrs)`, `topoinfopop`, `topoinfoclass(point|vertex|primitive)`, `trianglecountmode`, `quadcountmode`, `linestripcountmode`, `lsvertcountmode`, `linecountmode`, `pointprimcountmode`

### Torus POP — `torusPOP`
The Torus POP creates rows and columns of points in a closed tube shape.
Params: `surftype(none|points|rows|cols|rowcol|triangles|alttriangles|quads)`, `linetype(linestrip|lines)`, `orient(x|y|z)`, `modifybounds`, `rad`, `cols`, `rows`, `anchoru`, `anchorv`, `anchorw`, `t`, `r`, `scale`, `normal(none|pointNormals|vertNormals)`, `texture(none|pointNormals|vertNormals)`, `closedu`, `closedv`, `angleu`, `anglev`

### Trace POP — `tracePOP`
The Trace POP reads a TOP image and traces it, generating line strips around areas exceeding a certain brightness threshold.
Params: `inputattrscope`, `posattrib`, `top`, `channel(luminance|red|green|blue|alpha|rgbaverage|average|rgbmax|max)`, `resmult`, `threshold`, `inside(below|above)`, `extend(hold|zero)`, `twodimensions(contour|contourls|surface)`, `uniquepoints`, `winding(natural|ccw)`, `smooth`, `rerangep`, `tolow`, `tohigh`, `normal(none|point|prim)`, `normaldirection(default|z)`, `texture`, `allocfract`, `setmaxnumls`, `setmaxnumvertsperls`, `cpureadback`

### Trail POP — `trailPOP`
The Trail POP captures and retains all the points of the input for the most recent N frames or N "slices", being a time-history of the input's points.
Params: `active`, `alwayscook`, `length`, `inc`, `reset`, `ageattr(none|seconds|frames)`, `oldestpointfirst`, `fillmissedframes`, `orientationattrs(none|tangent|tangentnormal|tangentnormalbinormal|quaternion|matrix3x3|matrix4x4)`, `attrmatch`, `attrname`, `uintmax(uint4|uint8|uint12|uint16|uint20|uint24|uint28|uint32)`, `maxls`, `surftype(none|points|rows|cols|rowcol|triangles|alttriangles|quads)`, `closed`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`

### Transform POP — `transformPOP`
The Transform POP applies a translate, rotate and scale to the position (attribute P) and normal (attribute N) of all the points of the input.
Params: `mode(transformgeo|transformattrib|transformattribscopepos|transformattribscopevec|transformattr|transformattrscopepos|transformattrscopevec)`, `attrclass(point|vertex|primitive)`, `inputattrscope`, `group`, `weightattr`, `xord(srt|str|rst|rts|tsr|trs)`, `rord(xyz|xzy|yxz|yzx|zxy|zyx)`, `t`, `r`, `s`, `p`, `scale`, `invert`, `vlength`, `lookat`, `upvector`, `forwarddir(posx|negx|posy|negy|posz|negz)`, `xformmatrixop`, `multiplyorder(inputxformpage|xformpageinput)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`, `alignxformorder(transformalign|aligntransform)`, `alignopord(st|ts)`, `aligntx(off|origin|reference)`, `fromx(min|center|max)`, `tox(min|center|max)`, `alignty(off|origin|reference)`, `fromy(min|center|max)`, `toy(min|center|max)`, `aligntz(off|origin|reference)`, `fromz(min|center|max)`, `toz(min|center|max)`, `alignscale(peraxis|unity|reference)`, `alignscalex(off|unity|reference|unityprop|referenceprop)`, `alignscaley(off|unity|reference|unityprop|referenceprop)`, `alignscalez(off|unity|reference|unityprop|referenceprop)`, `map`, `map0op`, `map0element`, `map0parm(t|tx|ty|tz|r|rx|ry|rz|s|sx|sy|sz|p|px|py|pz|scale)`, `map0combineop(set|mult|add)`

### Triangulate POP — `triangulatePOP`
The Triangulate POP converts each closed line strip into a set of triangles that fill the interior of the line strip.
Params: `mode(convex|concave)`, `connectholes`, `hwraytracing(off|fastbuild)`, `raydir`, `maxls`, `numpasses`, `lsmaxverts`, `exceedmaxverts(zero|clamp)`, `maxiter`, `triangulatequads`, `remzerotri`

### Trig POP — `trigPOP`
The Trig POP is a simple operator that converts attributes that are angles into the trigonometry representation of angles (sine, cosine, tangent).
Params: `attrclass(point|vertex|primitive)`, `group`, `inputattrscopea`, `inputattrscopeb`, `operation(none|cos|sin|tan|acos|asin|atan|atan2|cosh|sinh|tanh|none|cos|sin|tan|acos|asin|atan|atan2|cosh|sinh|tanh)`, `fromunit(deg|rad|cycle)`, `tounit(deg|rad|cycle)`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### Tube POP — `tubePOP`
The Tube POP creates rows and columns of points in a cylinder or tube shape.
Params: `surftype(none|points|rows|cols|rowcol|triangles|alttriangles|quads)`, `linetype(linestrip|lines)`, `orient(x|y|z)`, `modifybounds`, `rad`, `height`, `cols`, `rows`, `anchoru`, `anchorv`, `anchorw`, `t`, `r`, `scale`, `normal(none|pointNormals|vertNormals)`, `texture(none|point|vert)`, `closedu`, `angleu`, `endcaps`

### Twist POP — `twistPOP`
The Twist POP performs non-linear deformations on points such as Twist, Bend, Shear, Taper, Linear Taper, and Squash & Stretch.
Params: `attrclass(point|vertex|primitive)`, `inputattrscope`, `weightattr`, `op(twist|bend|shear|taper|ltaper|squash)`, `paxis(x|y|z)`, `saxis(x|y|z)`, `p`, `strength`, `rolloff`, `outputattrscope(P|N|Color|Color.rgb|Tex|PointScale|LineWidth)`, `overrideautoattr`, `attrtype(float|double|int|uint|color|dcolor|dir|ddir)`, `attrnumcomps(1|2|3|4)`, `attrdefaultval`

### ZED POP — `zedPOP`
The ZED POP uses the ZED StereoLabs SDK to scan and create geometry meshes (triangles) by moving it around the room or an object of interest.
Params: `active`, `zedtop`, `outputmode(mesh|pointcloud)`, `connectivity(none|points|triangles)`, `initialize`, `startpulse`, `play`, `donepulse`, `preview(nopreview|limited|limited)`, `maxmemory`, `resolution`, `range`, `normals`, `color`, `filter(low|medium|high)`, `perspective(left|right)`, `rerangefromlow`, `rerangetolow`, `mirrorimage`, `camera`, `overridecamera`, `viewanglemethod(horfov|vertfov|focallengths)`, `fov`, `focallengths`, `center`, `deletenear`, `depthnear`, `deletefar`, `depthfar`

