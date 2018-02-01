from ozzdesign import OZZDesign


exp = OZZDesign(filename="IN11_10000.txt", nbExp="auto", maxExp=50)

exp.getMor()

print(exp.nbExp)
# exp.readOpt("active_c.txt", ord=3)
#
# print(exp.meanOpt())
# print(exp.varOpt())
# print(exp.skewOpt())
# print(exp.kurtOpt())

# exp.getMor()
#
# exp.saveMor(filename="samples\\clusters.txt")