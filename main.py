from ozzdesign import OZZDesign
import numpy as np


exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.readMor(filename="samples\\exp.txt")
d = np.loadtxt("MC07_10000.txt")

print(exp.meanMor())
print(exp.varMor())
print(exp.skewMor())
# exp.getMor()
#
# exp.saveMor(filename="samples\\clusters.txt")