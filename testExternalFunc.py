from time import time
from func4c import ctopy
print(ctopy().squre(90))

from func4c_sharp import c_sharptopy
print(c_sharptopy().square(14))
a=time()
from func4m import mtopy

for i in range(100):
    print(mtopy().square(i))
    print(time() - a)

