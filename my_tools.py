import xml.dom.minidom
import os
from random import random


def read_xml(in_path)->xml.dom.minidom.Document:
    """
    读取并解析xml文件
    :param in_path: xml路径
    :return: ElementTree
    """
    try:
        dom = xml.dom.minidom.parse(in_path)
        return dom
    except:
        print("file path error.\n")


def member_file_name(path):
    """
    读取一个文件夹下的所有文件的文件名
    :param path:
    :return:
    """
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    for f in files:
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    return fileList


def shatter_number(upper, length):
    """
    将一个数撕裂为一个设定长度的随机数组
    :param upper:要被撕裂的数
    :param length:设定被撕裂的长度
    :return:r被撕裂的随机数列表，sum(r)随机数列表和
    """
    r = []
    for i in range(length):
        r.append(random())
    a_s = upper / sum(r)
    for i in range(len(r)):
        r[i] *= a_s
    return r, sum(r)


def in_degree0(v, e):
    '''
    辅拓扑排序辅助函数
    :param v:
    :param e:
    :return:
    '''
    if v == []:
        return None
    tmp = v[:]
    for i in e:
        if i[1] in tmp:
            tmp.remove(i[1])
    if tmp == []:
        return -1

    for t in tmp:
        for i in range(len(e)):
            if t in e[i]:
                e[i] = 'toDel'  # 占位，之后删掉
    if e:
        eset = set(e)
        eset.remove('toDel')
        e[:] = list(eset)
    if v:
        for t in tmp:
            v.remove(t)
    return tmp


def topoSort(v, e):
    '''
    拓扑排序函数，外界复制而来，切勿乱动
    :param v:点的集合
    :param e:边的集合
    :return:一个拓扑排序序列
    '''
    result = []
    while True:
        nodes = in_degree0(v, e)
        if nodes == None:
            break
        if nodes == -1:
            print('there\'s a circle.')
            return None
        result.extend(nodes)
    return result


def write_xml(path, dom):
    '''
    xml存储函数
    :param path:存储路径
    :param dom:描述xml的dom对象
    :return:no return
    '''
    try:
        with open(path, 'w', encoding='UTF-8') as fh:
            dom.writexml(fh)
    except:
        print("error")


def printPath(level, path):
    '''
    打印一个目录下的所有文件夹和文件，外界引用而来，切勿乱动
    :param level:
    :param path:
    :return:
    '''
    allFileNum = 0

    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print('-' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    for fl in fileList:
        # 打印文件
        print('-' * (int(dirList[0])), fl)
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1


def floyd_with_path(weight_matrix, path_matrix):
    for k in weight_matrix.columns:
        for i in weight_matrix.columns:
            for j in weight_matrix.index:
                if weight_matrix[i][j] > weight_matrix[i][k] + weight_matrix[k][j]:
                    weight_matrix[i][j] = weight_matrix[i][k] + weight_matrix[k][j]
                    path_matrix[i][j] = k

