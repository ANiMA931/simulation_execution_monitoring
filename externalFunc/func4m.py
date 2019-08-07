import matlab.engine
from time import time
class mtopy:
    def __init__(self,engine=matlab.engine.connect_matlab()):
        self.engine=engine
    def square(self,num):
        return self.engine.square(matlab.double([num]))

if __name__ == '__main__':
    b=time()
    a=mtopy()
    print(a.square(90))
    print(time()-b)
