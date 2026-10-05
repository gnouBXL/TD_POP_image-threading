# TD_POP_image-threading

**ImageThreading POP** est un composant TouchDesigner (2025.3x, POPs) qui tend un fil
entre les points d'un nuage 3D de façon à ce que sa projection XY reproduise une
image 2D.

- Entrée 0 : une image (TOP)
- Entrée 1 : des pegs (POP, positions 3D quelconques)
- Sortie : un ou plusieurs Line Strips (POP) qui gardent les positions XYZ d'origine

Vu de face, le fil révèle l'image. Quand on tourne autour, on ne voit plus que la
sculpture de fils.

Statut : spécification, avant implémentation. Voir [docs/SPEC.md](docs/SPEC.md).

## Credits / Inspiration

L'algorithme s'inspire de
[image-stylization-threading](https://github.com/piellardj/image-stylization-threading)
de Jérémie Piellard. Merci à lui pour ce travail et cette inspiration.
Ce dépôt ne contient aucun code issu de ce projet : l'algorithme est réimplémenté
à partir de sa description.
