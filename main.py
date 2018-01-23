import k_means
import numpy as np
import math

alpha    = 38*math.pi/180
alp      = 0.1
d        = 0.202e-3
dmax     = (1+alp)*d
dmin     = (1-alp)*d
moyx   = (dmax+dmin)/2
stdx   = math.sqrt((dmax-dmin)**2./12)

X = np.random.normal(moyx, stdx, (10000, 2))

k, c = k_means.getClusters(X)

k_means.plotPoints(X, k)

unique, counts = np.unique(c, return_counts=True)
weighted_k = np.repeat(k, counts, axis=0)

print(np.mean(np.pi*weighted_k[:, 0]**2*5*24*weighted_k[:, 1]*math.cos(38*math.pi/180)/4))
print(np.mean(np.pi*X[:, 0]**2*5*24*X[:, 1]*math.cos(38*math.pi/180)/4))