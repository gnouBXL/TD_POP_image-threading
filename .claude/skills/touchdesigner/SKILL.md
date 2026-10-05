---
name: touchdesigner
description: Expertise TouchDesigner 2025.3x — POPs (Point Operators), GLSL POP / GLSL Advanced POP / GLSL TOP compute, Feedback POP, TOP to POP, Line Strips, Python API (custom parameters, extensions, callbacks), construction de réseaux par script. À charger pour toute question ou tâche TouchDesigner (.toe, .tox, opérateurs TOP/POP/CHOP/SOP/DAT/COMP/MAT, docs.derivative.ca), et avant d'écrire un shader ou un script destiné à TouchDesigner.
---

# TouchDesigner 2025.3x

Connaissances vérifiées dans docs.derivative.ca (octobre 2026), plus les pièges
rencontrés dans le projet ImageThreading POP. Répondre d'abord avec ce fichier et
les index ; n'aller sur la doc que pour ce qui manque.

## Où chercher, dans cet ordre

1. Ce fichier (concepts, pièges, recettes).
2. `reference/pops-index.md` : **tous les POPs** avec `opType` (pour
   `comp.create()`), une phrase de description et les **noms Python des
   paramètres** (+ valeurs de menu). `grep -A3 '### Feedback POP' …`
3. `reference/glsl-pops.md` : fonctions intégrées des shaders GLSL POP.
4. `reference/python-api.md` : API Python (création d'opérateurs, paramètres
   custom, extensions, callbacks, lecture de POPs).
5. `reference/others-index.md` : TOPs/DATs/COMPs/CHOPs/MATs courants.
6. La doc en ligne via le script (cache dans `~/.cache/td_docs`) :
   ```
   S=.claude/skills/touchdesigner/scripts/td_doc.py
   python3 $S params "GLSL POP"            # opType + tous les paramètres (nom Python, type, résumé, menus)
   python3 $S summary "Feedback POP"       # description longue
   python3 $S grep "Write a GLSL POP" TDDim # lignes + contexte
   python3 $S search "line strip info"     # recherche plein texte
   python3 $S methods "POP Class"          # membres/méthodes d'une classe Python
   python3 $S index out.md "Category:POPs" # régénérer un index
   ```
   Astuce : `index.php?title=Page&action=raw` (wikitext) est 5 à 10 fois plus
   compact que le HTML. Le site renvoie 403 au user-agent Python par défaut
   (le script envoie celui de curl). Si docs.derivative.ca est inaccessible,
   le dire au lieu de deviner.

