import xml.dom.minidom
import os

def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    try:
        dom = xml.dom.minidom.parse(in_path)
        return dom
    except:
        print("file path error, press any key to exit.")
        input()
        exit()


def member_file_name(path):
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


def in_degree0(v, e):
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
    try:
        with open(path, 'w', encoding='UTF-8') as fh:
            dom.writexml(fh)
    except:
        print("error")
