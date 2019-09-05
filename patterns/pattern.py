from time import time
from math import inf

from tools import *


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
        p = []
        for i in self.positions:
            p.append(i['pID'])
        b = []
        for i in self.behaviors:
            b.append((i['before'], i['after']))
        self.topo_sort_sequence = topoSort(p, b)

    def points_distance(self, start, target):
        know = [False] * len(self.topo_sort_sequence)
        distance = [inf] * len(self.topo_sort_sequence)  # 存储当前距离
        pre_p = ['-1'] * len(self.topo_sort_sequence)  # 存储计算的当前距离的上一个点
        now = self.topo_sort_sequence.index(start)
        distance[now] = 0  # 代表自己
        for i in self.behaviors:
            if self.topo_sort_sequence[now] == i['before']:
                for j in self.positions:
                    if self.topo_sort_sequence[now] == j['pID']:
                        distance[self.topo_sort_sequence.index(i['after'])] = 1
                        pre_p[self.topo_sort_sequence.index(i['after'])] = self.topo_sort_sequence[now]

        know[now] = True
        t = time()
        while time()-t<2 and not know[self.topo_sort_sequence.index(target)]:  # 寻路超过1秒视为无法到达
            unknown = []
            tempd = distance.copy()
            for i in range(len(self.topo_sort_sequence)):
                if know[i] == False:
                    unknown.append(i)  # 此处找出来了unknown的列表
            for i in range(len(self.topo_sort_sequence)):
                if i not in unknown:
                    tempd[i] = inf
            now = tempd.index(min(tempd))
            for i in self.behaviors:
                if self.topo_sort_sequence[now] == i['before']:
                    for j in self.positions:
                        if self.topo_sort_sequence[now] == j['pID']:
                            if distance[self.topo_sort_sequence.index(i['after'])] > distance[now] + 1:
                                distance[self.topo_sort_sequence.index(i['after'])] = distance[now] + 1
                                pre_p[self.topo_sort_sequence.index(i['after'])] = self.topo_sort_sequence[now]
            know[now] = True
        if not know[self.topo_sort_sequence.index(target)]:
            return None
        path = []
        tp = target
        while tp != '-1':
            path.append(tp)
            tp = pre_p[self.topo_sort_sequence.index(tp)]
        return distance[self.topo_sort_sequence.index(target)], list(reversed(path))

    def get_best_way(self, start, target):
        """
        :param target: an ID of a position on pattern
        :param start: an ID of a position on pattern
        :return: a path of lowest cost to target and zhe cost
        """

        know = [False] * len(self.topo_sort_sequence)
        distance = [inf] * len(self.topo_sort_sequence)  # 存储当前距离
        pre_p = ['-1'] * len(self.topo_sort_sequence)  # 存储计算的当前距离的上一个点
        now = self.topo_sort_sequence.index(start)
        distance[now] = 0  # 代表自己
        for i in self.behaviors:
            if self.topo_sort_sequence[now] == i['before']:
                for j in self.positions:
                    if self.topo_sort_sequence[now] == j['pID']:
                        distance[self.topo_sort_sequence.index(i['after'])] = round(i['weight'] - j['weight'], 5)
                        pre_p[self.topo_sort_sequence.index(i['after'])] = self.topo_sort_sequence[now]

        know[now] = True
        t = time()
        while time() - t < 2 and not know[self.topo_sort_sequence.index(target)]:  # 寻路超过1秒视为无法到达
            unknown = []
            tempd = distance.copy()
            for i in range(len(self.topo_sort_sequence)):
                if know[i] == False:
                    unknown.append(i)  # 此处找出来了unknown的列表
            for i in range(len(self.topo_sort_sequence)):
                if i not in unknown:
                    tempd[i] = inf
            now = tempd.index(min(tempd))
            for i in self.behaviors:
                if self.topo_sort_sequence[now] == i['before']:
                    for j in self.positions:
                        if self.topo_sort_sequence[now] == j['pID']:
                            if distance[self.topo_sort_sequence.index(i['after'])] > round(
                                    distance[now] + i['weight'] - j['weight'], 5):
                                distance[self.topo_sort_sequence.index(i['after'])] = round(
                                    distance[now] + i['weight'] - j['weight'], 5)
                                pre_p[self.topo_sort_sequence.index(i['after'])] = self.topo_sort_sequence[now]
            know[now] = True
        if not know[self.topo_sort_sequence.index(target)]:
            return None
        path = []
        tp = target
        while tp != '-1':
            path.append(tp)
            tp = pre_p[self.topo_sort_sequence.index(tp)]
        return distance[self.topo_sort_sequence.index(target)], list(reversed(path))


if __name__ == '__main__':
    a = pattern(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml"))
    print('start')
    print(a.get_best_way('p24', 'p21'))
    print(a.points_distance('p24', 'p21'))
