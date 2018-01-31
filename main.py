from ozzdesign import OZZDesign


exp = OZZDesign(filename="MC07_10000.txt", nbExp=25)

print(exp.getMor(keep_initial=True))
# exp.getMor()
#
# exp.saveMor(filename="samples\\clusters.txt")