Quand une info est absente de la doc, l'écrire comme **« à vérifier dans TD »**
et proposer un test minimal ; ne pas l'inventer. Après chaque découverte
(doc ou retour de l'utilisateur sur un test dans TD), **mettre à jour ce skill**
(section « Vérifié en pratique » ou « Pièges »).

## Concepts POP essentiels

- POP = géométrie / données sur GPU. Trois listes d'attributs : **points**,
  **vertices**, **primitives**. Chaque attribut est un SSBO séparé.
- Noms standards : `P` (float3), `N`, `Color` (float4 ; **`Cd` est le nom
  SOP**), `Tex` (float3 ; `uv` en SOP), `PointScale`, `T`, `LineWidth`
  (Line MAT), `LineBreak`, `LineStripIndex`, `Weight`, `Part*` (Particle POP).
- Attributs intégrés en lecture seule : `_PointI`, `_PointU`, `_PointCy`,
  `_PrimI`, `_VertPrimI`, `_NumVertsPerPrim`, `_DimI[]`, `_DimU[]`,
  `_DimCy[]`, `_DimSize[]`, `_NumDim`.
- Types de primitives, toujours regroupés dans cet ordre dans l'index buffer :
  triangles, quads, **line strips**, lines, point primitives. Pas de polygone
  quelconque ni de courbe (splines = line strips subdivisés : Line Divide POP).
- **Line strip fermé** = son dernier sommet a le même index de point que le
  premier. Pour un chemin qui repasse par un même point, créer un point par
  sommet, sinon le strip peut se fermer.
- Séparateur entre line strips dans l'index buffer : `cTDPrimIndexRestart`
  (0xFFFFFFFF).
- **Dimension** : métadonnée de structure (ex. Grid 20×40 ; TOP to POP W×H).
  Les `dim[0]` premiers points forment la première ligne. Préservée par les
  POPs qui ne changent pas le nombre de points (Math, GLSL POP), perdue par
  Delete POP.
- **Comptes sur CPU ou sur GPU** : certains POPs (Delete, Proximity, Facet…)
  ne connaissent leur nombre de points/primitives que sur GPU → allocation au
  max + dispatch indirect en aval. Relire ces comptes sur CPU provoque un
  stall (ou 1 frame de latence en mode « delayed »). Topology POP / option
  « Copy Topology Info Back to CPU » pour revenir à des comptes CPU.
- Attributs non modifiés de l'entrée 0 = **références** (pas de copie mémoire).
- Créer des line strips sans écrire d'index buffer : produire des points
  ordonnés + **Line Break POP** (`uselinestripindex` sur l'attribut
  `LineStripIndex`, ou `uselinebreak` sur `LineBreak`).
- GLSL Create POP est **déprécié** : utiliser GLSL Advanced POP (+ Topology POP).

## Choisir le bon opérateur GLSL

| Besoin | Opérateur |
|---|---|
| Modifier/créer des attributs d'une seule classe, nombre d'éléments inchangé | **GLSL POP** (`glslPOP`) |
| Plusieurs passes (`npasses`) dans un cook | **GLSL POP** uniquement (doc *Write a GLSL POP* ; la page de l'Advanced liste `npasses` mais la doc dit le contraire → à vérifier) |
| Changer le nombre de points / primitives, écrire l'index buffer, plusieurs classes à la fois, sorties multiples | **GLSL Advanced POP** (`glsladvancedPOP`) |
| Même shader appliqué à chaque copie | GLSL Copy POP |
| Écrire une image, lire des POPs en entrée | GLSL TOP en mode compute (`TDImageStoreOutput/LoadOutput`, `TDBuffer_Attr()`) |

Réglages de threads (GLSL POP et Advanced) :
- `numthreadsmode` Auto / per element : `TDIndex()` + test
  `if (id >= TDNumElements()) return;` obligatoire (arrondi au workgroup : 32
  NVIDIA, 64 AMD).
- `numthreadsmode = manual` : on fixe `workgroupsize` et `dispatchsize` ;
  **`TDIndex()` / `TDNumElements()` n'existent plus** (erreur de compilation)
  → `gl_GlobalInvocationID`, `gl_LocalInvocationIndex`. TD génère lui-même le
  `layout(local_size_…)`. Un seul workgroup (`dispatchsize 1 1 1`) permet de
  synchroniser tous les threads avec `barrier()`.
- `outputaccess = readwrite` nécessaire pour relire ses sorties et pour les
  atomics. `initoutputattrs` On = dispatch supplémentaire qui copie l'entrée
  (ou met la valeur par défaut des nouveaux attributs) ; Off = sorties non
  initialisées (lire une valeur non initialisée en aval peut planter).
- Uniforms : pages Vectors (`vec0name`, `vec0type` float…uvec4, `vec0value`),
  Colors, Samplers (TOP), Arrays (CHOP), Matrices, Constants (constantes de
  spécialisation), Temp Buffers (sémantique non documentée).

## Feedback POP (boucles d'état)

- `targetpop` = POP en aval dont la sortie revient à la frame suivante.
- `initializepulse` : instantané de l'entrée puis attente (`ready`) ;
  `startpulse` : démarre (seul, il prend aussi l'instantané) ; `play` : pause
  (arrête aussi le cook de la boucle) ; `steppulse` : avance d'une frame ;
  `donepulse` ; `preroll`. **Pas de paramètre Reset** : Reset = Initialize +
  Start. L'instantané **n'est pas repris** quand l'entrée change.
- Info CHOP sur le Feedback POP : `initializing`, `ready`, `running`, `done`,
  `timer_*`.
- Particle POP = Feedback POP spécialisé. Trail POP = historique de N frames
  (+ line strips, `Age`). Cache POP = frames passées.

## TOP ↔ POP

- **TOP to POP** (`toptoPOP`) : `rgba` = color | pactive | pos | depth | height
  | custom ; `input0top`, `input0chanscope`, `input0attrscope` ;
  `input0filter` nearest|linear|highquality ; `pixelsamplingloc`
  edgetoedge|pixelcentered ; `overrideres`/`res` ; `surftype` (connectivité).
  Résultat : dimension W×H. Le sens des lignes (bas → haut ?) n'est pas écrit
  dans la doc → à vérifier.
- **POP to TOP** : `layout` = Fit to Square | Wrapped | Cropped | **POP
  Dimension** (W×H automatique) ; `rgbamode` Position and Active | Custom.
- Lire un TOP dans un shader POP : page Samplers.

## Python : l'essentiel (détails dans reference/python-api.md)

```python
c = parent().create(glslPOP, 'engine')        # classe = opType ; ou baseCOMP, textDAT, nullPOP…
c.inputConnectors[0].connect(op('state'))     # câbler (ou op('a').outputConnectors[0].connect(c))
c.par.computedat = 'engine_comp'              # paramètres par leur nom Python
c.par.numthreadsmode = 'manual'               # menu : par nom (par.menuNames / par.menuLabels)
c.seq.vec.numBlocks = 3; c.par.vec0name = 'uK'  # séquences : op.seq.<nom>
page = comp.appendCustomPage('Threading')
pg = page.appendInt('Linecount', label='Line Count')  # renvoie un ParGroup
pg.default = 2000; pg.min = 1; pg.clampMin = True; comp.par.Linecount = 2000
comp.par.ext0object = "op('./ext').module.MyExt(me)"; comp.par.ext0promote = True
```

Noms de menu inconnus ? Choisir par libellé, avec un helper qui cherche dans
`par.menuLabels` et lève une erreur claire. C'est plus robuste qu'un nom deviné.

## Pièges connus

- Un POP en mode Manual ne peut pas utiliser `TDIndex()`.
- Long dispatch unique (> ~2 s) → risque de reset du driver (TDR Windows) :
  découper en passes ou sur plusieurs frames.
- `Initialize Output Attributes` coûte un dispatch : le couper si le shader
  écrit tout.
- Changer le nombre de points dans un GLSL Advanced POP supprime les
  références aux attributs d'entrée : tout réécrire soi-même.
- `TDIn_Attr()` fait un contrôle de bornes (renvoie le dernier élément hors
  bornes), pas les tableaux de sortie `Attr[id]`.
- Parenthèses dans les menus d'index : `pops-index.md` affiche
  `nom(valeurs)` seulement pour les vrais menus ; `xxx(xxx|yyy)` ailleurs
  signale une paire menu + valeur (ex. `maxpointsmode` / `maxpoints`).

## Valider sans TouchDesigner

- Syntaxe GLSL : `glslangValidator` (apt `glslang-tools`) avec un en-tête qui
  simule les déclarations TD ; voir `glsl/tools/` dans le dépôt ImageThreading
  si présent.
- Logique : référence NumPy à côté du shader (même hash entier `uint`, mêmes
  arrondis) et comparaison des sorties.

## Vérifié en pratique (dans TD)

_(rien encore : ajouter ici chaque point confirmé par un test dans TouchDesigner,
avec la build)_
