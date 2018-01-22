import numpy as np
from sklearn import linear_model
import math

def generate_data(n, m):
	return np.random.normal(0, 5, (n, m))

def load_data(filename):
	""" Charge le jeu de donnée initial depuis le fichier et le retourne

			filename : Fichier contenant les données"""
	return np.loadtxt(filename)


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
	X = np.insert(X, 4, np.power(X[:, 0], 3), axis=1)
	X = np.insert(X, 5, np.power(X[:, 1], 3), axis=1)
	X = np.insert(X, 6, np.power(X[:, 0], 2)*np.power(X[:, 1], 1), axis=1)
	X = np.insert(X, 7, np.power(X[:, 0], 1)*np.power(X[:, 1], 2), axis=1)
	X = np.insert(X, 8, np.power(X[:, 0], 1)*np.power(X[:, 1], 1), axis=1)

	return X



# csts

N=5;
C=24;
sigma    = 41.2e6;
alpha    = 38*math.pi/180;
d        = 0.202e-3;
alp      = 0.1;
dmax     = (1+alp)*d;
dmin     = (1-alp)*d;
sigmamax = (1+alp)*sigma;
sigmamin = (1-alp)*sigma;

################

m = 10000
n = 2
#X = generate_data(m, n)
X = load_data("MC07_10000.txt")
X = get_features(X)
nb_exp = 10
theta = np.zeros((1, 9))

theta[0, 6] = math.pi*N*C*math.cos(alpha)/4
print(theta)
n = 9

t = get_optimal_design_exp(nb_exp)
tx = np.random.choice(X.shape[0], nb_exp)

Y = np.dot(X, theta.T) + np.random.normal(0, 0.05, m).reshape(m, 1)

reg = linear_model.LinearRegression()
reg.fit(X[t, :], Y[t])


print('\033[1m Erreur (avec Active Learning): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')
print('\033[1m Erreur (avec Active Learning): ' + str(np.sum(np.absolute(np.dot(reg.coef_, X.T).T - Y))) + '\033[0m')

print(np.mean(np.dot(reg.coef_, X.T).T))
print(np.var(np.dot(reg.coef_, X.T).T))