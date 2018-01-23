import k_means
import numpy as np
import math
from ozzdesign import *

exp = OZZDesign(25, filename="MC07_10000.txt")

exp.getMor()

exp.values = (2*exp.k[:, 0] + 4*exp.k[:, 1]).reshape(25, 1)

print(exp.meanMor())
