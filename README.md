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

```
pip install numpy
pip install sklearn
pip install scipy
pip install matplotlib
```

## Utilisation

### Réduction d'ordre

```python

from ozzdesign import OZZDesign

#Pour générer des données suivants une distribution aléatoire donnée cf plus bas)

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.getMor()
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

#Pour générer des données suivants une distribution aléatoire donnée cf plus bas)

# nbExp : Le nombre des expériences optimaux souhaitées

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.getOptDesign()
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

### Quelques options

#### Clusters appartenant au plan d'éxpérience initial

```python

# nbIte : lance le k-means 5 fois, la meilleur solution est gardé
# keep_initial=True : spécifie que les clusters finaux doivent appartenir au plan d'éxpérience initial

exp.getMor(nbIte=5, keep_initial=True)

```

#### Choix de l'ordre pour l'active learning

```python
# ord : l'ordre des variables d'entrèe par exemple si ord = 2 toutes les combinaisons
#          quadratiques (x, y, xy, x^2, y^2, 1) seront choisises
#           par défaut le modéle est supposé linéaire
#           à noter que si ord != 1 vous devrez fournir la même valeur lors de l'appel de la fonction readOpt()

exp.getOptDesign(self, ord=1)


```

#### Choix automatique du nombre des clusters

```python
# Choisir automatiquement le nombre de clusters (ne marche pour le moment que pour le MOR)
# maxExp : Nombre maximal de clusters
# minScore : Erreur minimal accépté (par rapport aux valeurs d'entré)

exp = OZZDesign(filename="IN11_10000.txt", nbExp="auto", maxExp=50, minErrMean=1e-13)

```

#### CDF (Fonction de répartition)

```python
exp = OZZDesign(filename="IN11_10000.txt", nbExp=25)

exp.readMor("clusters_c.txt")

print(exp.cdfMor(1.75e-05)) # Affiche 0.3918
```

#### Tracer CDF (Fonction de répartition)

```python
exp = OZZDesign(filename="IN11_10000.txt", nbExp=25)

exp.readMor("clusters_c.txt")

exp.plotCdfMor()
```

## Exemple d'utilisation complet

### MOR pour un couplage Onde/Ligne de transmission et CDF associé

Dans l'exemple suivant nous présenteront un cas d'utilisation concret sur une fonction de couplage Onde/Ligne.

#### Génération du plan d'éxpérience initial

Tout d'abord nous devons créer un plan d'expérience initial (avec les dimensions souhaitées).

La fonction de couplage prends 11 paramètres, par contre vous pouvez choisir le nombre d'exemples qui vous semble le mieux adapté, dans notre cas nous avons choisi d'étudier 100.000 exemples.

Bien entendu il n y'a aucune obligation à utiliser Python pour cette génération vous pouvez très bien la faire avec MatLab.
Du moment qu'à la fin vous obtenez un fichier (que nous nommerons déromais _IN_100000.txt_) contenant 100.000 variables de dimensions 11
distribuèes suivant une loi normale réduite centrèe

```python

import numpy as np

# VOus pouvez remplacer 100.000 avec le nombre d'exemple souhaités
np.savetxt("IN_100000.txt", np.random.normal(1, 0, (100000, 11)))
```

#### Calcul des clusters

```python

from ozzdesign import OZZDesign

#Remplacez le fichier IN_100000.txt par le fichier de votre choix contenant le plan d'éxpérience initial
#Nous considérons ici que le nombre de clusters choisi est de 25 si vous voulez
#un nombre plus important de clusters il suffit de choisir une valeur différente pour nbExp (par exemple nbExp=100)

exp = OZZDesign(filename="IN_100000.txt", nbExp=25)

exp.getMor()
exp.saveMor(filename="output.txt")

```

#### Calcul des valeurs de la fonctionpour les clusterds

Vous devrez voir apparaitre un nouveau fichier _output.txt_ ce fichier contient l'ensemble des clusters choisis. 
Vous devrez maintenant calculer la valeur de la fonctionnelle (en utilisant MatLab par exemple) pour chacun des clusters et mettre la valeur associé dans la dernière colonne.

Exemple 

Note : Remplacer ici 25 avec le nombre d'éxpériences choisises
````matlab
X = importdata("output.txt");

for i = 1:25
    line = mat2cell(X(i, :), 1, ones(1, 11));
    y(i, 1) = couplageOLT(line{:});
end

dlmwrite('clusters_c.txt', [X y], ' ')
````

Vous devrez donc avoir un fichier _clusters_c.txt_ contenant cette fois ci les mêmes 
clusters mais avec la valeur de la fonction dans ces points.

#### Importation des nouvelles valeurs et calcul des différents résultats.

Encore une fois pensez à changer la valeur de nbExp si nombre d'éxpériences différent de 25
```python

from ozzdesign import OZZDesign

exp = OZZDesign(filename="IN_100000.txt", nbExp=25)

exp.readOpt(filename="clusters_c.txt")

# Calcul des moments do'rdre

print("Moment d'ordre 1 : ", exp.meanOpt())
print("Moment d'ordre 2 : ", exp.varOpt())
print("Moment d'ordre 3 : ", exp.skewOpt())
print("Moment d'ordre 4 : ", exp.kurtOpt())

# Affichage de la CDF

exp.plotCdfMor()

```
## Contributeurs

* Yassir Karroum [http://ykarroum.com/](http://ykarroum.com/)
* Imad Enneiymy [https://github.com/maddxyz](https://github.com/maddxyz)

## Référants

* Sebastien LALLECHERE
* Christophe Duhamel [https://www.isima.fr/~duhamel/](https://www.isima.fr/~duhamel/)

