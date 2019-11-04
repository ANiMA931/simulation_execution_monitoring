# pattern.py
from math import inf  # 必要的无穷大

from tools import *  # 必要的部分工具


# 格局类
class pattern:
    def __init__(self, xml_dom):
        '''
        构造函数
        :param xml_dom: 保存着格局的xml的dom对象
        '''
        # 获取dom对象的根节点
        self.root = xml_dom.documentElement
        # 获取xml中的commonInformation标签
        common_information_label = self.root.getElementsByTagName('commonInformation')[0]
        # 获得格局的id（虽然主程序中没用到）
        self.ID = common_information_label.getAttribute('ID')
        # 声明一下格局里面的点的集合
        self.positions = []
        # 声明一下格局的初始点
        self.init_position = None
        # 声明一下格局的所有终点
        self.ending_positions = []
        # 获得xml中的所有position标签与behavior标签
        temporary_position_labels = self.root.getElementsByTagName('position')
        temporary_behavior_labels = self.root.getElementsByTagName('behavior')
        # 初始化保存behavior的集合
        self.behaviors = []
        # 对于每一个behavior标签
        for i in temporary_behavior_labels:
            # 获取标签中的bID、before、after、success_rate、weight、属性作为字典
            temporary_behavior = {"bID": i.getAttribute('bID'), "before": i.getAttribute('before'), "after": i.getAttribute('after'),
                 "success_rate": float(i.getAttribute('successRate')), "weight": float(i.getAttribute('weight'))}
            # 添加到行为集合中
            self.behaviors.append(temporary_behavior)
        # 对于所有position标签
        for i in temporary_position_labels:
            # 取出标签中的pID属性、name属性、type属性、weight属性作为字典存起来
            next_position = []
            for j in self.behaviors:
                if j['before'] == i.getAttribute('pID'):
                    n_p = {"pID": j['after'], "success_rate": j['success_rate'], "weight": j['weight']}
                    next_position.append(n_p)
            temporary_position = {"pID": i.getAttribute('pID'), "name": i.getAttribute('name'), "type": i.getAttribute('type'),
                 "weight": float(i.getAttribute('weight')), "next_position": next_position}
            # 加到集合里面去
            self.positions.append(temporary_position)
            # 如果当前的点的类型是ending即终点，再把这个点的id加到终点集合里面
            if temporary_position['type'] == "ending":
                self.ending_positions.append(temporary_position["pID"])
            # 如果类型是start，把这个点的id赋值为格局的初始点
            elif temporary_position['type'] == "start":
                self.init_position = temporary_position["pID"]
        # 初始化一下格局上能有的所有行为

        # 拿一下所有position的ID
        temporary_position_labels = []
        for i in self.positions:
            temporary_position_labels.append(i['pID'])
        # 拿一下所有behavior的ID
        temporary_behavior_labels = []
        for i in self.behaviors:
            temporary_behavior_labels.append((i['before'], i['after']))
        # 算一下所有点的拓扑排序的序列
        self.topo_sort_sequence = topoSort(temporary_position_labels, temporary_behavior_labels)

    def points_distance(self, start, target):
        '''
        计算两个点之间的距离,该距离是不带权意义的距离，智能从拓扑序列的前列向后找，利用了类似最短路径算法
        :param start: 开始的位置
        :param target: 目标位置
        :return: start与point之间的距离（无权重）,如果start不能到达target，返回None
                 祖传代码，切勿乱改
        '''
        # 如果target的拓扑序列大于start则代表没有路径
        if self.topo_sort_sequence.index(start) > self.topo_sort_sequence.index(target):
            return None
        # is in between表示的意思是，target的拓扑序列在start与所有start的后继节点的中间，
        # 这种情况下，不存在路径能够从start到达target
        if self.is_in_between(start, target):
            return None

        know = [False] * len(self.topo_sort_sequence)  # 该点是否已经遍历的标志位
        distance = [inf] * len(self.topo_sort_sequence)  # 存储距离
        pre_p = ['-1'] * len(self.topo_sort_sequence)  # 存储计算的当前距离的上一个点
        # 初始化程序中保存当前点的变量
        now = self.topo_sort_sequence.index(start)
        old_now = None
        distance[now] = 0  # 初始点与初始点的距离设置为0
        # 格局的最短路径算法实现

        for i in self.positions:
            if self.topo_sort_sequence[now] == i['pID']:
                for j in i['next_position']:
                    distance[self.topo_sort_sequence.index(j['pID'])] = 1
                    pre_p[self.topo_sort_sequence.index(j['pID'])] = self.topo_sort_sequence[now]
        know[now] = True

        # 当寻路时间超过0.05秒表示不可达，但可以更改pattern类的数据结构来避免
        while old_now != now:
            unknown = []
            tempd = distance.copy()
            for i in range(len(self.topo_sort_sequence)):
                if know[i] == False:
                    unknown.append(i)  # 此处找出来了unknown的列表
            for i in range(len(self.topo_sort_sequence)):
                if i not in unknown:
                    tempd[i] = inf
            old_now = now
            now = tempd.index(min(tempd))
            # for i in self.behaviors:
            #     if self.topo_sort_sequence[now] == i['before']:
            #         for j in self.positions:
            #             if self.topo_sort_sequence[now] == j['pID']:bjkl
            #                 if distance[self.topo_sort_sequence.index(i['after'])] > distance[now] + 1:
            #                     distance[self.topo_sort_sequence.index(i['after'])] = distance[now] + 1
            #                     pre_p[self.topo_sort_sequence.index(i['after'])] = self.topo_sort_sequence[now]

            for i in self.positions:
                if self.topo_sort_sequence[now] == i['pID']:
                    for j in i['next_position']:
                        if distance[self.topo_sort_sequence.index(j['pID'])] > distance[now] + 1:
                            distance[self.topo_sort_sequence.index(j['pID'])] = distance[now] + 1
                            pre_p[self.topo_sort_sequence.index(j['pID'])] = self.topo_sort_sequence[now]

            know[now] = True
        if not know[self.topo_sort_sequence.index(target)]:
            return None
        path = []
        tp = target
        while tp != '-1':
            path.append(tp)
            tp = pre_p[self.topo_sort_sequence.index(tp)]
        return distance[self.topo_sort_sequence.index(target)], list(reversed(path))

    def is_in_between(self, start, target):
        '''
        计算target的拓扑序列是否在start与start的所有后继position之间
        :param start:起始点
        :param target:目标点
        :return:
        '''
        # 对于所有的position
        for i in self.positions:
            # 定位到start代表的position
            if start == i['pID']:
                # 对于start的所有后继position
                for j in i['next_position']:
                    #如果发现有一个后继节点的拓扑序列要比target小，表明target不是与start平级的position
                    if self.topo_sort_sequence.index(j['pID']) > self.topo_sort_sequence.index(target):
                        continue
                    else:
                        return False
                return True

    def get_best_way(self, start, target):
        """
        获得起始点与目标点的最佳路径，是带权（权核可能为负）有向无环图的最短路径算法实现。
        :param target: an ID of a position on pattern
        :param start: an ID of a position on pattern
        :return: a path of lowest cost to target and the cost or None if no path from start to target
                 如果start不能到达target，返回None
                 祖传代码，切勿乱改
        """
        # 首先判断start的拓扑序列是否大于target，如果大于则表示不可达，直接return None
        if self.topo_sort_sequence.index(start) > self.topo_sort_sequence.index(target):
            return None
        # 如果target的拓扑序列小于start，但是start的所有后继点的拓扑序列都大于target，表明从start到target没有路径
        if self.is_in_between(start, target):
            return None
        know = [False] * len(self.topo_sort_sequence)
        distance = [inf] * len(self.topo_sort_sequence)  # 存储当前距离
        pre_p = ['-1'] * len(self.topo_sort_sequence)  # 存储计算的当前距离的上一个点
        now = self.topo_sort_sequence.index(start)
        old_now = None
        distance[now] = 0  # 代表自己
        for i in self.positions:
            if self.topo_sort_sequence[now] == i['pID']:
                for j in i['next_position']:
                    distance[self.topo_sort_sequence.index(j['pID'])] = round(i['weight'] - j['weight'], 5)
                    pre_p[self.topo_sort_sequence.index(j['pID'])] = self.topo_sort_sequence[now]
        know[now] = True
        # 当now不再更新，说明找不到更短的路径后
        while old_now != now:
            unknown = []
            tempd = distance.copy()
            for i in range(len(self.topo_sort_sequence)):
                if know[i] == False:
                    unknown.append(i)  # 此处找出来了还有哪些点没有遍历到
            for i in range(len(self.topo_sort_sequence)):
                if i not in unknown:
                    tempd[i] = inf
            old_now = now
            now = tempd.index(min(tempd))
            for i in self.positions:
                if self.topo_sort_sequence[now] == i['pID']:
                    for j in i['next_position']:
                        if distance[self.topo_sort_sequence.index(j['pID'])] > round(
                                distance[now] + i['weight'] - j['weight'], 5):
                            distance[self.topo_sort_sequence.index(j['pID'])] = round(
                                distance[now] + i['weight'] - j['weight'], 5)
                            pre_p[self.topo_sort_sequence.index(j['pID'])] = self.topo_sort_sequence[now]
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
    a = pattern(xml_dom=read_xml("pattern1.xml"))
    # print('start')
    # print(a.get_best_way('p3', 'p22'))
    print(a.points_distance('p3', 'p8'))