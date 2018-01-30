import numpy as np
import k_means
import itertools
from sklearn import linear_model
import scipy

class OZZDesign:
	def __init__(self, nbExp, np_arr=None, filename=None):
		if filename:
			self.X = np.loadtxt(filename)
		else:
			self.X = np_arr

		self.nbExp = nbExp

	def saveAll(self, filename):
		np.savetxt(filename, self.X)

	def getMor(self, nbIte=1, threeshold=0.01):
		self.k, c = k_means.getClusters(self.X, self.nbExp, nbIte, threeshold)
		self.weights = np.unique(c, return_counts=True)[1].reshape(self.nbExp, 1)

		return self.k, self.weights

	def getOptDesign(self, ord=1):
		""" Retourne les points représantant le plan d'éxpérience optimale """

		self.getFeatures(ord)
		indexs = [np.random.randint(np.shape(self.X)[0])]
		x = self.X[indexs[0], :].reshape(1, np.shape(self.X)[1])

		A = np.linalg.pinv(np.dot(x.T, x))

		for k in range(self.nbExp - 1):
			bestScore = - np.inf
			ind = 0
			for i in range(np.shape(self.X)[0]):
				if np.dot(np.dot(self.X[i, :], A), self.X[i, :].T) > bestScore:
					bestScore = np.dot(np.dot(self.X[i, :], A), self.X[i, :].T)
					ind = i

			indexs.append(ind)
			x = np.append(x, self.X[ind, :].reshape(1, np.shape(self.X)[1]), axis=0)
			A = np.linalg.pinv(np.dot(x.T, x))

		self.Opt = self.X[indexs, :]

	def getFeatures(self, ord):
		pows = [list(range(0, ord + 1))]*np.shape(self.X)[1]
		combins = list(itertools.product(*pows))

		for i in range(len(combins)):
			if sum(combins[i]) <= ord and sum(combins[i]) != 1:
				self.X = np.append(self.X, np.product(np.power(self.X[:, :len(combins[i])], combins[i]), axis=1, keepdims=True), axis=1)

	def saveMor(self, filename):
		np.savetxt(filename, np.append(self.k, self.weights, axis=1))

	def saveOpt(self, filename):
		np.savetxt(filename, self.Opt)

	def readMor(self, filename):
		file = np.loadtxt(filename)
		self.k = file[:, :np.shape(file)[1] - 2]
		self.weights = file[:, np.shape(file)[1] - 2]
		self.values = file[:, np.shape(file)[1] - 1]

	def readOpt(self, filename, ord=1):
		file = np.loadtxt(filename)
		self.getFeatures(ord)
		self.Opt = file[:, :np.shape(file)[1] - 1]
		self.values = file[:, np.shape(file)[1] - 1]

		self.reg = linear_model.LinearRegression()
		self.reg.fit(self.Opt, self.values.reshape(25, 1))

	def meanMor(self):
		return np.mean(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def meanOpt(self):
		return np.mean(self.reg.predict(self.X))

	def varMor(self):
		return np.var(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def varOpt(self):
		return np.var(np.dot(self.theta, self.X.T).T)

	def meanMor(self):
		return np.mean(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def meanOpt(self):
		return np.mean(self.reg.predict(self.X))

	def skewMor(self):
		return scipy.stats.skew(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def skewOpt(self):
		return scipy.stats.skew(np.dot(self.theta, self.X.T).T)

	def kurtMor(self):
		return scipy.stats.kurtosis(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def kurtOpt(self):
		return scipy.stats.kurtosis(np.dot(self.theta, self.X.T).T)
