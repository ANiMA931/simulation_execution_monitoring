import xml.dom.minidom
import numpy as np
from math import inf

def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    dom = xml.dom.minidom.parse(in_path)
    return dom


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


class pattern:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        cif = self.root.getElementsByTagName('commonInformation')[0]
        self.ID = cif.getAttribute('ID')
        self.positions = []
        p = self.root.getElementsByTagName('position')
        for i in p:
            a = {"pID": i.getAttribute('pID'), "name": i.getAttribute('name'), "type": i.getAttribute('type'),
                 "weight": float(i.getAttribute('weight'))}
            self.positions.append(a)
        self.behaviors = []
        b = self.root.getElementsByTagName('behavior')
        for i in b:
            a = {"bID": i.getAttribute('bID'), "before": i.getAttribute('before'), "after": i.getAttribute('after'),
                 "success_rate": float(i.getAttribute('successRate')), "weight": float(i.getAttribute('weight'))}
            self.behaviors.append(a)


    def get_best_way(self,start,target):
        """
        :param target: an ID of a position on pattern
        :param start: an ID of a position on pattern
        :return: a path of lowest cost to target and zhe cost
        """
        p=[]
        for i in self.positions:
            p.append(i['pID'])
        b=[]
        for i in self.behaviors:
            b.append((i['before'],i['after']))
        res=topoSort(p,b)#此处得到了position拓扑排序的序列
        know=[False]*len(res)
        distance=[inf]*len(res)#存储当前距离
        pre_p=['-1']*len(res)#存储计算的当前距离的上一个点
        now=res.index(start)
        distance[now]=0#代表自己
        for i in self.behaviors:
            if res[now]==i['before']:
                for j in self.positions:
                    if res[now]==j['pID']:
                        distance[res.index(i['after'])]=round(i['weight']-j['weight'],5)
                        pre_p[res.index(i['after'])]=res[now]
        know[now]=True
        while not know[res.index(target)]:
            unknown=[]
            tempd=distance.copy()
            for i in range(len(res)):
                if know[i]==False:
                    unknown.append(i)#此处找出来了unknown的列表
            for i in range(len(res)):
                if i not in unknown:
                    tempd[i]='None'
            while 'None' in tempd:
                del tempd[tempd.index('None')]
            now=distance.index(min(tempd))
            for i in self.behaviors:
                if res[now] == i['before']:
                    for j in self.positions:
                        if res[now] == j['pID']:
                            if distance[res.index(i['after'])]>round(distance[now]+i['weight'] - j['weight'], 5):
                                distance[res.index(i['after'])] = round(distance[now]+i['weight'] - j['weight'], 5)
                                pre_p[res.index(i['after'])] = res[now]
            know[now] = True
            pass
        path=[]
        tp=target
        while tp!='-1':
            path.append(tp)
            tp=pre_p[res.index(tp)]
        input()
        return distance[res.index(target)],list(reversed(path))


if __name__ == '__main__':
    a = pattern(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml"))
    print(a.get_best_way('p1','p21'))
