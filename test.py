from time import time
from externalFunc.func4c import ctopy
print(ctopy().squre(90))

from externalFunc.func4c_sharp import c_sharptopy
print(c_sharptopy().square(14))
a=time()
from func4m import mtopy
print(time()-a)
for i in range(100):
    print(mtopy().square(i))




