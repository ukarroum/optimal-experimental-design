import numpy as np
from sklearn import linear_model
import math

def generate_data(n, m):
	return np.random.normal(1, 5, (n, m))


def get_optimal_design_exp(nbExps):
	x = X[np.random.randint(m), :].reshape(1, n)

	A = np.linalg.pinv(np.dot(x.T, x))

	for k in range(nbExps - 1):
		bestScore = np.dot(np.dot(X[0, :], A), X[0, :].T)
		ind = 0
		for i in range(m):
			if np.dot(np.dot(X[i, :], A), X[i, :].T) > bestScore:
				bestScore = np.dot(np.dot(X[i, :], A), X[i, :].T)
				ind = i

		x = np.append(x, X[ind, :].reshape(1, n), axis=0)
		A = np.linalg.pinv(np.dot(x.T, x))

	return x

def get_features(X):
	X = np.insert(X, 2, np.power(X[:, 0], 2), axis=1)
	X = np.insert(X, 3, np.power(X[:, 1], 2), axis=1)
	X = np.insert(X, 4, X[:, 0]*X[:, 1], axis=1)
	X = np.insert(X, 5, np.power(X[:, 0], 2)*X[:, 1], axis=1)
	X = np.insert(X, 6, np.power(X[:, 1], 2)*X[:, 0], axis=1)

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
X = generate_data(m, n)
X = get_features(X)
nb_exp = 25
theta = np.zeros((1, 7))

theta[0, 5] = math.pi*N*C*math.cos(alpha)/4
n = 7

t = get_optimal_design_exp(nb_exp)
tx = X[np.random.choice(X.shape[0], nb_exp), :]


Y = np.dot(t, theta.T) + np.random.normal(0, 0.1, nb_exp).reshape(nb_exp, 1)
Y2 = np.dot(tx, theta.T) + np.random.normal(0, 0.1, nb_exp).reshape(nb_exp, 1)

reg = linear_model.LinearRegression()
reg.fit(t, Y)


print('\033[1m' + str(reg.coef_) + '\033[0m')
print(np.abs(reg.coef_ - theta))
print('\033[1m Erreur (avec Active Learning): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')

reg = linear_model.LinearRegression()
reg.fit(tx, Y2)

print('\033[1m' + str(reg.coef_) + '\033[0m')
print(np.abs(reg.coef_ - theta))
print('\033[1m Erreur (avec tirage aléatoire): ' + str(np.sum(np.absolute(reg.coef_ - theta))/n) + '\033[0m')