from ozzdesign import *

exp = OZZDesign(25, filename="MC07_10000.txt")

# exp.getMor(25)
#
# exp.saveMor(filename="clu.txt")

# exp.readMor(filename="samples\\exp.txt")
#
# print(exp.meanMor())



#
# exp.getOptDesign(3)
#
# exp.saveOpt(filename="samples\\1_act.txt")

exp.readOpt(filename="samples\\exp.txt", ord=3)

print(exp.meanOpt())

#print(exp.meanMor())