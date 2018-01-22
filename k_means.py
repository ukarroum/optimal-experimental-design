"""
			k_means.py
			==========

Implémentation de l'algorithme K-Means dans le cadre du projet de deuxième année à l'ISIMA.
Cet implémentation prends en compte certaines contraintes dans le projet et a été réalisée
dans le cadre de MOR (model order reduction)

"""

# Utilisée pour l'aiffhage des points
import matplotlib.pyplot as plt
# Utilisée pour toutes les opérations algebriques
import numpy as np
import math

nb_clusters = 10

# Nombre d'itérations du script (chaque itération correspand à une execution du k-means à partir d'un solution
# aléatoire de clusters, à la fin le résultat présentant le meilleur coût est séléctionné
nb_ite = 1

# Utilisé dans la condition d'arret
threshold = 0.01

def load_data(filename):
	""" Charge le jeu de donnée initial depuis le fichier et le retourne

			filename : Fichier contenant les données"""
	return np.loadtxt(filename)

def generateData(n, m):
	""" génére une matrice de taille (n x m) de valeurs aléatoires suivant une loi normal d'éspérence 1 et d'écart-type 5"""
	return np.random.normal(1, 5, (m, n))

def generateK():
	"""Génére des clusters aléatoires depuis les points initiaux de X"""
	return X[np.random.randint(m, size=nb_clusters), :]

def plotPoints(legend=""):
	"""Dessine le jeu de donnée en entrée (points rouges) ainsi que les différents clusters (points bleus)"""
	plt.suptitle(legend)
	plt.plot(X[:, 0], X[:, 1], 'ro')
	plt.plot(k[:, 0], k[:, 1], 'bo')
	plt.axis([-5, 5, -5, 5])
	plt.show()
	
def saveFig(filename, legend):
	"""Enregistre l'image sous le nom filename"""
	plt.suptitle(legend)
	plt.plot(X[:	, 0], X[:, 1], 'ro')
	plt.plot(k[:, 0], k[:, 1], 'bo')
	plt.axis([-5, 5, -5, 5])
	plt.savefig(filename)

def getClosestVect(X):
	"""Retourne un vecteur contenant le cluster le plus proche à chaque point de la matrice X

	Cette version est véctorisé et tourne plus rapidement que la version précédante"""
	return np.argmin(np.linalg.norm(np.tile(X, (nb_clusters, 1, 1)) \
		- k.reshape((nb_clusters, 1, np.shape(X)[1])), keepdims=True, axis=2)\
		, axis=0)

def updateCluster(i):
	"""Met à jour le cluster i"""
	s = np.zeros(np.shape(X)[1])
	nb = 0

	for j in range(m):
		if c[j] == i:
			s += X[j]
			nb += 1
	return s/nb if nb != 0 else k[i]
	
def costFct():
	"""Fonction objective qui permet de quantifier la qualité d'une solution par rapport à une autre"""
	return (1/m)*np.sum(np.linalg.norm(X - np.take(k, c, axis=0).reshape(m, n)))

def validate():
	"""Retourne une matrice contenant la différence de l'éspérence et la variance entre le jeu de donnée initial
		et les clusters (en prenant en considération leurs poids)."""
	res = np.zeros((2, 2))

	unique, counts = np.unique(c, return_counts=True)
	weighted_k = np.repeat(k, counts, axis=0)
	res[0] = (np.mean(X, axis=0) - np.mean(weighted_k, axis=0)) / np.mean(X, axis=0)
	res[1] = (np.var(X, axis=0) - np.var(weighted_k, axis=0)) / np.var(X, axis=0)

	return res


# X est la matrice contenant le jeu de donnée initial
# Elle contient m points, chacun de taille n
X = load_data("MC07_10000.txt")
m = np.shape(X)[0]
n = np.shape(X)[1]
c = np.zeros((m, 1), dtype='int64')

bestCost = np.inf
ind = 0
bestK = 0
bestC = 0

for l in range(nb_ite):
	k = generateK()
	changed = True

	while changed:
		changed = False

		c = getClosestVect(X)

		for i in range(nb_clusters):
			tmp = updateCluster(i)
			if np.linalg.norm(k[i] - tmp) > threshold:
				changed = True
			k[i] = tmp
	tmp = np.sum(np.absolute(validate()))
	if tmp < bestCost:
		bestK = k
		bestCost = tmp
		bestC = c
		ind = l
k = bestK
c = bestC

unique, counts = np.unique(c, return_counts=True)
weighted_k = np.repeat(k, counts, axis=0)

print(np.var(np.pi*weighted_k[:, 0]**2*5*24*weighted_k[:, 1]*math.cos(38*math.pi/180)/4))
print(np.var(np.pi*X[:, 0]**2*5*24*X[:, 1]*math.cos(38*math.pi/180)/4))
#print(np.var(validations, axis=0))
