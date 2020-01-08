import matlab # 必要的包引用
import matlab.engine # 必要的包引用
engine = matlab.engine.start_matlab() # matlab的engine的实例化


def add(a, b, c):
    """
    add函数的.m文件在本文件的相同目录下
    """
    return engine.add(a, b, c)


def square(a):
    """
    square函数的.m文件不在本文件的相同目录下
    """
    return engine.square(a)


if __name__ == '__main__':
    # add函数可以正常调用
    a = add(9, 3, 8)
    # square函数不能正常调用，系统会随机返回1或者-1。
    b = square(126)
    print(a,b)
