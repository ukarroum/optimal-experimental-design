from ozzdesign import OZZDesign

exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

exp.readMor(filename="samples\\exp.txt")

print(exp.meanMor())

print(exp.varMor())
# exp.getMor()
#
# exp.saveMor(filename="samples\\clusters.txt")