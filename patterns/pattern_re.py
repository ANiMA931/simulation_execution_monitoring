# pattern.py
import numpy as np
import pandas as pd
from math import inf  # 必要的无穷大
from my_tools import *  # 必要的部分工具


# 格局类
class pattern:
    def __init__(self, xml_dom):
        """
        构造函数
        :param xml_dom: 保存着格局的xml的dom对象
        """
        # 获取dom对象的根节点
        root = xml_dom.documentElement
        # 获取xml中的commonInformation标签
        common_information_label = root.getElementsByTagName('commonInformation')[0]
        # 获得格局的id（虽然主程序中没用到）
        self.ID = common_information_label.getAttribute('ID')
        # 声明一下格局里面的点的集合
        self.positions = []
        # 声明一下格局的初始点
        self.init_position = None
        # 声明一下格局的所有终点
        self.ending_positions = []
        # 获得xml中的所有position标签与behavior标签
        temporary_position_labels = root.getElementsByTagName('position')
        temporary_behavior_labels = root.getElementsByTagName('behavior')
        # 初始化保存behavior的集合
        self.behaviors = []
        # 对于每一个behavior标签
        for i in temporary_behavior_labels:
            # 获取标签中的bID、before、after、success_rate、weight、属性作为字典
            temporary_behavior = {"bID": i.getAttribute('bID'), "before": i.getAttribute('before'),
                                  "after": i.getAttribute('after'),
                                  "success_rate": float(i.getAttribute('successRate')),
                                  "weight": float(i.getAttribute('weight'))}
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
            temporary_position = {"pID": i.getAttribute('pID'), "name": i.getAttribute('name'),
                                  "type": i.getAttribute('type'),
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
        self.topo_sort_sequence = topoSort(temporary_position_labels.copy(), temporary_behavior_labels)
        # Floyd算法需要的连接矩阵
        self.position_link_matrix = pd.DataFrame(index=temporary_position_labels, columns=temporary_position_labels,
                                                 dtype=np.float)
        self.position_link_matrix[:][:] = np.inf
        # Floyd算法扩展的路径矩阵初始化
        self.position_link_path = pd.DataFrame(index=temporary_position_labels, columns=temporary_position_labels)
        # 初始化邻接矩阵，首先声明边与点的权重差
        temporary_b_p_weight_difference = float(0)
        for b in self.behaviors:
            for p in self.positions:
                if p['pID'] == b['after']:
                    temporary_b_p_weight_difference = b['weight'] - p['weight']
                    break
            self.position_link_matrix[b['before']][b['after']] = temporary_b_p_weight_difference
            self.position_link_path[b['before']][b['after']] = b['before']
        floyd_with_path(self.position_link_matrix, self.position_link_path)


def points_distance(the_pattern, start, target):
    path=[target]
    mid_position = the_pattern.position_link_path[start][target]
    while mid_position != start:
        path.append(mid_position)
        mid_position=the_pattern.position_link_path[start][mid_position]
    path.append(start)
    return len(path)-1, list(reversed(path))


def get_best_way(the_pattern, start, target):
    """
    获得起始点与目标点的最佳路径，是带权（权核可能为负）有向无环图的最短路径算法实现。
    :param target: an ID of a position on pattern
    :param start: an ID of a position on pattern
    :return: a path of lowest cost to target and the cost or None if no path from start to target
             如果start不能到达target，返回None
             祖传代码，切勿乱改
    """
    w = the_pattern.position_link_matrix[start][target]
    if w == np.inf:
        return None
    path = [target]
    mid_position = the_pattern.position_link_path[start][target]
    while mid_position != start:
        path.append(mid_position)
        mid_position = the_pattern.position_link_path[start][mid_position]
    path.append(start)
    return w, list(reversed(path))


if __name__ == '__main__':
    a = pattern(xml_dom=read_xml("pattern1.xml"))
    # print('start')
    print(get_best_way(a, 'p24', 'p22'))
    print(points_distance(a, 'p24', 'p22'))
