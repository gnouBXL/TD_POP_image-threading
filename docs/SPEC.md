# ImageThreading POP — Spécification

> Composant TouchDesigner (2025.3x, famille POP) qui tend un fil entre les points
> d'un nuage 3D de façon à ce que sa **projection XY** reproduise une image 2D.

Statut : spécification V1, avant implémentation.

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
| Step | `Step` | pulse | | Ajoute une itération (mode Progressive, debug) |
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
| Color | `Color` | rgb | 0 0 0 | Valeur de `Cd` (1 1 1 si Invert) |
| Output Pegs Only | `Pegsonly` | toggle | Off | Debug : sort les pegs comme points |

Évolutions prévues, hors V1 : `Projection Mode` (XY / Camera / Custom), mode RGB
avec 3 fils, image animée.

### 3.3 Topologie et attributs de sortie

- Un Line Strip par fil (`Trails` primitives).
- Un point par sommet du fil. Un peg traversé plusieurs fois donne plusieurs
  points à la même position, comme le fait le Trail POP. Chaque point recopie
  `P` (et les autres attributs utiles) du peg d'entrée correspondant.

| Attribut | Classe | Type | Description |
|---|---|---|---|
| `P` | point | vec3 | Position XYZ du peg d'origine |
| `Cd` | point | vec4 | Couleur du fil (alpha = Line Opacity) |
| `PegIndex` | point | int | Index du peg dans le POP d'entrée |
| `Step` | point | int | Rang du sommet dans le fil (0, 1, 2…) |
| `StepNorm` | point | float | `Step / (longueur du fil)` ; utile pour animer l'apparition |
| `Score` | point | float | Score du segment qui arrive à ce sommet |
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

### 5.1 Contraintes

- L'algorithme est **séquentiel d'une itération à l'autre** (chaque choix
  modifie R), mais le score des N candidats d'une même itération est
  **parallèle**.
- Il faut un **état persistant** entre les frames (R, peg courant, historique,
  chemin), qu'on doit pouvoir réinitialiser.
- On ne veut **aucun aller-retour CPU** par itération.

### 5.2 Idée centrale : une boucle dans un seul dispatch

Un compute shader lancé avec **un seul workgroup** (par exemple 256 ou 1024
threads) effectue K itérations à la suite :

```
répéter K fois :
    1. chaque thread score un sous-ensemble des pegs candidats
    2. réduction en shared memory → meilleur candidat (score max, index)
    3. barrier()
    4. les threads dessinent ensemble le segment choisi dans R
       (chaque thread traite une partie des échantillons du segment)
    5. barrier() + memoryBarrierBuffer()
    6. le thread 0 ajoute le peg au chemin et met à jour l'historique
```

- **Progressive** : K = `Iterperframe`.
- **All At Once** : K = `Linecount` dans un seul cook.

Ordre de grandeur : avec 500 pegs et R de 256 px, on fait environ 500 × 256
lectures par itération, ce qui va très vite sur un GPU. 3000 itérations en All
At Once devraient prendre de quelques dizaines à quelques centaines de
millisecondes (à mesurer).

### 5.3 Réseau interne (proposition)

```
ImageThreading (Base COMP, POP in/out)
│
├── in_image   (In TOP)
├── in_pegs    (In POP)
│
├── image_prep          TOP : Level/Monochrome + Fit → résolution de travail
├── residual_init       TOP to POP : un point par pixel, attribut R
│
├── state_feedback      Feedback POP  ── état de la frame précédente
├── state_init          (Switch/Merge) : choisit init ou feedback selon Reset
├── engine              GLSL Advanced POP (single dispatch)
│                         entrée 0 : état (R + chemin + compteurs)
│                         entrée 1 : pegs (P, uv)
│                         uniforms : K, Linecount, Historylength, Minpegdist, a, Seed…
├── state_out           Null POP (cible du Feedback POP)
│
├── threads_build       GLSL Advanced / GLSL Copy POP :
│                         chemin + pegs → Line Strip(s) avec P d'origine
├── out_threads         Out POP
│
└── ext_logic           Execute DAT / extension Python :
                          Reset, Step, Auto Reset, Build Mode
```

Représentation de l'état (à confirmer pendant la phase 1) :

- **R** : attribut float sur `W × H` points (venant de TOP to POP), écrit en
  place par le shader.
- **Chemin** : attribut int sur un tableau de `Linecount + Trails` éléments,
  plus des compteurs (itération courante, peg courant par fil).
- **Debug** : R peut être rendu en TOP (POP to TOP) pour afficher le résidu.

### 5.4 Points à vérifier dans la documentation TouchDesigner

Ces points conditionnent le code GLSL. Il faut les vérifier dans
docs.derivative.ca avant d'écrire le shader :

1. **GLSL Advanced POP** :
   - le mode « single shader dispatch » ;
   - comment fixer le nombre de workgroups à 1 et leur taille ;
   - la disponibilité de `shared`, `barrier()` et des atomics ;
   - la lecture et l'écriture d'attributs de plusieurs classes ;
   - comment déclarer de nouveaux attributs en sortie ;
   - comment fixer un nombre de points ou de Line Strips différent de l'entrée
     (paramètres `Max Line Strips` et `Max Line Strip Verts`).
2. **Write GLSL POPs** : les fonctions intégrées (`TDIndex()`, accès aux
   attributs des entrées 0 et 1, nombre d'éléments, uniforms, samplers TOP).
3. **Feedback POP** : Initialize, Start, et réinitialisation par script.
4. **TOP to POP** : l'attribut produit et l'ordre des points (ligne par ligne ?).
5. **Trail POP** : les noms d'attributs standard, pour rester cohérent avec
   l'écosystème.

Si le stockage de R dans un POP s'avère trop lourd, l'alternative est un
**GLSL TOP en mode compute** (`imageLoad`/`imageStore`) dans une boucle
Feedback TOP. Le moteur produit alors un petit TOP « chemin » qui est relu par
le GLSL POP de sortie.

### 5.5 Référence CPU

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
| 0 | Référence Python/NumPy (section 5.5) | Un portrait reconnaissable avec 200 pegs en cercle et 3000 lignes |
| 1 | Coquille du COMP : entrées/sorties, paramètres, mapping XY → UV, sortie « pegs only » | Les pegs s'affichent en UV par-dessus l'image |
| 2 | Sortie Line Strip à partir d'un chemin aléatoire | Topologie correcte, XYZ conservés, attributs présents |
| 3 | Résidu R (TOP to POP) + debug POP to TOP | R affiché, identique à l'image en luminance |
| 4 | Shader : score + argmax pour **une** itération | Même choix que la référence Python |
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
│   ├── engine.comp        moteur (score, argmax, dessin)
│   └── build_threads.comp chemin → Line Strip
├── python/
│   ├── reference.py       référence CPU NumPy
│   └── ext_imagethreading.py  extension du COMP
├── td/
│   └── ImageThreading.tox
└── examples/
    └── craboutcha.toe
```
