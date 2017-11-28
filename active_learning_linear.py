import numpy as np
from sklearn import linear_model
import random

NB_ITE_MULTI_START = 10
NB_ITE_LOCAL_SEARCH = 30


def generate_data(n, m):
	return np.random.normal(0, 5, (n, m))


def get_optimal_design_exp(X, nbExps):
	best = np.random.choice(X.shape[0], nbExps)
	best_score = np.trace(np.linalg.pinv(np.dot(X[best, :].T, X[best, :])))

	for i in range(NB_ITE_MULTI_START):
		curr_ind = np.random.choice(X.shape[0], nbExps)
		curr = X[curr_ind, :]
		for j in range(NB_ITE_LOCAL_SEARCH):
			print("i : ", i, " j : ", j)
			ind = random.randint(0, nbExps - 1)
			best_score_loc = np.trace(np.linalg.pinv(np.dot(curr.T, curr)))
			best_loc = curr_ind
			tmpInd = curr_ind
			changed = False
			for k in range(X.shape[0]):
				tmpInd[ind] = k
				if np.trace(np.linalg.pinv(np.dot(X[tmpInd, :].T, X[tmpInd, :]))) > best_score_loc:
					changed = True
					best_loc[ind] = k
					best_score_loc = np.trace(np.linalg.pinv(np.dot(X[best_loc, :].T, X[best_loc, :])))

			curr_ind = best_loc
			curr = X[curr_ind, :]

			if not changed:
				break
		if np.trace(np.linalg.pinv(np.dot(curr.T, curr))) > best_score:
			best = curr_ind
			best_score = np.trace(np.linalg.pinv(np.dot(curr.T, curr)))
	return best

X = generate_data(10000, 2)

t = get_optimal_design_exp(X, 2)
#t = np.random.choice(X.shape[0], 2)

theta = np.array([[3, 5]])

Y = np.dot(X[t, :], theta.T)

reg = linear_model.LinearRegression()
reg.fit(X[t, :], Y)

print('\033[1m' + str(reg.coef_) + '\033[0m')