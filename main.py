from ozzdesign import OZZDesign
import numpy as np
from k_means import validate

#exp = OZZDesign(filename="IN11_10000.txt", nbExp="auto", maxExp=50, minErrMean=1e-13)
exp = OZZDesign(filename="IN11_10000.txt", nbExp=25)

#exp.getMor()

#exp.getOptDesign(ord=2)
#exp.saveOpt("active.txt")
exp.readOpt("active_c.txt", ord=2)



print(exp.cdfOpt(1.7984e-05))
print(exp.cdfOpt(1.7313e-05))
print(exp.cdfOpt(1.75e-05))
print(exp.cdfOpt(500))