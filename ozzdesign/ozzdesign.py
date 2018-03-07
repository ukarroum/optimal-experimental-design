import itertools

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn import linear_model

from ozzdesign import k_means


class OZZDesign:
	def __init__(self, nbExp, np_arr=None, filename=None, maxExp=None, minErrMean=0.1):
		"""Initialise l'objet ZZDesign


		Params :

		nbExp : entier détérminant le nombre d'éxpériences optimals souhaitées ou "auto" pour que ce nombre soit déduit automatiquement
				Bien entendu l'utilisateur devra toujours spécifier un nombre maximal d'éxpériences à ne pas dépasser

		minScore : Uniquement si nbExp = auto, précise le score silouhaite minimal souhaité."""
		if filename:
			self.X = np.loadtxt(filename)
		else:
			self.X = np_arr

		self.nbExp = nbExp

		if nbExp == "auto":
			self.maxExp = maxExp
			self.minErrMean = minErrMean

	def saveAll(self, filename):
		np.savetxt(filename, self.X)

	def getMor(self, nbIte=1, threeshold=0.01, keep_initial=False, useVar=False):
		""" Retourne les points du modele réduit :

		Params :

		nbIte : Nombre des itération du k-means
		threeshold : Utilisé comme condition d'arrêt pour le k-means
		keep_initial : choisir des points appartenant au plan d'éxpérience initial"""

		if self.nbExp != "auto":
			self.k, c = k_means.getClusters(self.X, self.nbExp, nbIte, threeshold, useVar)
		else:
			for i in range(2, self.maxExp):
				self.k, c = k_means.getClusters(self.X, i, nbIte, threeshold)
				print(i)
				if np.mean(np.abs(k_means.validate(self.X, self.k, c)[0])) <= self.minErrMean:
					self.nbExp = i
					break

		if keep_initial:
			for i in range(np.shape(self.k)[0]):
				self.k[i] = self.X[np.argmin(np.abs(np.linalg.norm(self.k[i] - self.X, axis=1))), :]

		self.weights = np.unique(c, return_counts=True)[1].reshape(self.nbExp, 1)

		print(np.mean(np.absolute(k_means.validate(self.X, self.k, c)[1])))
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
		return np.var(self.reg.predict(self.X))

	def skewMor(self):
		return stats.skew(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def skewOpt(self):
		return stats.skew(self.reg.predict(self.X))[0]

	def kurtMor(self):
		return stats.kurtosis(np.repeat(self.values, self.weights.reshape(self.nbExp, ).astype(int), axis=0))

	def kurtOpt(self):
		return stats.kurtosis(self.reg.predict(self.X))[0]

	def cdfMor(self, value):
		sorted_values = sorted(list(zip(self.values, self.weights)))
		cum_weight = 0

		for val in sorted_values:
			if value < val[0]:
				break
			cum_weight += val[1]
		return cum_weight/self.X.shape[0]

	def cdfOpt(self, value):
		sorted_values = sorted(self.reg.predict(self.X))
		cum_weight = 0

		for val in sorted_values:
			if value < val:
				break
			cum_weight += 1
		return cum_weight/self.X.shape[0]

	def plotCdfMor(self):
		sorted_values = sorted(list(zip(self.values, self.weights/self.X.shape[0])))
		values, weights = list(zip(*sorted_values))
		plt.plot(values, np.cumsum(weights))
		plt.show()

	def plotCdfOpt(self):
		sorted_values = sorted(self.reg.predict(self.X))

		plt.plot(sorted_values, np.cumsum(np.ones(self.X.shape[0])/self.X.shape[0]))
		plt.show()