import k_means
import numpy as np

X = np.loadtxt("MC07_10000.txt")

# unique, counts = np.unique(c, return_counts=True)
# weighted_k = np.repeat(k, counts, axis=0)
#
# print(np.var(np.pi*weighted_k[:, 0]**2*5*24*weighted_k[:, 1]*math.cos(38*math.pi/180)/4))
# print(np.var(np.pi*X[:, 0]**2*5*24*X[:, 1]*math.cos(38*math.pi/180)/4))
# #print(np.var(validations, axis=0))