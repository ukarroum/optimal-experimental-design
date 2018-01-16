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

def generate_data(n, m):
	""" Génére des données aléatoires (distrubition normale N(0, 5000))"""
	return np.random.normal(0, 5000, (n, m))


def get_optimal_design_exp(nbExps):
	""" Retourne les points représantant le plan d'éxpérience optimale """
	x = X[np.random.randint(m), :].reshape(1, n)

	A = np.linalg.pinv(np.dot(x.T, x))

	for k in range(nbExps - 1):
		bestScore = - np.inf
		ind = 0
		for i in range(m):
			if np.dot(np.dot(X[i, :], A), X[i, :].T) > bestScore:
				bestScore = np.dot(np.dot(X[i, :], A), X[i, :].T)
				ind = i

		x = np.append(x, X[ind, :].reshape(1, n), axis=0)
		A = np.linalg.pinv(np.dot(x.T, x))

	return x

# Génération d'un jeu de données aléatoire
m = 10000
n = 5
X = generate_data(m, n)
nb_exp = n + 1
theta = np.arange(1, n + 1).reshape(1, n)

# t représente les données choisi par active learnign et tx les données tirés aléatoirement
t = get_optimal_design_exp(nb_exp)
tx = X[np.random.choice(X.shape[0], nb_exp), :]

# 
Y = np.dot(t, theta.T) + np.random.normal(0, 50, nb_exp).reshape(nb_exp, 1)
Y2 = np.dot(tx, theta.T) + np.random.normal(0, 50, nb_exp).reshape(nb_exp, 1)

reg = linear_model.LinearRegression()
reg.fit(t, Y)


#print('\033[1m' + str(reg.coef_) + '\033[0m')
#print(np.abs(reg.coef_ - theta))
print(t)
print('\033[1m Erreur (avec Active Learning): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')

reg = linear_model.LinearRegression()
reg.fit(tx, Y2)

#print('\033[1m' + str(reg.coef_) + '\033[0m')
#print(np.abs(reg.coef_ - theta))
print('\033[1m Erreur (avec tirage aléatoire): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')