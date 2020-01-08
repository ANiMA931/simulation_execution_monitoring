from time import time
from externalFunc.func4c import square as c_square

print(c_square(90))

from externalFunc.func4c_sharp import square as c_sharp_square

print(c_sharp_square(14))
a = time()


from externalFunc import *
from externalFunc.func4m import square, add

def more_square(a):

    return square(a)

print(time() - a)
for i in range(10):
    print(add(i, i, i))
    print(square(i))
