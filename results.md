# Résultats sur des exemples :

## CouplageOLT

La fonction utilisé est *couplageOLT* (cf samples/couplaeOLT.m), nous avons modifié la fonction afin qu'elle prenne 11 parametres
au lieu de deux.

Le jeu de données utilisé est : *IN11_10000.txt* (10.000 variables de taille 11 chacune, généré depuis une distribution gaussiene)

nbExps = 25

mean = 1.8217369129999999e-05  
mean(mor) = 1.81763708e-05  
mean(active_1) = 1.80769648999e-05  
mean(active_2) = 1.74578142847e-05  
mean(active_3) = 1.94616482835e-05  

var = 1.1918236827750043e-11  
var(mor) = 3.87688885911e-12  
var(active_1) = 1.80769648999e-05  
var(active_2) = 2.66476956694e-12  
var(active_3) = 7.1029615001e-13  

skew = 0.46281987943203334  
skew(mor) = -0.10283692505605878  
skew(active_1) = 0.00250502  
skew(active_2) = 0.400934210178  
skew(active_3) = -0.254829719464  


kurtosis = 0.2912105527353108  
kurtosis(mor) = -0.7346393523390295  
kurtosis(active_1) = -0.00557957  
kurtosis(active_2) = 1.85063124204  
kurtosis(active_3) = 7.55632999431  



## ToDo

* ~~Ajouter guide pour utilisation~~
* AJouter interface MatLab
* ~~Ajouter d'autres lois (cf NumPy) (surtout une log normal)~~
* Choisir automatiquement nombre de clusters
* ~~AJouter moments d'ordre 3 4~~
* Ajouter CDF et la PDF
* Cf bootstraping
* Regressiin linéaire inverse
* ~~10 monte carlo (différents) et comparer clusters (25)~~
* ~~rapprocher le k-means des points initiaux~~