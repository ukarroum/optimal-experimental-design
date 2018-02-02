# Résultats sur des exemples :

## CouplageOLT

La fonction utilisé est *couplageOLT* (cf samples/couplaeOLT.m), nous avons modifié la fonction afin qu'elle prenne 11 parametres
au lieu de deux.

Le jeu de données utilisé est : *IN11_10000.txt* (10.000 variables de taille 11 chacune, généré depuis une distribution gaussiene)

Modèles utilisés :
* mean, var, ... : valeurs des moments d'ordre sur la totalité des données (en gros c'est une sorte de valeur de référence) 
* MOR : k_means
* MOR_rapproche : K_means avec des clusters appartenant au plan d'éxpérience initial
* active_n : Active learning d'ordre n


```
nbExps = 25
```

```
mean = 1.8217369129999999e-05  
mean(mor) = 1.81763708e-05  
mean(mor_rapporche) =  
mean(active_1) = 1.80769648999e-05  
mean(active_2) = 1.74578142847e-05  
mean(active_3) = 1.94616482835e-05  
```

```
var = 1.1918236827750043e-11  
var(mor) = 3.87688885911e-12  
mean(mor_rapporche) =  
var(active_1) = 1.80769648999e-05  
var(active_2) = 2.66476956694e-12  
var(active_3) = 7.1029615001e-13  
```

```
skew = 0.46281987943203334  
skew(mor) = -0.10283692505605878  
mean(mor_rapporche) =  
skew(active_1) = 0.00250502  
skew(active_2) = 0.400934210178  
skew(active_3) = -0.254829719464  
```

```
kurtosis = 0.2912105527353108  
kurtosis(mor) = -0.7346393523390295  
mean(mor_rapporche) =   
kurtosis(active_1) = -0.00557957  
kurtosis(active_2) = 1.85063124204  
kurtosis(active_3) = 7.55632999431  
```

En lancant une détéction automatique du nombre des clusters on obitient (avec un score minimal de 0.9) :

```
nombre clusters = 
```

## Résultats de lancement de 10 monte carlo différents 

```
mean_1 = 159.2043
mean_1(mor) = 158.4695387

mean_2 = 158.4441
mean_2(mor) = 157.7036484

mean_3 = 157.6823
mean_3(mor) = 156.9453355

mean_4 = 158.7310
mean_4(mor) = 157.9515142

mean_5 = 157.9431
mean_5(mor) = 157.0767357

mean_6 = 159.2945
mean_6(mor) = 158.4241033

mean_7 = 159.3801
mean_7(mor) = 158.635559

mean_8 = 159.2718
mean_8(mor) = 158.4799453

mean_9 = 159.0503
mean_9(mor) = 158.3840955

mean_10 = 156.8127
mean_10(mor) = 156.0987295

```
## ToDo

* ~~Ajouter guide pour utilisation~~
* AJouter interface MatLab
* ~~Ajouter d'autres lois (cf NumPy) (surtout une log normal)~~
* ~~Choisir automatiquement nombre de clusters~~
* ~~AJouter moments d'ordre 3 4~~
* Ajouter CDF et la PDF
* Cf bootstraping
* Regressiin linéaire inverse
* ~~10 monte carlo (différents) et comparer clusters (25)~~
* ~~rapprocher le k-means des points initiaux~~