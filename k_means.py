import matplotlib.pyplot as plt
import numpy as np
import math
from sys import getsizeof

nb_clusters = 35
nb_ite = 10
threshold = 0.1 #Utilisé dans la condition d'arret

def load_data(filename):
	""" Charge les différentes données et les retourne """
	return np.loadtxt(filename)

def generateData(n, m):
	return np.random.normal(0, 5, (m, n))

def generateK():
	"""Génére des clusters aléatoires"""
	return X[np.random.randint(m, size=nb_clusters), :]

def plotPoints(legend=""):
	"""Dessine le jeu de donnée en entrée ainsi que les différents clusters"""
	plt.suptitle(legend)
	plt.plot(X[:, 0], X[:, 1], 'ro')
	plt.plot(k[:, 0], k[:, 1], 'bo')
	plt.axis([-5, 5, -5, 5])
	plt.show()
	
def saveFig(filename, legend):
	"""Enregistre l'image"""
	plt.suptitle(legend)
	plt.plot(X[:	, 0], X[:, 1], 'ro')
	plt.plot(k[:, 0], k[:, 1], 'bo')
	plt.axis([-5, 5, -5, 5])
	plt.savefig(filename)
	
def getClosest(x):
	"""Affecte chaque cluster au points qui lui sont le plus proche"""
	mini = math.inf
	ind = 0
	for i in range(nb_clusters):
		if(mini > np.linalg.norm(x - k[i])):
			mini = np.linalg.norm(x - k[i])
			ind = i;
	return ind

def getClosestVect(X):
	"""Version vectorisée de la fonction getClosest"""
	return np.argmin(np.linalg.norm(np.tile(X, (nb_clusters, 1, 1)) \
		- k.reshape((nb_clusters, 1, np.shape(X)[1])), keepdims=True, axis=2)\
		, axis=0)

def updateCluster(i):
	"""Met à jour les clusters"""
	s = np.zeros(np.shape(X)[1])
	nb = 0

	for j in range(m):
		if(c[j] == i):
			s += X[j]
			nb += 1
	return s/nb if nb != 0 else k[i]
	
def costFct():
	"""Fonction objective qui permet de quantifier la qualité d'une solution"""
	return (1/m)*np.sum(np.linalg.norm(X - np.take(k, c, axis=0).reshape(m, n)))

def validate():
	res = np.zeros((2, 2))
	res[0] = (np.mean(X, axis=0) - np.mean(k, axis=0)) / np.mean(X, axis=0)
	res[1] = (np.var(X, axis=0) - np.var(k, axis=0)) / np.var(X, axis=0)

	return res

X = load_data("MC07_10000.txt")
m = np.shape(X)[0]
n = np.shape(X)[1]
c = np.zeros((m, 1), dtype='int64')


bestCost = np.inf
ind = 0

for l in range(10):
	k = generateK()
	changed = True

	while changed:
		changed = False

		c = getClosestVect(X)

		for i in range(nb_clusters):
			tmp = updateCluster(i)
			if(np.linalg.norm(k[i] - tmp) > threshold):
				changed = True
			k[i] = tmp
	tmp = costFct()
	if tmp < bestCost:
		bestK = k
		bestCost = tmp	
		ind = l

k = bestK
np.savetxt("clusters.txt", k)
print("Best Cost : ", str(bestCost))
print("Index of best solution : ", str(ind))
print(validate())
plotPoints()
