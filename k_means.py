"""
			k_means.py
			==========

Implémentation de l'algorithme K-Means dans le cadre du projet de deuxième année à l'ISIMA.
Cet implémentation prends en compte certaines contraintes dans le projet et a été réalisée
dans le cadre de MOR (model order reduction)

"""

# Utilisée pour l'affichage des points
import matplotlib.pyplot as plt
# Utilisée pour toutes les opérations algebriques
import numpy as np
import math

NB_CLUSTERS = 25

# Nombre d'itérations du script (chaque itération correspand à une execution du k-means à partir d'un solution
# aléatoire de clusters) à la fin le résultat présentant le meilleur coût est séléctionné
NB_ITE = 1

# Utilisé dans la condition d'arret
THRESHOLD = 0.01

def generateK(X):
	"""Génére des clusters aléatoires depuis les points initiaux de X"""
	return X[np.random.randint(np.shape(X)[0], size=NB_CLUSTERS), :]

def plotPoints(X, k, legend=""):
	"""Dessine le jeu de donnée en entrée (points rouges) ainsi que les différents clusters (points bleus)"""
	plt.suptitle(legend)
	plt.plot(X[:, 0], X[:, 1], 'ro')
	plt.plot(k[:, 0], k[:, 1], 'bo')
	plt.axis([-5, 5, -5, 5])
	plt.show()
	
def saveFig(X, k, filename, legend):
	"""Enregistre l'image sous le nom filename"""
	plt.suptitle(legend)
	plt.plot(X[:	, 0], X[:, 1], 'ro')
	plt.plot(k[:, 0], k[:, 1], 'bo')
	plt.axis([-5, 5, -5, 5])
	plt.savefig(filename)

def getClosestVect(X, k):
	"""Retourne un vecteur contenant le cluster le plus proche à chaque point de la matrice X

	Cette version est véctorisé et tourne plus rapidement que la version précédante"""
	return np.argmin(np.linalg.norm(np.tile(X, (NB_CLUSTERS, 1, 1)) \
									- k.reshape((NB_CLUSTERS, 1, np.shape(X)[1])), keepdims=True, axis=2)\
		, axis=0)

def updateCluster(X, k, c, i):
	"""Met à jour le cluster i"""
	s = np.zeros(np.shape(X)[1])
	nb = 0

	for j in range(np.shape(X)[0]):
		if c[j] == i:
			s += X[j]
			nb += 1
	return s/nb if nb != 0 else k[i]
	
def costFct(X, k, c):
	"""Fonction objective qui permet de quantifier la qualité d'une solution par rapport à une autre"""
	m = np.shape(X)[0]
	n = np.shape(X)[1]
	return (1/m)*np.sum(np.linalg.norm(X - np.take(k, c, axis=0).reshape(m, n)))

def validate(X, k, c):
	"""Retourne une matrice contenant la différence de l'éspérence et la variance entre le jeu de donnée initial
		et les clusters (en prenant en considération leurs poids)."""
	res = np.zeros((2, X.shape[1]))

	unique, counts = np.unique(c, return_counts=True)
	weighted_k = np.repeat(k, counts, axis=0)
	res[0] = (np.mean(X, axis=0) - np.mean(weighted_k, axis=0)) / np.mean(X, axis=0)
	res[1] = (np.var(X, axis=0) - np.var(weighted_k, axis=0)) / np.var(X, axis=0)

	return res

def getClusters(X, nbClusters=NB_CLUSTERS, nbIte=NB_ITE, threshold=THRESHOLD):
	"""La fonction principale calcule les clusters pour un jeu de donnée X"""
	c = np.zeros((np.shape(X)[0], 1), dtype='int64')

	NB_CLUSTERS = nbClusters
	NB_ITE = nbIte
	THRESHOLD = threshold

	bestCost = np.inf
	bestK = 0
	bestC = 0

	for l in range(NB_ITE):
		k = generateK(X)
		changed = True

		while changed:
			changed = False

			c = getClosestVect(X, k)

			for i in range(NB_CLUSTERS):
				tmp = updateCluster(X, k, c, i)
				if np.linalg.norm(k[i] - tmp) > THRESHOLD:
					changed = True
				k[i] = tmp
		tmp = np.sum(np.absolute(validate(X, k, c)))
		if tmp < bestCost:
			bestK = k
			bestCost = tmp
			bestC = c
	k = bestK
	c = bestC

	return k, c
