# ImageThreading POP — Spécification

> Composant TouchDesigner (2025.3x, famille POP) qui tend un fil entre les points
> d'un nuage 3D de façon à ce que sa **projection XY** reproduise une image 2D.

Statut : spécification V1. Phase 0 (référence Python) faite ; section 5 vérifiée
contre la documentation TouchDesigner (docs.derivative.ca, octobre 2026).

---

## 1. Vision

Le composant reçoit :

- une **image 2D** (TOP) ;
- un **nuage de points 3D** (POP) qui sert de « pegs ».

Il choisit l'ordre dans lequel relier les pegs en ne regardant que leurs
coordonnées **X/Y**, puis sort le fil comme un **Line Strip POP** qui garde les
positions **XYZ d'origine**.

Le résultat est une sculpture de fils en 3D qui ne révèle l'image que depuis un
point de vue précis (vue orthographique de face). Quand on tourne autour,
l'image se défait et laisse voir la structure 3D des fils. C'est le cas d'usage
de référence du projet (le « craboutcha »).

```
            IMAGE TOP (2D)
                 │
                 ▼
          ┌──────────────┐
PEGS POP ►│ImageThreading│──► THREADS POP (Line Strip, XYZ d'origine)
 (XYZ)    │   analyse XY │
          └──────────────┘
```

Le composant :

- **ne crée pas** de points : le nombre, la position et la distribution des pegs
  viennent entièrement de l'amont (Circle POP, Grid POP, Sphere POP, bruit,
  particules…) ;
- **ne déplace pas** les points : il produit uniquement une topologie, c'est-à-dire
  une séquence d'indices de pegs ;
- **positions = POP d'entrée, connexions = ImageThreading.**

---

## 2. Crédits et licence

