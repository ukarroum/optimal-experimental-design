"""
			active_learning_var.py
			=======================

Script séléctionnant les meilleurs points sur leqsquels on pourrai réaliser une régression linéaire
Le but est de l'utiliser pour trouver lesp lans d'éxpérience optimal en considérant comme critère : une A-optimalité

"""

import numpy as np

# Bibliothèque de Machine Learning utilisé ici pour la régression linéaire
from sklearn import linear_model
import random

def get_optimal_design_exp(nbExps):
	""" Retourne les points représantant le plan d'éxpérience optimale """
	indexs = [np.random.randint(m)]
	x = X[indexs[0], :].reshape(1, n)

	A = np.linalg.pinv(np.dot(x.T, x))

	for k in range(nbExps - 1):
		bestScore = - np.inf
		ind = 0
		for i in range(m):
			if np.dot(np.dot(X[i, :], A), X[i, :].T) > bestScore:
				bestScore = np.dot(np.dot(X[i, :], A), X[i, :].T)
				ind = i

		indexs.append(ind)
		x = np.append(x, X[ind, :].reshape(1, n), axis=0)
		A = np.linalg.pinv(np.dot(x.T, x))

	return indexs

def get_features(X):
	X = np.insert(X, 2, np.power(X[:, 0], 2), axis=1)
	X = np.insert(X, 3, np.power(X[:, 1], 2), axis=1)
	X = np.insert(X, 4, X[:, 0]*X[:, 1], axis=1)
	X = np.insert(X, 5, np.power(X[:, 0], 2)*X[:, 1], axis=1)
	X = np.insert(X, 6, np.power(X[:, 1], 2)*X[:, 0], axis=1)

	return X

# Génération d'un jeu de données aléatoire
m = 10000
n = 5
X = generate_data(m, n)
nb_exp = n + 1
theta = np.arange(1, n + 1).reshape(1, n)

valid = np.zeros((20, 2, 2))

for i in range(20):
	# t représente les données choisi par active learnign et tx les données tirés aléatoirement
	t = get_optimal_design_exp(nb_exp)
	tx = np.random.choice(X.shape[0], nb_exp)

	Y = np.dot(X, theta.T) + np.random.normal(0, 50, m).reshape(m, 1)

	reg = linear_model.LinearRegression()
	reg.fit(X[t, :], Y[t])


	#print('\033[1m Erreur (avec Active Learning): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')
	#print('\033[1m Erreur J (avec Active Learning): ' + str(np.sum(np.absolute(np.dot(reg.coef_, X.T).T - Y))) + '\033[0m')

	valid[i][0][0] = np.sum(np.absolute(reg.coef_ - theta))/n
	valid[i][0][1] = np.sum(np.absolute(np.dot(reg.coef_, X.T).T - Y))

	reg = linear_model.LinearRegression()
	reg.fit(X[tx, :], Y[tx])

	#print('\033[1m Erreur (avec tirage aléatoire): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')
	#print('\033[1m Erreur J (avec Active Learning): ' + str(np.sum(np.absolute(np.dot(reg.coef_, X.T).T - Y))) + '\033[0m')

	valid[i][1][0] = np.sum(np.absolute(reg.coef_ - theta)) / n
	valid[i][1][1] = np.sum(np.absolute(np.dot(reg.coef_, X.T).T - Y))

print(np.mean(valid, axis=0))
print(np.var(valid, axis=0))