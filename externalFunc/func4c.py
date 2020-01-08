# *-本.py文件是针对C语言的包装文件，-*import ctypes
from ctypes import *  # 引入C编译的DLL的函数

# 调用cdll模块的LoadLibrary函数来读取路径代表的DLL文件，括号中填写的是DLL文件的路径，通过lib对象来调用函数。
lib = cdll.LoadLibrary(r'libfunc.dll')


class POINT(Structure):
    _fields_ = [("x", c_double), ("y", c_double)]


class STUDENT(Structure):
    _fields_ = [("name", c_char_p), ("age", c_int), ("position", POINT)]


def square(a):
    """
    函数名需要与.C文件中的函数一致，参数亦需要对应。
    """
    return lib.square(a)


def printPointTest(p):
    lib.printPointTest.restype = POINT
    return lib.printPointTest(p)


def usePointTest(x, y, p_point):
    lib.usePointTest.restype = POINTER(POINT)
    return lib.usePointTest(c_double(x), c_double(y), p_point)


def useStudentTest(p_student, name, age, p_position):
    lib.useStudentTest.restype = POINTER(STUDENT)
    return lib.useStudentTest(p_student, name, age, p_position)


if __name__ == '__main__':
    print(square(26)) # 测试包装的square函数
    p = POINT() # 声明一个POINT结构体对象p
    xp = usePointTest(3.23, 16.2, byref(p)) # 测试usePointTest包装函数，参数是两个浮点数和p的指针，返回值是指针
    print(f'In python, p.x={p.x}, p.y={p.y}') # 输出对象p，查看对象p能否用c函数修改属性
    print(f'In python, xp->x={xp.contents.x}, xp->y={xp.contents.y}') # 输出指针xp，查看用对象的指针访问属性与用对象访问指针的区别
    p0 = printPointTest(p) # 声明p0是printPointTest函数的结果，函数的参数在c语言中定义为一个Point结构体变量
    print(f"In python after change, p0.x={p0.x}, p0.y={p0.y}") # 显示p0的运算结果
    s0 = STUDENT(b"Lucy", 14) # 声明一个student结构体对象，赋值名称与年龄
    # 显示s0的属性
    print(f"Before useStudentTest,s0.name={s0.name}, s0.age={s0.age}, s0.position=({s0.position.x},{s0.position.y})")
    namestr = "ANiMA"
    # 若想将字符串对象赋给C语言的char*指针，字符串对象必须转化为byte类型对象，否则无法赋值
    # 通过指针修改对象内容没有问题，但是通过该对象的指针访问对象属性有问题
    s1 = useStudentTest(byref(s0), namestr.encode('gbk'), 15, byref(p0))
    # 该问题出在直接赋数据没问题，但是不能通过变量名赋变量，否则会有概率出错
    # s1 = useStudentTest(byref(s0), namestr, 15, byref(p0)) # namestr=b"ANiMA"
    # 通过指针修改对象属性后通过对象访问其属性没有问题，
    print(f"After useStudentTest,s0.name={s0.name}, s0.age={s0.age}, s0.position=({s0.position.x},{s0.position.y})")
    # 但是通过该对象的指针访问对象属性有问题
    print(f"s1.contents.name={s1.contents.name}, s1.contents.age={s1.contents.age}, " ,end='')
    print(f"s1.contents.position=({s1.contents.position.x},{s1.contents.position.y})")
    s1.contents.name="Zeva".encode('gbk')
    print(s0.name,s1.contents.name)


