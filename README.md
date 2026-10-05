# TD_POP_image-threading

**ImageThreading POP** est un composant TouchDesigner (2025.3x, POPs) qui tend un fil
entre les points d'un nuage 3D de façon à ce que sa projection XY reproduise une
image 2D.

- Entrée 0 : une image (TOP)
- Entrée 1 : des pegs (POP, positions 3D quelconques)
- Sortie : un ou plusieurs Line Strips (POP) qui gardent les positions XYZ d'origine

Vu de face, le fil révèle l'image. Quand on tourne autour, on ne voit plus que la
sculpture de fils.

Statut : référence Python (phase 0) faite, architecture TouchDesigner vérifiée
contre la documentation officielle, phases 1-2 écrites (à tester dans
TouchDesigner). Voir [docs/SPEC.md](docs/SPEC.md).

## Construire le composant dans TouchDesigner (phases 1-2)

1. Dans TouchDesigner 2025.3x, créer un **Text DAT** et mettre son paramètre
   **File** sur `td/build_imagethreading.py` (chemin complet vers ce dépôt).
2. Clic droit sur le DAT > **Run Script**.

Le script crée `ImageThreading` (paramètres custom, réseau interne, shaders
chargés depuis `glsl/` en Text DAT synchronisés) et une petite démo :
`demo_image` (Movie File In) et `demo_pegs` (Circle POP, 200 points).

Il construit aussi un **réseau de rendu** à côté (opérateurs `view_*`) :

- `view_front` : vue de face orthographique, cadrée sur l'image. C'est là que
  l'image doit apparaître.
- `view_orbit` : caméra qui tourne autour de la sculpture (15° par seconde ;
  vitesse dans l'expression de `view_cam_orbit`).
- `view_geo` (Geometry COMP), `view_mat` (Line MAT, transparence = Line
  Opacity), `view_cam_front`, `view_cam_orbit`, `view_target`. Pas de
  lumière : les fils sont des lignes non éclairées.

Le viewer du nœud `ImageThreading` lui-même reste noir : une Base COMP
n'affiche pas la géométrie qu'elle sort. Regarder `view_front` / `view_orbit`.

Vérifications :

- **Phase 1** : le TOP `ImageThreading/debug_overlay` montre les pegs (points
  rouges) en UV par-dessus l'image. `Output Pegs Only` sort les pegs.
- **Phase 2** : avec `Debug > Random Path` activé, la sortie est un chemin
  aléatoire en Line Strips : `Trails` primitives, positions XYZ des pegs,
  attributs `Color`, `PegIndex`, `Step`, `StepNorm`, `Score`,
  `LineStripIndex`, `TrailId`.

Si un menu n'a pas l'entrée attendue, le script s'arrête avec un message qui
liste les entrées disponibles : il suffit de le copier pour corriger le
script.

Vérifier la syntaxe des shaders hors TouchDesigner :
`python glsl/tools/check_glsl.py` (demande `glslangValidator`).

## Credits / Inspiration

L'algorithme s'inspire de
[image-stylization-threading](https://github.com/piellardj/image-stylization-threading)
de Jérémie Piellard. Merci à lui pour ce travail et cette inspiration.
Ce dépôt ne contient aucun code issu de ce projet : l'algorithme est réimplémenté
à partir de sa description.
