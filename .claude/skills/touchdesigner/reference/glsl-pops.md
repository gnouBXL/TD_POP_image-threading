# Shaders GLSL POP — aide-mémoire (doc *Write a GLSL POP*)

GLSL 4.60, compute shaders. Chaque attribut est un SSBO. TouchDesigner génère
les déclarations (attributs, uniforms, `layout(local_size…)`) : ne pas les
redéclarer.

## Nombre d'éléments / index

```glsl
uint TDNumElements();   // threads demandés (pas défini en mode Manual)
uint TDIndex();         // index 1D du thread (pas défini en mode Manual)
uint TDInputNumPoints(uint input);  TDInputNumPrims(uint input);  TDInputNumVerts(uint input);
// sans argument = entrée 0 ; renvoie 0 si l'entrée n'existe pas
uint TDInputNumElements();          // GLSL POP : selon la classe choisie
```

Squelette standard :

```glsl
void main() {
    const uint id = TDIndex();
    if (id >= TDNumElements()) return;   // threads arrondis à 32 (NVIDIA) / 64 (AMD)
    P[id] = TDIn_P();                    // = TDIn_P(0, id)
}
```

## Attributs

GLSL POP (classe choisie dans `attrclass`) :

```glsl
T  TDIn_Attr(uint input, uint elem, uint arrayIndex);  // défauts : (0, TDIndex(), 0) ; contrôle de bornes
T  TDInPoint_Attr(...) / TDInVert_Attr(...) / TDInPrim_Attr(...)   // autres classes
T  TDInCache_Attr(uint input, uint cacheIndex, uint elem, uint arrayIndex)  // frames d'un Cache POP
T  Attr[];             // sortie (attributs listés dans outputattrs ou créés page Create Attribs)
const uint cTDArraySize_Attr;
```

GLSL Advanced POP : préfixe de classe partout.

```glsl
T TDInPoint_Attr(uint input, uint id, uint arrayIndex);  TDInPrim_…  TDInVert_…
T oTDPoint_Attr[];  oTDPrim_Attr[];  oTDVert_Attr[];      // sorties
// Extra outputs (page Extra Outputs, nom N) : TDInPoint_N_Attr(id), oTDPoint_N_Attr[], TDInputNumPoints_N()
uint I[];   // index buffer en écriture si un « Max … » est en Custom
```

Sortie lisible dans le même shader seulement avec `outputaccess = readwrite`
(nécessaire aussi pour `atomicAdd` & co. sur `Attr[]`).

## Topologie (lecture)

```glsl
uint TDInputPointIndex(uint input, uint vert);     // index buffer
uint TDInputPrimIndex(uint vert);  TDInputVertPrimIndex(uint vert);
uint TDInputPrimType(uint prim);   TDInputPrimType_Vert(uint vert);
const uint cTDTrianglesType = 0, cTDQuadsType = 1, cTDLineStripsType = 2, cTDLinesType = 3, cTDPointPrimsType = 4;
uint TDInputNumVertsPerPrim(uint input, uint prim);  TDInputNumVertsPerPrimFromVert(uint input, uint vert);
uint TDInputPrimVertsStartIndex(uint input, uint prim);
uint TDInputPrimsStartIndex(uint input, uint primType);  TDInputVertsStartIndex(uint input, uint primType);
const uint cTDPrimIndexRestart;   // 0xFFFFFFFF entre deux line strips
```

Les fonctions « output » de topologie ne sont pas définies en Single Shader
Dispatch (Advanced) ; en mode Per Primitive Batch : `TDPrimsStartIndex()`,
`TDNumPrimsBatch()`, `TDVertsStartIndex()`, `TDNumVertsBatch()`…

## Dimension

```glsl
const uint cTDDimSize;                      // nb de dimensions de l'entrée 0 (cTDDimSizeN pour l'entrée N)
uint[cTDDimSize] TDDimension();             // tailles (ex. {W, H} après TOP to POP)
uint[cTDDimSize] TDDimCoords(uint point);   // = _DimI[]
uint TDDimPointIndex(uint[cTDDimSize] c);
// TDDimensionN(), TDDimCoordsN(), TDDimPointIndexN() pour l'entrée N
```

## GLSL Copy POP

`TDNumPoints()`, `TDInputNumPoints()`, `TDInputIndex()`, `TDCopyIndex()`,
`TDTemplate_Attr()`, `TDIn_Attr()`, autres POPs via page POP Buffers +
`TDBuffer_Attr()` ; `TDUpdatePointGroups()`, `TDUpdateTopology()`,
`TDUpdateLineStripsInfo()`, `TDUpdatePrimGroups()`.

## GLSL TOP (compute) et MAT : accès aux POPs

Page Buffers (`buffer0pop`, `buffer0attrclass`, `buffer0attr`, `buffer0name`) :

```glsl
T TDBuffer_Attr(uint elem, uint arrayIndex);   const uint TDBufferLength_Attr();
// GLSL TOP compute (depuis 2025.30000) :
void TDImageStoreOutput(uint index, ivec3 coord, vec4 color);
vec4 TDImageLoadOutput(uint index, ivec3 coord);   // range-check et sRGB gérés
uniform int uTDPass;                               // index de passe (GLSL TOP)
```

## Non documenté (à tester avant de s'en servir)

- `shared`, `barrier()`, `memoryBarrierBuffer()` : GLSL standard, devraient
  fonctionner en mode Manual, sans confirmation dans la doc.
- Persistance des tableaux de sortie entre passes (GLSL POP, `npasses > 1`,
  `prevpassoutput` Off).
- Nom de l'uniform d'index de passe dans un GLSL POP.
- Page Temp Buffers.
