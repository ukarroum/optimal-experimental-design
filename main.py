from ozzdesign import OZZDesign
import numpy as np

for i in range(10):
	exp = OZZDesign(filename="clusters_" + str(i) + ".txt", nbExp=25)
	exp.readMor("clusters_c_" + str(i) + ".txt")
	print(exp.meanMor())

# exp = OZZDesign(filename="IN11_10000.txt", nbExp="auto", maxExp=50, minScore=0.5)
#
# exp.getMor()
#
# print(exp.nbExp)
# exp.readOpt("active_c.txt", ord=3)
#
# print(exp.meanOpt())
# print(exp.varOpt())
# print(exp.skewOpt())
# print(exp.kurtOpt())

# exp.getMor()
#
# exp.saveMor(filename="samples\\clusters.txt")