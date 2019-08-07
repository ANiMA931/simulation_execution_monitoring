import clr
clr.FindAssembly("E:\code\PycharmProjects\simulation\ClassLibrary.dll")
import ClassLibrary
class c_sharptopy:
    def __init__(self,Library=ClassLibrary):
        self.library=Library
    def square(self,num):
        return self.library.Class1().Square(num)

if __name__ == '__main__':
    a=c_sharptopy()
    print(a.square(50))