L'algorithme s'inspire du projet
[piellardj/image-stylization-threading](https://github.com/piellardj/image-stylization-threading)
de Jérémie Piellard. Un grand merci à lui pour son travail et son inspiration.

Ce projet-là est publié sous **GPL-3.0**. Pour que notre dépôt reste propre au
niveau licence :

- on **réimplémente** l'algorithme à partir de sa description (section 4),
  écrite avec nos propres mots ;
- **aucune ligne de code** du dépôt d'origine n'est copiée, traduite ligne à
  ligne ou incluse dans ce dépôt ;
- le README et le composant citent le projet d'origine dans une section
  « Credits / Inspiration ».

Le choix de la licence de ce dépôt (par exemple MIT) reste à faire par le
propriétaire du dépôt avant la première publication du `.tox`.

---

## 3. Interface du composant

### 3.1 Entrées et sorties

| Connecteur | Type | Rôle |
|---|---|---|
| Entrée 0 | TOP | Image cible (fixe en V1 ; l'architecture doit permettre une vidéo plus tard) |
| Entrée 1 | POP | Pegs. Seul l'attribut `P` (vec3) est obligatoire |
| Sortie 0 | POP | Fil(s) en Line Strip |

### 3.2 Paramètres

**Page `Threading`**

| Paramètre | Nom | Type | Défaut | Notes |
|---|---|---|---|---|
| Line Count | `Linecount` | int | 2000 | Nombre total de segments, tous fils confondus |
| Trails | `Trails` | int | 1 | Nombre de fils indépendants (Line Strips) |
| Line Opacity | `Lineopacity` | float | 0.1 | Contribution d'un segment au résidu (voir 4.3) |
| History Length | `Historylength` | int | 20 | Nombre de derniers pegs interdits |
| Min Peg Distance | `Minpegdist` | float | 0.2 | Distance XY minimale entre deux pegs reliés, en UV (0.2 ≈ 1/16 de tour sur un cercle inscrit) |
| Invert | `Invert` | toggle | Off | Off : fil sombre sur fond clair. On : fil clair sur fond sombre |
| Seed | `Seed` | int | 0 | Départage les égalités et le choix du premier segment |

**Page `Build`**

| Paramètre | Nom | Type | Défaut | Notes |
|---|---|---|---|---|
| Build Mode | `Buildmode` | menu | `Progressive` | `Progressive` ou `All At Once` |
| Iterations Per Frame | `Iterperframe` | int | 10 | Mode Progressive uniquement. 0 = pause |
| Step | `Step` | pulse | | Avance d'un frame, soit `Iterperframe` itérations (mode Progressive, debug ; voir 5.3) |
| Reset | `Reset` | pulse | | Repart de zéro (résidu = image, fil vide) |
| Auto Reset | `Autoreset` | toggle | On | Reset automatique quand l'image, les pegs ou un paramètre d'algorithme changent |

- **Progressive** : à chaque frame, le moteur ajoute `Iterperframe` segments
  jusqu'à atteindre `Linecount`. Le dessin se construit dans le temps.
- **All At Once** : dès qu'un recalcul est nécessaire (reset, changement d'entrée
  ou de paramètre), le moteur calcule les `Linecount` segments en une seule fois,
  puis reste figé tant que rien ne change.

**Page `Image Mapping`**

| Paramètre | Nom | Type | Défaut | Notes |
|---|---|---|---|---|
| Fit | `Fit` | menu | `Bounds` | `Bounds` : la boîte XY des pegs couvre l'image. `Manual` : utilise Scale et Offset |
| Scale | `Scale` | float2 | 1 1 | Mode Manual |
| Offset | `Offset` | float2 | 0 0 | Mode Manual |
| Aspect | `Aspect` | menu | `Fit` | `Fit`, `Fill`, `Stretch` |
| Resolution | `Resolution` | int | 256 | Résolution de travail (plus grand côté) du résidu |

**Page `Output`**

| Paramètre | Nom | Type | Défaut | Notes |
|---|---|---|---|---|
| Color | `Color` | rgb | 0 0 0 | Valeur de l'attribut `Color` (1 1 1 si Invert) |
| Output Pegs Only | `Pegsonly` | toggle | Off | Debug : sort les pegs comme points |

Évolutions prévues, hors V1 : `Projection Mode` (XY / Camera / Custom), mode RGB
avec 3 fils, image animée.

### 3.3 Topologie et attributs de sortie

- Un Line Strip par fil (`Trails` primitives).
- Un point par sommet du fil. Un peg traversé plusieurs fois donne plusieurs
  points à la même position, comme le fait le Trail POP. Chaque point recopie
  `P` (et les autres attributs utiles) du peg d'entrée correspondant.
- C'est aussi nécessaire pour la topologie : en POP, un Line Strip est
  **fermé** si l'index de point de son dernier sommet est égal à celui du
  premier. Réutiliser directement les points des pegs fermerait le fil dès
  qu'il revient à son peg de départ.

| Attribut | Classe | Type | Description |
|---|---|---|---|
| `P` | point | vec3 | Position XYZ du peg d'origine |
| `Color` | point | vec4 | Couleur du fil (alpha = Line Opacity). Nom standard POP (`Cd` est le nom SOP) |
| `PegIndex` | point | int | Index du peg dans le POP d'entrée |
| `Step` | point | int | Rang du sommet dans le fil (0, 1, 2…) |
| `StepNorm` | point | float | `Step / (longueur du fil)` ; utile pour animer l'apparition |
| `Score` | point | float | Score du segment qui arrive à ce sommet |
| `LineStripIndex` | point | int | Index du fil. Nom standard (Line Break POP, Line Metrics POP) |
| `TrailId` | primitive | int | Index du fil |

L'animation d'apparition peut aussi se faire en aval avec `StepNorm` ou
`Score`, sans recalcul.

---

## 4. Algorithme (référence, réécrite)

### 4.1 Espace image

Pour chaque peg `i` :

```
uv_i = mapping(P_i.xy)        // Z ignoré
px_i = uv_i * residualSize    // coordonnées en pixels du résidu
```

Avec `Fit = Bounds`, `mapping` normalise la boîte englobante XY des pegs sur
[0,1]², en respectant `Aspect`. Le Y n'est pas inversé : le Y du POP monte comme
le V d'une texture TouchDesigner.

### 4.2 Une seule image d'état : le résidu

Le moteur ne garde pas trois images (cible, reconstruction, erreur), mais **une
seule** :

1. Au départ, `R = luminance(image)` (en mode Invert : `1 - luminance`), à la
   résolution de travail. Un pixel sombre signifie « il faut encore du fil ici ».
2. Chaque segment choisi est **dessiné dans R en l'éclaircissant** :
   `R = min(1, R + a)` le long du segment, où `a` est la contribution d'un fil
   (dérivée de `Lineopacity`).
3. Le prochain segment est cherché là où R est encore le plus sombre.

R joue donc à la fois le rôle de la cible et celui de l'erreur restante.

Règles précises (fixées par la référence Python, à reproduire en GLSL) :

- **Échantillonnage** de R : bilinéaire, centres de pixels en `i + 0.5`. En
  dehors de l'image, `R = 1` (rien à dessiner).
- **Dessin** d'un segment : ligne de 1 px par DDA, avec un pixel par pas le long
  de l'axe principal (`n = ceil(max(|dx|, |dy|)) + 1` points arrondis au pixel).
  Chaque pixel n'est touché qu'une fois par segment, donc le GPU peut écrire
  sans conflit.
- **Égalités** : parmi les candidats ex aequo, on prend celui dont
  `wang_hash(wang_hash(Seed ^ wang_hash(itération)) ^ index)` est le plus petit
  (arithmétique `uint` 32 bits, identique en GLSL).

### 4.3 Score d'un segment candidat

Pour un segment entre les pegs `A` et `B` (en pixels du résidu) :

```
n = max(1, ceil(longueur(A, B)))       // environ 1 échantillon par pixel
pour k = 1..n :
    t  = k / (n + 1)
    p  = mix(A, B, t)
    s += 0.5 - (R_bilinéaire(p) + a)   // "obscurité restante" après ajout du fil
score = s / n
```

- Le score est une **moyenne** : il ne favorise pas les segments longs.
- `+ a` pénalise les segments qui passent sur des zones déjà assez claires.
- La valeur 0.5 correspond au gris moyen. Elle déplace le score sans changer
  quel candidat est le meilleur ; elle est gardée pour que les scores restent
  lisibles en debug.

### 4.4 Choix glouton du peg suivant

Depuis le peg courant `c` d'un fil :

```
pour chaque peg j :
    exclure si j est dans les Historylength derniers pegs de ce fil
    exclure si distance_uv(c, j) < Minpegdist
    score_j = score(c, j)
meilleur = argmax(score_j)
égalités : départage pseudo-aléatoire (hash(Seed, itération, j))
```

Puis :

1. ajouter `meilleur` au fil ;
2. dessiner le segment `c → meilleur` dans R ;
3. `c = meilleur`.

### 4.5 Premier segment d'un fil

Il n'y a pas de peg courant au départ. On cherche donc la meilleure paire
`(i, j)` sur un **sous-échantillon** des pegs (un peg sur `1 + N/100`), avec les
mêmes exclusions, et on démarre le fil avec ces deux pegs.

### 4.6 Plusieurs fils (`Trails > 1`)

- Les segments sont répartis à tour de rôle entre les fils (fil 0, fil 1, …,
  fil 0, …) : `Linecount` reste le total.
- Tous les fils partagent le même résidu R.
- L'historique est propre à chaque fil.

### 4.7 Différences volontaires avec le projet d'origine

- Les pegs viennent d'un POP quelconque, pas d'un cercle ou d'un rectangle
  généré.
- La règle des « pegs trop proches » est une distance XY en UV, et non une
  distance angulaire (qui n'a pas de sens pour un nuage arbitraire).
- Le hasard est reproductible grâce à `Seed`.
- Le moteur tourne sur GPU.

---

## 5. Architecture TouchDesigner

Cette section a été vérifiée contre la documentation de TouchDesigner 2025.3x
(docs.derivative.ca : *GLSL POP*, *GLSL Advanced POP*, *Write a GLSL POP*,
*Feedback POP*, *TOP to POP*, *POP to TOP*, *Trail POP*, *Line Break POP*,
*Analyze POP*, *Topology POP*, *Learning About POPs*, *Write a GLSL TOP*). La
section 5.6 résume ce qui a changé par rapport à la première proposition.

### 5.1 Contraintes

- L'algorithme est **séquentiel d'une itération à l'autre** (chaque choix
  modifie R), mais le score des N candidats d'une même itération est
  **parallèle**.
- Il faut un **état persistant** entre les frames (R, peg courant, historique,
  chemin), qu'on doit pouvoir réinitialiser.
- On ne veut **aucun aller-retour CPU** par itération.

### 5.2 Idée centrale : K itérations dans un seul workgroup

Le moteur est un **GLSL POP** (pas un GLSL Advanced POP, voir 5.6) réglé ainsi :

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Attribute Class | `Point` | L'état est une liste de points de taille fixe |
| Number of Threads | `Manual` | Seul mode qui fixe la taille et le nombre de workgroups |
| Work Group Size | `256 1 1` (ou 1024) | Threads qui coopèrent sur une itération |
| Dispatch Size | `1 1 1` | **Un seul workgroup** : `barrier()` synchronise tout le monde |
| Output Attributes | `R Path Counters` | Attributs de l'état modifiés par le shader |
| Output Access | `Read-Write` | Le shader relit ce qu'il vient d'écrire (et autorise les atomics) |
| Initialize Output Attributes | `On` | Copie l'état d'entrée vers la sortie avant le shader |
| Passes | P | Découpe le calcul en P dispatchs de K itérations |

En mode `Manual`, `TDIndex()` et `TDNumElements()` ne sont **pas définis**
(erreur de compilation) : le shader utilise `gl_LocalInvocationIndex` et
`gl_WorkGroupSize`. Il lit et écrit uniquement les tableaux de sortie (`R[]`,
`Path[]`, `Counters[]`) ; les pegs sont lus sur l'entrée 1 avec
`TDIn_P(1, j)` / `TDIn_PegUV(1, j)` et leur nombre avec `TDInputNumPoints(1)`.

Chaque pass exécute K itérations :

```
répéter K fois :
    1. chaque thread score un sous-ensemble des pegs candidats
    2. réduction en shared memory → meilleur candidat (score max, puis hash min)
    3. barrier()
    4. les threads dessinent ensemble le segment choisi dans R[]
       (chaque thread traite une partie des pixels du segment, sans conflit)
    5. memoryBarrierBuffer() + barrier()
    6. le thread 0 ajoute le peg au chemin et met à jour les compteurs
```

- **Progressive** : 1 pass de K = `Iterperframe` itérations par frame, dans une
  boucle Feedback POP (5.3).
- **All At Once** : pas de Feedback POP. Le moteur part directement de l'état
  initial avec P = `ceil(Linecount / K)` passes (K interne, par exemple 100).
  Découper en passes évite un dispatch unique de plusieurs secondes, qui
  risquerait de déclencher le watchdog GPU (TDR, environ 2 s sous Windows).

Uniforms : page `Vectors` (valeurs nommées : K, Linecount, Trails,
Historylength, Minpegdist, a, Seed, W, H…), page `Constants` pour les
constantes de spécialisation (taille max de l'historique par exemple).

Ordre de grandeur : avec 500 pegs et R de 256 px, environ 500 × 256 lectures
par itération. Un seul workgroup n'occupe qu'une unité de calcul du GPU, donc
3000 itérations devraient prendre de l'ordre de 0,1 à 1 s (à mesurer en
phase 8 ; l'alternative multi-workgroup est notée en 5.5).

### 5.3 Réseau interne

```
ImageThreading (Base COMP, In TOP + In POP → Out POP)
│
├── in_image            In TOP
├── in_pegs             In POP
│
│   Mapping des pegs (phase 1)
├── pegs_bounds         Analyze POP : Min / Max de P (un seul point, reste sur GPU)
├── pegs_uv             GLSL POP (Point) : entrée 0 = pegs, entrée 1 = pegs_bounds
│                         crée PegUV (vec2) selon Fit / Aspect / Scale / Offset
│
│   État initial (phase 3)
├── image_prep          TOP : Monochrome/Level (+ Invert) → résolution de travail W × H
├── residual_init       TOP to POP : First RGBA Contains = Custom, canal r → attribut R,
│                         Filter = Nearest, Pixel Sampling = Pixel Centered,
│                         Connectivity = None. Dimension W × H
├── state_init          GLSL POP / Attribute POP : ajoute Path (int, -1) et Counters (int, 0)
│
│   Moteur (phases 4 à 7)
├── state_fb            Feedback POP, Target POP = state_out        ┐
├── engine_progressive  GLSL POP, 1 pass, K = Iterperframe           │ Progressive
├── state_out           Null POP                                     ┘
├── engine_allatonce    GLSL POP, même DAT, entrée = state_init,      All At Once
│                         P = ceil(Linecount / K) passes
├── state_select        Switch POP selon Buildmode
│
│   Sortie (phase 2)
├── threads_points      GLSL Advanced POP : Max Points = Trails × M,
│                         Number of Threads = Per Max Output Point
│                         entrée 0 = état (Path, Counters), entrée 1 = pegs_uv
│                         écrit P, Color, PegIndex, Step, StepNorm, Score, LineStripIndex
├── threads_strips      Line Break POP : mode Line Strip Index Attribute → un Line Strip par fil
├── out_threads         Out POP
│
│   Debug
├── residual_debug      POP to TOP : Layout = POP Dimension, attribut R
│
├── shaders             Text DAT : engine.comp, build_threads.comp, pegs_uv.comp
└── ext_logic           Extension Python : Reset, Step, Auto Reset, Build Mode
```

**Représentation de l'état** (une seule liste de points de taille fixe S = W × H,
celle du TOP to POP) :

| Attribut | Type | Contenu |
|---|---|---|
| `R` | float | Résidu. Pixel (x, y) au point `y × W + x` (voir 5.5 pour le sens des lignes) |
| `Path` | int | Chemins. Le fil t occupe les points `[t × M, (t + 1) × M)`, avec `M = ceil(Linecount / Trails) + 1`. `-1` = vide |
| `Counters` | int | Compteurs dans les premiers points : nombre de segments, itération, longueur de chaque fil, fils bloqués. Disposition exacte fixée en phase 4 |
| `Score` | float | Score du segment arrivant à chaque entrée de `Path` (même indexation) |

Contrainte : `Trails × M ≤ W × H` (65 536 à 256 × 256, très au-dessus de
`Linecount` = 2000). L'extension refuse ou borne `Linecount` sinon.

**Boucle Feedback POP** (API réelle) :

- Le Feedback POP n'a **pas** de paramètre Reset. Il a `Target POP`,
  `Initialize` (pulse : prend un instantané de l'entrée, puis attend),
  `Start` (pulse ; seul, il prend l'instantané et démarre), `Play` (lecture /
  pause) avec un mode « Step Pulse » qui avance d'un seul frame, et
  `Go to Done`. Un Info CHOP donne les canaux `initializing`, `ready`,
  `running`, `done`.
- **Reset** = l'extension pulse `Initialize` puis `Start` sur `state_fb`.
- **Pause** = `Play` à Off. La doc précise que cela arrête aussi le cook des
  nœuds de la boucle, ce qui satisfait le critère « aucun recalcul quand rien
  ne change ».
- **Step** = le Step Pulse du Feedback POP : avance d'**un frame**, soit
  `Iterperframe` itérations (mettre `Iterperframe = 1` pour avancer d'une
  itération).
- **Fin du calcul** : le nombre de frames nécessaires est connu sur CPU
  (`ceil(Linecount / Iterperframe)` si aucun fil n'est bloqué) ; l'extension
  met `Play` à Off une fois ce nombre atteint, sans relire le GPU. Le shader
  s'arrête de toute façon à `Linecount`.
- **Auto Reset** : le Feedback POP ne reprend pas l'instantané tout seul quand
  son entrée change. L'extension surveille l'image, les pegs et les paramètres
  d'algorithme et déclenche Reset.

**Sortie Line Strip** (phase 2) : `threads_points` produit un point par entrée
de `Path` (Trails × M points, nombre fixe et connu sur CPU), recopie `P` du peg
correspondant et écrit `LineStripIndex = t`. Le **Line Break POP** en mode
« Line Strip Index Attribute » en fait un Line Strip par fil. Les entrées pas
encore calculées (mode Progressive) répètent le dernier sommet valide : segments
de longueur nulle, invisibles, et topologie constante. `TrailId` (primitive) est
ajouté après le Line Break POP par un GLSL POP en classe Primitive (index de
primitive = index du fil).

Alternative plus compacte, à garder pour la phase 8 : écrire directement le
tampon d'index dans le GLSL Advanced POP (`I[]`, séparateur `cTDPrimIndexRestart`
= 0xFFFFFFFF entre les fils, `Max Line Strips` / `Max Line Strip Verts` en
Custom, `Line Strip Info Update = Auto`).

### 5.4 Fonctions GLSL utiles (doc *Write a GLSL POP*)

| Besoin | GLSL POP | GLSL Advanced POP |
|---|---|---|
| Lire un attribut d'une entrée | `TDIn_Attr(input, id)` | `TDInPoint_Attr(input, id)`, `TDInPrim_…`, `TDInVert_…` |
| Écrire un attribut | `Attr[id]` (tableau, compatible atomics) | `oTDPoint_Attr[id]`, `oTDPrim_…`, `oTDVert_…` |
| Nombre d'éléments d'une entrée | `TDInputNumPoints(input)` | idem |
| Index / nombre de threads | `TDIndex()`, `TDNumElements()` (pas en mode Manual) | idem |
| Dimension (W × H du TOP to POP) | `TDDimension()`, `TDDimCoords(i)`, `TDDimPointIndex(c)` | idem |
| Lire un TOP | page `Samplers` (nom, TOP, Extend, Filter) | idem |
| Index buffer en écriture | non | `I[]` si un `Max …` est en Custom |

Nouveaux attributs : page `Create Attribs` (classe, nom, type, valeur par
défaut). Ils ne sont pas initialisés si `Initialize Output Attributes` est Off.

### 5.5 Points que la documentation ne tranche pas (à tester en premier)

1. **`shared`, `barrier()`, `memoryBarrierBuffer()`** : GLSL 4.60 standard en
   compute shader, mais la doc TouchDesigner n'en parle pas, et c'est
   TouchDesigner qui génère le `layout(local_size_…)` à partir de
   `Work Group Size`. Premier test de la phase 4 : une réduction en shared
   memory sur un workgroup.
2. **Persistance des tableaux de sortie d'une pass à l'autre** (GLSL POP,
   `Copy Previous Pass Output to Input` = Off). La doc le laisse entendre
   (« initialisées pendant la première pass d'un POP multi-pass ») sans le
   dire. Sinon : activer `Copy Previous Pass Output to Input`.
3. **Passes sur le GLSL Advanced POP** : la page des paramètres liste
   `Passes`, mais *Write a GLSL POP* dit que c'est réservé au GLSL POP. On ne
   compte pas dessus.
4. **Sens des lignes du TOP to POP** : la doc dit que les W premiers points
   forment la première ligne, mais pas si c'est la ligne du bas (convention
   des textures TouchDesigner, qui correspond à la référence Python). À
   vérifier en phase 3 avec une image test asymétrique.
5. **Types `int` dans `Create Attribs`** et nom personnalisé `R` dans le
   TOP to POP (mode Custom).
6. **Ordre des points dans le Line Break POP** : on suppose que l'ordre des
   points est conservé à l'intérieur de chaque Line Strip.

Repli si le stockage de R dans un POP s'avère trop lent : **GLSL TOP en mode
compute** dans une boucle Feedback TOP. Depuis 2025.30000, on y lit et écrit la
sortie avec `TDImageLoadOutput()` / `TDImageStoreOutput()`, et on lit les
attributs des pegs avec `TDBuffer_Attr()` (page `Buffers`). Le moteur produit
alors un petit TOP « chemin » relu par `threads_points`.

Autre piste d'optimisation (phase 8) : plusieurs workgroups pour le score
(un dispatch « score » large + un dispatch « réduction + dessin »), au prix de
deux dispatchs par itération.

### 5.6 Corrections par rapport à la première proposition

| Première version | Correction | Source |
|---|---|---|
| Moteur = GLSL Advanced POP en « single shader dispatch » | Moteur = **GLSL POP** (classe Point), Number of Threads = Manual, Dispatch Size = 1 1 1. Il ne change pas le nombre d'éléments et a besoin de `Passes`, réservé au GLSL POP | *Write a GLSL POP* |
| All At Once = K = Linecount dans un seul dispatch | All At Once = plusieurs **passes** de K itérations dans un seul cook, sans Feedback POP | Paramètre `Passes` ; risque TDR |
| Le Feedback POP se réinitialise par un « Reset » | Pas de Reset : `Initialize` + `Start` en pulse, `Play` Off = pause (et arrêt du cook), mode Step Pulse = un frame | *Feedback POP* |
| Step = une itération | Step = un frame (`Iterperframe` itérations) | *Feedback POP* |
| `state_init` = Switch/Merge selon Reset | L'instantané est pris par le Feedback POP lui-même ; le Switch sert à choisir Progressive / All At Once | *Feedback POP* |
| R = attribut float, sans précision sur l'organisation | R sur une liste de points de dimension W × H ; chemins et compteurs dans des attributs de la même liste (taille unique) | *TOP to POP*, *Dimension* |
| Sortie : `Max Line Strips` / `Max Line Strip Verts` dans le GLSL Advanced POP | Sortie : GLSL Advanced POP (`Max Points` = Custom) qui écrit les points + **Line Break POP** (`LineStripIndex`). L'écriture directe de l'index buffer reste une option | *GLSL Advanced POP*, *Line Break POP* |
| Attribut couleur `Cd` | **`Color`** (float4) : `Cd` est le nom SOP | *Learning About POPs* |
| — | Ajout de `LineStripIndex` (nom standard utilisé par Line Break POP et Line Metrics POP) | *Learning About POPs* |
| Mapping XY → UV non précisé côté TD | Analyze POP (Min / Max de P, reste sur GPU) + GLSL POP qui crée `PegUV` | *Analyze POP* |
| Un point par sommet « comme le Trail POP » | Confirmé, et nécessaire : un Line Strip est fermé si son dernier index de point égale le premier | *Learning About POPs* |

Le Trail POP n'impose pas de nom d'attribut utile ici (il crée `Age` et des
attributs d'orientation) ; on garde `Step`, `StepNorm`, `Score`, `PegIndex`.

### 5.7 Référence CPU

Implémentée dans [`python/reference.py`](../python/reference.py) (NumPy + Pillow) :

```
pip install -r python/requirements.txt
python python/reference.py portrait.jpg --pegs-circle 200 --lines 3000 --opacity 0.08 --out out/portrait
python python/reference.py letter --lines 1500 --out out/letter        # images de test : disk, gradient, letter
python python/reference.py portrait.jpg --pegs-file pegs.csv --trails 3 --seed 7 --out out/sculpture
```

`--pegs-file` accepte un CSV `x,y,z` (par exemple exporté depuis un POP) ou un
`.npy`. Sorties : `.json` (pegs, chemins, scores), `_render.png` (vue de face),
`_residual.png` (R final) et `.obj` (polylignes 3D avec le XYZ d'origine, à
ouvrir dans n'importe quel viewer pour tester l'effet « craboutcha »).

Mesures indicatives (CPU, un cœur) : 250 pegs × 3000 lignes ≈ 10 s,
400 pegs × 3000 lignes ≈ 14 s.

Un script Python/NumPy autonome (`python/reference.py`, hors TouchDesigner)
implémente la section 4 à l'identique. Il sert à :

- valider l'algorithme sur des images de test ;
- comparer les chemins avec le moteur GLSL (avec la même Seed et les mêmes
  paramètres, le chemin doit être le même ou très proche) ;
- produire des images de référence pour la documentation.

---

## 6. Plan de développement

Chaque phase est validée visuellement avant de passer à la suivante.

| Phase | Contenu | Critère de validation |
|---|---|---|
| 0 | Référence Python/NumPy (section 5.7) | Un portrait reconnaissable avec 200 pegs en cercle et 3000 lignes |
| 1 | Coquille du COMP : entrées/sorties, paramètres, mapping XY → UV, sortie « pegs only » | Les pegs s'affichent en UV par-dessus l'image |
| 2 | Sortie Line Strip à partir d'un chemin aléatoire | Topologie correcte, XYZ conservés, attributs présents |
| 3 | Résidu R (TOP to POP) + debug POP to TOP | R affiché, identique à l'image en luminance, lignes dans le bon sens |
| 4 | Test shared memory / barrier (5.5), puis score + argmax pour **une** itération | Même choix que la référence Python |
| 5 | Boucle K itérations + dessin dans R + Feedback POP | Mode Progressive fonctionnel, Reset et Step OK |
| 6 | Mode All At Once + Auto Reset | Recalcul uniquement quand quelque chose change |
| 7 | Trails > 1, Seed, Invert | Variantes reproductibles |
| 8 | Profilage et optimisation | Mesures documentées |
| 9 | Exemple « craboutcha » : pegs en Sphere POP ou Grid POP + bruit en Z, caméra orbitale | L'image apparaît seulement de face |

### Images de test (dans cet ordre)

1. Fond blanc, disque noir
2. Dégradé horizontal
3. Une lettre
4. Un portrait

---

## 7. Critères de réussite V1

1. Un TOP et un POP quelconques peuvent être branchés.
2. La sortie est un Line Strip POP dont les positions sont exactement celles des
   pegs d'entrée (Z conservé).
3. Vue de face en orthographique, l'image est reconnaissable ; augmenter
   `Linecount` améliore la ressemblance.
4. Les modes Progressive et All At Once fonctionnent ; `Iterperframe = 0` met en
   pause.
5. Reset, Step et Seed fonctionnent ; le résultat est reproductible.
6. Aucun recalcul quand rien ne change.
7. Le moteur ne fait aucun aller-retour CPU par itération.

---

## 8. Structure du dépôt (proposée)

```
TD_POP_image-threading/
├── README.md
├── docs/
│   └── SPEC.md            ← ce document
├── glsl/
│   ├── pegs_uv.comp       mapping XY → PegUV
│   ├── engine.comp        moteur (score, argmax, dessin)
│   └── build_threads.comp chemin → points du fil (avant Line Break POP)
├── python/
│   ├── reference.py       référence CPU NumPy
│   └── ext_imagethreading.py  extension du COMP
├── td/
│   └── ImageThreading.tox
└── examples/
    └── craboutcha.toe
```
