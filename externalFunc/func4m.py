import matlab.engine
from time import time
class mtopy:
    def __init__(self,engine=matlab.engine.start_matlab()):
        self.engine=engine
    def square(self,num):
        return self.engine.square(matlab.double([num])) #此处虽然报错double，但是真的可以将其改成double型的数据。

if __name__ == '__main__':
    b=time()
    a=mtopy()
    for i in range(100):
        print(a.square(i))
    print(time()-b)

