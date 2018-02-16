from ozzdesign import OZZDesign
import numpy as np
from k_means import validate

#exp = OZZDesign(filename="IN11_10000.txt", nbExp="auto", maxExp=50, minErrMean=1e-13)
exp = OZZDesign(filename="IN11_10000.txt", nbExp=25)

#exp.getMor()

exp.readMor("clusters_c.txt")

print(exp.cdf( 1.75e-05))