# pattern.py
import numpy as np
import pandas as pd
from my_tools import *  # 必要的部分工具


# 格局类
class pattern:
    def __init__(self, xml_dom):
        '''
        构造函数
        :param xml_dom: 保存着格局的xml的dom对象
        '''
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

"""因修改底层代码，无需此函数辅助"""
# def is_in_between(the_pattern, start, target):
#     """
#     计算target的拓扑序列是否在start与start的所有后继position之间
#     :param the_pattern:
#     :param start: 起始点ID
#     :param target: 目标点ID
#     :return:
#     """
#     # 对于所有的position
#     for i in the_pattern.positions:
#         # 定位到start代表的position
#         if start == i['pID']:
#             # 对于start的所有后继position
#             for j in i['next_position']:
#                 # 如果发现有一个后继节点的拓扑序列要比target小，表明target不是与start平级的position
#                 if the_pattern.topo_sort_sequence.index(j['pID']) > the_pattern.topo_sort_sequence.index(target):
#                     continue
#                 else:
#                     return False
#             return True

"""新的函数已经准备好，而且效果更佳"""
# def points_distance(the_pattern, start, target):
#     """
#     计算两个点之间的距离,该距离是不带权意义的距离，智能从拓扑序列的前列向后找，利用了类似最短路径算法
#     :param the_pattern:
#     :param start: 开始的位置
#     :param target: 目标位置
#     :return: start与point之间的距离（无权重）,如果start不能到达target，返回None
#              祖传代码，切勿乱改
#     """
#     # 如果target的拓扑序列大于start则代表没有路径
#     if the_pattern.topo_sort_sequence.index(start) > the_pattern.topo_sort_sequence.index(target):
#         return None
#     # is in between表示的意思是，target的拓扑序列在start与所有start的后继节点的中间，
#     # 这种情况下，不存在路径能够从start到达target
#     if is_in_between(the_pattern, start, target):
#         return None
#
#     know = [False] * len(the_pattern.topo_sort_sequence)  # 该点是否已经遍历的标志位
#     distance = [inf] * len(the_pattern.topo_sort_sequence)  # 存储距离
#     pre_p = ['-1'] * len(the_pattern.topo_sort_sequence)  # 存储计算的当前距离的上一个点
#     # 初始化程序中保存当前点的变量
#     now = the_pattern.topo_sort_sequence.index(start)
#     old_now = None
#     distance[now] = 0  # 初始点与初始点的距离设置为0
#     # 格局的最短路径算法实现
#
#     for i in the_pattern.positions:
#         if the_pattern.topo_sort_sequence[now] == i['pID']:
#             for j in i['next_position']:
#                 distance[the_pattern.topo_sort_sequence.index(j['pID'])] = 1
#                 pre_p[the_pattern.topo_sort_sequence.index(j['pID'])] = the_pattern.topo_sort_sequence[now]
#     know[now] = True
#
#     while old_now != now:
#         unknown = []
#         tempd = distance.copy()
#         for i in range(len(the_pattern.topo_sort_sequence)):
#             if know[i] == False:
#                 unknown.append(i)  # 此处找出来了unknown的列表
#         for i in range(len(the_pattern.topo_sort_sequence)):
#             if i not in unknown:
#                 tempd[i] = inf
#         old_now = now
#         now = tempd.index(min(tempd))
#
#         for i in the_pattern.positions:
#             if the_pattern.topo_sort_sequence[now] == i['pID']:
#                 for j in i['next_position']:
#                     if distance[the_pattern.topo_sort_sequence.index(j['pID'])] > distance[now] + 1:
#                         distance[the_pattern.topo_sort_sequence.index(j['pID'])] = distance[now] + 1
#                         pre_p[the_pattern.topo_sort_sequence.index(j['pID'])] = the_pattern.topo_sort_sequence[now]
#
#         know[now] = True
#     if not know[the_pattern.topo_sort_sequence.index(target)]:
#         return None
#     path = []
#     tp = target
#     while tp != '-1':
#         path.append(tp)
#         tp = pre_p[the_pattern.topo_sort_sequence.index(tp)]
#     return distance[the_pattern.topo_sort_sequence.index(target)], list(reversed(path))
#
# 新的函数效果更佳
# def get_best_way(the_pattern, start, target):
#     """
#     获得起始点与目标点的最佳路径，是带权（权核可能为负）有向无环图的最短路径算法实现。
#     :param target: an ID of a position on pattern
#     :param start: an ID of a position on pattern
#     :return: a path of lowest cost to target and the cost or None if no path from start to target
#              如果start不能到达target，返回None
#              祖传代码，切勿乱改
#     """
#     # 首先判断start的拓扑序列是否大于target，如果大于则表示不可达，直接return None
#     if the_pattern.topo_sort_sequence.index(start) > the_pattern.topo_sort_sequence.index(target):
#         return None
#     # 如果target的拓扑序列小于start，但是start的所有后继点的拓扑序列都大于target，表明从start到target没有路径
#     if is_in_between(the_pattern, start, target):
#         return None
#     know = [False] * len(the_pattern.topo_sort_sequence)
#     distance = [inf] * len(the_pattern.topo_sort_sequence)  # 存储当前距离
#     pre_p = ['-1'] * len(the_pattern.topo_sort_sequence)  # 存储计算的当前距离的上一个点
#     now = the_pattern.topo_sort_sequence.index(start)
#     old_now = None
#     distance[now] = 0  # 代表自己
#     for i in the_pattern.positions:
#         if the_pattern.topo_sort_sequence[now] == i['pID']:
#             for j in i['next_position']:
#                 distance[the_pattern.topo_sort_sequence.index(j['pID'])] = round(i['weight'] - j['weight'], 5)
#                 pre_p[the_pattern.topo_sort_sequence.index(j['pID'])] = the_pattern.topo_sort_sequence[now]
#     know[now] = True
#     # 当now不再更新，说明找不到更短的路径后
#     while old_now != now:
#         unknown = []
#         tempd = distance.copy()
#         for i in range(len(the_pattern.topo_sort_sequence)):
#             if know[i] == False:
#                 unknown.append(i)  # 此处找出来了还有哪些点没有遍历到
#         for i in range(len(the_pattern.topo_sort_sequence)):
#             if i not in unknown:
#                 tempd[i] = inf
#         old_now = now
#         now = tempd.index(min(tempd))
#         for i in the_pattern.positions:
#             if the_pattern.topo_sort_sequence[now] == i['pID']:
#                 for j in i['next_position']:
#                     if distance[the_pattern.topo_sort_sequence.index(j['pID'])] > distance[now] + i['weight'] - j[
#                         'weight']:
#                         distance[the_pattern.topo_sort_sequence.index(j['pID'])] = distance[now] + i['weight'] - j[
#                             'weight']
#                         pre_p[the_pattern.topo_sort_sequence.index(j['pID'])] = the_pattern.topo_sort_sequence[now]
#         know[now] = True
#     if not know[the_pattern.topo_sort_sequence.index(target)]:
#         return None
#     path = []
#     tp = target
#     while tp != '-1':
#         path.append(tp)
#         tp = pre_p[the_pattern.topo_sort_sequence.index(tp)]
#     return distance[the_pattern.topo_sort_sequence.index(target)], list(reversed(path))
def points_distance(the_pattern, start, target):
    """

    :param the_pattern:
    :param start:
    :param target:
    :return: 路径的深度与路径的内容
    """
    if the_pattern.position_link_path[start][target] is np.nan:
        return None
    path = [target]
    mid_position = the_pattern.position_link_path[start][target]
    while mid_position != start:
        path.append(mid_position)
        mid_position = the_pattern.position_link_path[start][mid_position]
    path.append(start)
    return len(path) - 1, list(reversed(path))


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
