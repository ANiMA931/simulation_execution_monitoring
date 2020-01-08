from clr import AddReference  # 必要的库，通过pip安装Pythonnet后可用

classLibrary_path = r'C:\Users\ANiMA\source\repos\ClassLibraryTestt\ClassLibraryTestt\bin\Debug\ClassLibraryTestt.dll'  # dll文件的所在路径
AddReference(classLibrary_path)  # 通过clr中的FindAssembly()方法来将路径引入
try:
    import ClassLibraryTestt
    from ClassLibraryTestt import *  # 引入包的名称必须要于dll文件一致，出现错误时退出
except ModuleNotFoundError:
    print(
        'ClassLibrary path: "' + classLibrary_path + '" has no current module. Please check module name according Docs.')
    input('\nPress "enter" to exit.\n')
    exit()


def square(a):
    """
    命名空间ClassLibrary中Class1类中的静态函数Square。
    在只有一个类的情况下，不必在函数名中添加与类相关的信息，仅需与函数名相同即可。
    函数名首字母小写，参数类型与返回值需要与C#函数对应，通过类的缺省声明来调用类中的函数。
    """
    return Class1().Square(a)


def plus(a, b):
    """
    命名空间ClassLibrary中Class1类中的静态函数Square。
    在只有一个类的情况下，不必在函数名中添加与类相关的信息，仅需与函数名相同即可。
    函数名首字母小写，参数类型与返回值需要与C#函数对应，通过类的缺省声明来调用类中的函数。
    """
    return Class1().Plus(a, b)


def times(a, b):
    """
    命名空间ClassLibrary中Class1类中的静态函数Square。
    在只有一个类的情况下，不必在函数名中添加与类相关的信息，仅需与函数名相同即可。
    函数名首字母小写，参数类型与返回值需要与C#函数对应，通过类的缺省声明来调用类中的函数。
    """
    return Class1().Times(a, b)


class Rectangle(Rectangle):
    def __init__(self, height=0, width=0):
        """
        param:Height
        param:Width
        """
        super(Rectangle, self).__init__(height, width)

    def refFromSuperObject(self,object):
        """
        映射函数，将C#类（父类）中的所有成员赋给python类（子类）
        """
        if object.__class__==ClassLibraryTestt.Rectangle:
            self.Height=object.Height
            self.Width=object.Width
        else:
            print("Wrong object's class in file: \n", __file__)
            input('\nPress "enter" to exit.\n')
            exit()


    def toString(self):
        return super(Rectangle, self).ToString()


def getRectangle(rectangle):
    """
    返回值是自定义类的函数，需要实现在包装文件中继承自定义类，该自定义类需要在C#中实现无参构造函数
    """
    rec=Rectangle() # 在返回值是自定义类的函数的包装函数的函数体中要声明子类
    # 通过映射函数将父类（C#类）对象中的属性赋给子类（python类）对象
    rec.refFromSuperObject(Class1().GetRectangle(rectangle))
    # 返回声明的子类对象作为包装函数的计算结果
    return rec

def test(a, b):
    """
    普通的测试函数，用于测试包装类以及类成员函数能否正常调用。
    调用结果是，类是python的类，而通过python的类生命的对像调用成员函数也没有问题。
    """
    rectangle = Rectangle(a, b)
    print(rectangle.__class__)
    print(rectangle.toString())
    print(rectangle.Height,rectangle.Width)
    return rectangle


if __name__ == '__main__':
    print(square(23), plus(42.5, 55), times(6, 2))  # 测试函数，第一个是平方，第二个是加法，第三个是异或运算(虽函数名不对)
    r=test(35.4, 42.1)
    a = getRectangle(r)
    print(a.toString())
    print("In python, return from C#, a.Height=%.2f, "%a.Height,"a.Width=%.2f. \n"%a.Width)