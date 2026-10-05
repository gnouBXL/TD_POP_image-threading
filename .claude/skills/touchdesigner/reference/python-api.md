# API Python TouchDesigner (2025.3x) — aide-mémoire

Source : pages *OP Class*, *COMP Class*, *Page Class*, *Par Class*, *ParGroup
Class*, *Sequence Class*, *Connector Class*, *POP Class*, *Extensions*,
*Parameter Execute DAT*, *COMP Extensions Page*. Détails :
`td_doc.py methods "<X> Class"`.

## Opérateurs

```python
n = comp.create(glslPOP, 'engine')     # create(opType, name, initialize=True) ; opType = classe Python
                                       # (voir `opType` dans pops-index.md : glslPOP, toptoPOP, feedbackPOP,
                                       #  linebreakPOP, analyzePOP, nullPOP, inPOP, outPOP, switchPOP…)
                                       # TOP/DAT/COMP classiques : inTOP, nullTOP, glslTOP, textDAT,
                                       #  parameterexecuteDAT, executeDAT, baseCOMP, geometryCOMP…
comp.copy(other, name='x')             # copie
n.destroy()
comp.findChildren(type=glslPOP, depth=1)
op('engine'), comp.op('engine'), parent(), me, ipar (paramètres de l'ancêtre « Parent Shortcut »)
n.nodeX, n.nodeY = 0, -200             # position dans l'éditeur
n.color = (0.3, 0.5, 0.3); n.comment = '...'
n.inputs, n.outputs                     # listes d'OPs
n.errors(recurse=True), n.warnings()    # diagnostic après cook
n.cook(force=True)
n.store(key, val) / n.fetch(key, default)  # stockage persistant dans le .toe
```

Câblage (*Connector Class* : `connect(target)`, `disconnect()`, `connections`) :

```python
b.inputConnectors[0].connect(a)        # a → entrée 0 de b
a.outputConnectors[0].connect(b)       # équivalent
b.inputConnectors[1].connect(pegs)     # entrée 1
```

## Paramètres

```python
n.par.computedat = 'engine_comp'       # valeur (chemin relatif pour un paramètre OP/DAT)
n.par.npasses.expr = 'parent().par.Linecount // 100'   # expression Python
n.par.npasses.mode = ParMode.EXPRESSION # CONSTANT | EXPRESSION | EXPORT | BIND
n.par.play.bindExpr = "parent().par.Play"
n.par.initializepulse.pulse()          # pulse (frames=…, seconds=… possibles)
n.par.numthreadsmode = 'manual'        # menu : nom (menuNames) ; menuLabels / menuIndex aussi
n.pars('vec*')                          # recherche par motif
p.eval(), p.default, p.isDefault, p.menuNames, p.menuLabels, p.tuplet, p.parGroup
```

Paramètres « séquence » (blocs répétés : vec, sampler, attr, input…) :

```python
n.seq.vec.numBlocks = 3                 # (Sequence Class) ; aussi n.par.vec0name.sequence
n.par.vec0name = 'uK';  n.par.vec0type = 'int'; n.par.vec0valuex = 10
n.par.vec1name = 'uSeed'
n.par.attr0name = ...                   # paires menu + valeur (attr0name/attr0customname) :
                                        # choisir l'entrée « custom » du menu puis remplir le nom
```

Helper robuste pour les menus dont le nom interne n'est pas documenté :

```python
def set_menu(par, *wanted):
    """Choisit une entrée par nom ou libellé (insensible à la casse, sous-chaîne)."""
    for w in wanted:
        w = w.lower()
        for name, label in zip(par.menuNames, par.menuLabels):
            if w == name.lower() or w == label.lower():
                par.val = name; return name
        for name, label in zip(par.menuNames, par.menuLabels):
            if w in name.lower() or w in label.lower():
                par.val = name; return name
    raise ValueError(f'{par.owner.path}.{par.name}: aucune entrée {wanted} dans {list(par.menuLabels)}')
```

## Paramètres custom (Page Class)

```python
page = comp.appendCustomPage('Threading')          # COMP Class
pg = page.appendInt('Linecount', label='Line Count')  # renvoie un ParGroup
pg.default = 2000; pg.min = 1; pg.max = 20000; pg.clampMin = True; pg.normMax = 10000
comp.par.Linecount = 2000                          # valeur courante (≠ default)
page.appendFloat('Scale', size=2)                  # size → tuplet Scalex/Scaley ? (suffixes : voir pg.suffixes)
page.appendXY('Offset'); page.appendRGB('Color'); page.appendToggle('Invert')
page.appendPulse('Reset'); page.appendMenu('Buildmode', label='Build Mode')
pg = comp.par.Buildmode.parGroup ; pg.menuNames = ['progressive', 'allatonce']; pg.menuLabels = [...]
page.appendTOP / appendPOP / appendDAT / appendOP / appendStr / appendFile / appendHeader / appendSequence
comp.sortCustomPages(p1, p2); page.destroy()
```

- Les noms de paramètres custom commencent par une majuscule suivie de
  minuscules/chiffres (`Linecount`, `Iterperframe`).
- `appendXY('Offset')` crée `Offsetx`, `Offsety` ; `appendRGB('Color')` crée
  `Colorr/g/b` ; `appendFloat(size=2)` crée des suffixes 1/2 (vérifier avec
  `pg.suffixes`).

## Extensions

Page Extensions d'un COMP : séquence `ext` → `ext0object`, `ext0name`,
`ext0promote` ; `reinitextensions` (pulse), `initextonstart`.

```python
comp.par.ext0object = "op('./ext_imagethreading').module.ImageThreadingExt(me)"
comp.par.ext0promote = True       # membres en Majuscule accessibles : comp.Reset()
comp.par.reinitextensions.pulse()

class ImageThreadingExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp
    def onInitTD(self): ...        # fin de la frame d'init (le COMP est prêt)
    def onDestroyTD(self): ...     # avant ré-init
    def Reset(self): ...            # promu
```

Accès : `comp.ext.ImageThreadingExt.Reset()`, ou `ext.ImageThreadingExt` depuis
n'importe quel opérateur à l'intérieur (recherche vers le haut).

## Callbacks

**Parameter Execute DAT** (`parameterexecuteDAT`) : paramètres `op`, `pars`,
`custom`, `builtin`, `valuechange`, `onpulse`, `expressionchange`,
`exportchange`, `enablechange`, `modechange`, `valueschanged`, `active`.

```python
def onValueChange(par, prev): ...
def onValuesChanged(changes): ...   # changes : liste avec .par et .prev
def onPulse(par): ...
```

Autres : Execute DAT (`onFrameStart(frame)`, `onStart()`, `onCreate()`), OP
Execute DAT (cook, changement d'entrées…), CHOP Execute DAT (canaux, ex.
Info CHOP d'un Feedback POP).

## POP depuis Python (POP Class)

```python
p = op('threads')
p.numPoints(delayed=False), p.numPrims(primType=None), p.numVerts(lineStrips=False)
p.points('P', startIndex=0, count=-1, delayed=False)   # lecture (stall GPU→CPU ; delayed=True = 1 frame de latence)
p.point('PegIndex', 12); p.prims('Color'); p.verts(...)
p.pointAttributes, p.primAttributes, p.vertAttributes, p.dimension, p.bounds()
p.save('out.pop')                                        # format natif .pop
```

À éviter dans une boucle par frame (sauf `delayed=True`).
