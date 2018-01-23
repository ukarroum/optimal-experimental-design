import numpy as np
import k_means
from sklearn import linear_model


class OZZDesign:
	def __init__(self, nbExp, moy=0, std=1, dim=(10, 2), filename=None):
		if filename:
			self.X = np.loadtxt(filename)
		else:
			self.X = np.random.normal(moy, std, dim)

		self.nbExp = nbExp

	def saveAll(self, filename):
		np.savetxt(filename, self.X)

	def saveOpt(self, filename):
		np.savetxt(filename, self.Opt)

	def Mor(self, nbIte=1, threeshold=0.01):
		self.k, c = k_means.getClusters(self.X, self.nbExp, nbIte, threeshold)
		self.weights = np.unique(c, return_counts=True)[1].reshape(self.nbExp, 1)

		return self.k, self.weights

	def getOptimalDesign(self):
		""" Retourne les points représantant le plan d'éxpérience optimale """
		indexs = [np.random.randint(np.shape(self.X)[0])]
		x = self.X[indexs[0], :].reshape(1, np.shape(self.X)[1])

		A = np.linalg.pinv(np.dot(x.T, x))

		for k in range(self.nbExps - 1):
			bestScore = - np.inf
			ind = 0
			for i in range(np.shape(self.X)[0]):
				if np.dot(np.dot(self.X[i, :], A), self.X[i, :].T) > bestScore:
					bestScore = np.dot(np.dot(self.X[i, :], A), self.X[i, :].T)
					ind = i

			indexs.append(ind)
			x = np.append(x, self.X[ind, :].reshape(1, np.shape(self.X)[1]), axis=0)
			A = np.linalg.pinv(np.dot(x.T, x))

		self.Opt = self.X[:, indexs]

	def saveMor(self, filename):
		np.savetxt(filename, np.append(self.k, self.weights, axis=1))

	def saveOpt(self, filename):
		np.savetxt(filename, self.Opt)

	def readMor(self, filename):
		file = np.loadtxt(filename)
		self.k = file[:, :np.shape(file)[1] - 2]
		self.weights = file[:, np.shape(file)[1] - 2]
		self.values = file[:, np.shape(file)[1] - 1]

	def readOpt(self, filename):
		file = np.loadtxt(filename)
		self.Opt = file[:, :np.shape(file)[1] - 1]
		self.values = file[:, np.shape(file)[1] - 1]
		self.theta = linear_model.LinearRegression().fit(self.Opt, self.values).coef_

	def meanMor(self):
		np.mean(np.repeat(self.values, self.counts, axis=0))

	def meanOpt(self):
		np.mean(np.dot(self.theta, self.X.T).T)

	def varMor(self):
		np.var(np.repeat(self.values, self.counts, axis=0))

	def varOpt(self):
		np.var(np.dot(self.theta, self.X.T).T)