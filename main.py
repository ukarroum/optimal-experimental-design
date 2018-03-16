from ozzdesign import OZZDesign

#exp = OZZDesign(filename="IN11_10000.txt", nbExp="auto", maxExp=50, minErrMean=1e-13)
exp = OZZDesign(filename="IN11_10000.txt", nbExp=25)

exp.readOpt(filename="active.txt", ord=2)

exp.exportOpt(filename="coefs.txt")