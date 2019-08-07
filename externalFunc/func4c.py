from ctypes import *
class ctopy:
    def __init__(self,lib=CDLL(".\externalFunc\libfunc.dll")):
        #在此处，相对路径的根节点是项目本身，或者说是解释器的所在位置，而不是当前文件的所在位置
        self.lib=lib
    def squre(self,num=0):
        return self.lib.square(num)
