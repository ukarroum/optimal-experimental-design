# OZZDesign (Optimal ZZ Design)

## Introduction

OZZDesign est notre projet de deuxième année à l'ISIMA, il vise à créer une bibliothéque permettant d'automatiser
certaines tâches liés à la réduction d'ordre ([MOR](https://en.wikipedia.org/wiki/Model_order_reduction)) et le plan
d'éxpérience optimale ([Plan d'éxpérience optimal](https://en.wikipedia.org/wiki/Optimal_design), la bibliothéque
permet d'utiliser façilement des structures de données NumPy.

## Fonctionalités

* Récupérer les points (nombre fixé par l'utilisateur) permettant d"étudier un système entier avec un nombre plus réduit de points
* Récupérer les plans d'éxpérience optimaux sur un plan d'éxpérience donnée
* Calculer les moments d'ordres (1, 2, 3 et 4) à partir du plan d'éxpérience optimaux ou du modéle réduit

## Dépendances

`
pip install numpy
pip install sklearn
pip install scipy
`

## Utilisation

### Réduction d'ordre

```python

from ozzdesign import OZZDesign

#Pour générer des données suivants une distribution aléatoire donnée cd plus bas)

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.saveMor(filename="output.txt")

```

Arrivé là vous devez ajouter une colone au fichier généré *output.txt*, une fois celà fait vous pouvez recharger le fichier dans le programme

```python

from ozzdesign import OZZDesign

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.readMor(filename="output.txt")

print("Moment d'ordre 1 : ", exp.meanMor())
print("Moment d'ordre 2 : ", exp.varMor())
print("Moment d'ordre 3 : ", exp.skewMor())
print("Moment d'ordre 4 : ", exp.kurtMor())

```

### Plan d'éxpérience optimal

Les fonctions sont exactement les mêmes, il suffit de changer *Mor* par *Opt*.

```python

from ozzdesign import OZZDesign

#Pour générer des données suivants une distribution aléatoire donnée cd plus bas)

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.saveOpt(filename="output.txt")

```

Arrivé là vous devez ajouter une colone au fichier généré *output.txt*, une fois celà fait vous pouvez recharger le fichier dans le programme

```python

from ozzdesign import OZZDesign

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.readOpt(filename="output.txt")

print("Moment d'ordre 1 : ", exp.meanOpt())
print("Moment d'ordre 2 : ", exp.varOpt())
print("Moment d'ordre 3 : ", exp.skewOpt())
print("Moment d'ordre 4 : ", exp.kurtOpt())

```

### Utiliser d'autres distributions

*OZZDesign* permet de fournir un tableau numpy comme jeu de donnée initial, NumPy permet de générer des données aléatoires suivants une loi.

Par exemple :

```python

from ozzdesign import OZZDesign
import numpy as np

exp = OZZDesign(np_arr=numpy.random.normal(1, 5, (10000, 2)), nbExp=25) # Normal(1, 5)
exp = OZZDesign(np_arr=numpy.random.lognormal(1, 5, (10000, 2)), nbExp=25) # LogNormal(1, 5)
exp = OZZDesign(np_arr=numpy.random.poisson(5, (10000, 2)), nbExp=25) # Poisson(lambda = 5)
exp = OZZDesign(np_arr=numpy.random.uniform(1, 5, (10000, 2)), nbExp=25) # Uniforme [1, 5]

```

Vous trouverez la totalité des lois proposées par NumPy ici : [https://docs.scipy.org/doc/numpy/reference/routines.random.html](https://docs.scipy.org/doc/numpy/reference/routines.random.html)





## Contributeurs

* Yassir Karroum [http://ykarroum.com/](http://ykarroum.com/)
* Imad Enneiymy [https://github.com/maddxyz](https://github.com/maddxyz)

## Encadrants

* Sebastien LALLECHERE
* Christophe Duhamel [https://www.isima.fr/~duhamel/](https://www.isima.fr/~duhamel/)

