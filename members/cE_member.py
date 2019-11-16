# cE_member.py
'''
本文件是众进化仿真成员的类文件
'''
from tools import *  # 必要的工具
from numpy.random import rand  # 必要的随机函数
from math import inf  # 必要的无穷大
from patterns.pattern import *  # 必要的pattern类


# unit类
class unit:
    """

    """
    def __init__(self, xml_dom):
        '''
        unit类构造函数，通过外界传入的xml的dom对象建立
        :param xml_dom: 外界传入的dom对象
        '''
        # 获得dom文件的根节点
        self.root = xml_dom.documentElement
        member_type = self.root.getElementsByTagName('memberType')[0]
        self.id = member_type.getAttribute('ID')
        self.target = self.root.getElementsByTagName('target')[0].getAttribute('pID')
        # 获得now标签，并从now标签获得pID属性（unit当前在格局上的位置是通过存储一个格局上的点（position）的id表示的，初始情况为init点
        self.now = self.root.getElementsByTagName('now')[0].getAttribute('pID')
        # 设置unit的状态为active即活跃的
        self.status = 'active'
        # 从membertype标签中获得该unit成员拥有的资源（resource）
        self.resource = float(member_type.getAttribute('resource'))
        # 用另一个变量再存一次，因为仿真过程中资源量会变，需要一个变量存储该单元拥有的最初资源
        self.init_resource = float(member_type.getAttribute('resource'))
        # 记录已走过的路，当前所在的位置也算入其中
        self.past_way = [self.now]  # 已经走过的路
        # unit的格局的存储路径，用于对比成员的路径是否相同
        self.ptn = self.root.getElementsByTagName('pattern')[0].getAttribute('path')
        # 获得effector标签
        effector_label = self.root.getElementsByTagName('effector')[0]
        # 获得所有advisor标签
        advisor_labels = self.root.getElementsByTagName('advisor')
        # 初始化与unit相连的建议者们
        advisors = {}
        # 对于每个advisor标签
        for i in advisor_labels:
            # 获得advisor标签的aID属性作为dict的key，strength属性作为dict的value,凑出来一个临时的advisor变量
            temporary_advisor = {i.getAttribute('aID'): float(i.getAttribute('strength'))}
            # 将获得dict添加到advisors里
            advisors.update(temporary_advisor)
        # 初始化unit的影响器，endowment为受影响禀赋，remain为禀赋剩余，scale为连接建议者的个数，advisors为建议者们的字典，通过id访问
        self.effector = {"endowment": float(effector_label.getAttribute('endowment')),
                         "remain": float(effector_label.getAttribute('remain')),
                         "scale": int(effector_label.getAttribute('scale')), "advisors": advisors}
        # 获得xml中decider标签
        decider_label = self.root.getElementsByTagName('decider')[0]
        # 初始化unit的决策器，depth是unit能在pattern上眺望的距离，selfConfidence是unit的自信程度，本质与advisors里的strength相同，
        # strategy为决策的策略，目前仅作为可能必要的条目存在，尚未在仿真过程中使用
        self.decider = {"depth": int(decider_label.getAttribute('depth')),
                        "selfConfidence": float(decider_label.getAttribute('selfConfidence')),
                        "strategy": decider_label.getAttribute('strategy')}
        # 获得xml中的executor标签
        executor_label = self.root.getElementsByTagName('executor')[0]
        # 获得xml中所有的monitor
        monitor_labels = self.root.getElementsByTagName('monitor')
        # 初始化监控者的集合
        monitors = []
        # 对于每个monitor标签
        for i in monitor_labels:
            # 以"mID"为key，具体的id值为value
            temporary_monitor = {"mID": i.getAttribute('mID')}
            # 存入monitors中
            monitors.append(temporary_monitor)
        # 初始化unit的执行器，mutationRate为突变率，selfDegeneration为自退化度，selfDiscipline为自律水平，scale为连接的监控者的数量
        # monitors为监控者的集合
        self.executor = {"mutationRate": float(executor_label.getAttribute('mutationRate')),
                         "selfDegeneration": float(executor_label.getAttribute('selfDegeneration')),
                         "selfDiscipline": float(executor_label.getAttribute('selfDiscipline')),
                         "scale": int(executor_label.getAttribute('scale')), "monitors": monitors}
        # 获得xml中parameter标签
        parameter_label = self.root.getElementsByTagName('parameter')[0]
        # 获得所有的cUnit标签
        conn_unit_labels = self.root.getElementsByTagName('cUnit')
        # 初始化与本unit相连的unit们
        conn_units = {}
        # 对于每个cUnit标签
        for i in conn_unit_labels:
            # 以uID属性为key，strength属性为value
            temporary_conn_unit = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            # 存到unit们中
            conn_units.update(temporary_conn_unit)
        # 初始化unit的联接器
        self.parameter = {"endowment": float(parameter_label.getAttribute('endowment')),
                          "remain": float(parameter_label.getAttribute('remain')),
                          "scale": int(parameter_label.getAttribute('scale')), "conn_units": conn_units}
        self.action_sequence = []

    def make_decision(self, pattern):
        """
        成员自己本身根据自己所在的位置做决策
        :param pattern:格局
        :return:一个tuple二元组
        """
        # 先眺望自己能到什么地方，over_list是字典，key为眺望的距离，value是眺望该距离能到达的position
        overlook_dict = self.overlook(pattern)
        # 对于所有的能眺望到的点
        for i in overlook_dict:
            if self.target in overlook_dict[i]:  # 已经眺望到了自己的目标
                c, path = pattern.get_best_way(self.now, self.target)  # 能眺望到自己的目标就可以用最短路径算法了
                return (path[0], path[1])
            else:  # 没有眺望到自己的目标
                mc = inf
                mp = []
                mx = max(overlook_dict.keys())
                while not overlook_dict[mx]:
                    mx -= 1
                else:  # 找到了能走到的最远的position们（可能存在眺望的距离比剩下的路更长的情况，基本在一轮仿真的后期）
                    for j in overlook_dict[mx]:  # 最远的position们
                        cp = pattern.get_best_way(self.now, j)  # 相继找最好的路径
                        if cp[0] < mc:  # 留最小的
                            mc = cp[0]
                            mp = cp[1]
                    return (mp[0], mp[1])

    def overlook(self, pattern):
        """
        眺望，看自己能看到什么地方
        :param now: 目前的所在点
        :param pattern: 眺望的格局
        :return:能眺望到的点们，以字典形式呈现，item是眺望几步，value是对应几步后能到的点的列表
        """
        # 用dict初始化一下存储点的集合
        overlook_dict = {}
        # 对于能眺望的距离
        for i in range(1, self.decider['depth'] + 1):
            # 初始化存储点的列表
            overlook_dict.update({i: []})
        # 对于以拓扑排序后的格局上的点的列表
        for i in pattern.topo_sort_sequence:
            # 排在在当前点后面的拓扑序列的点默认可达（实际上存在不可达的情况）
            if pattern.topo_sort_sequence.index(self.now) < pattern.topo_sort_sequence.index(i):
                # 获取当前遍历的点到当前点的步数距离
                a = pattern.points_distance(self.now, i)
                # 不为None（即不可达）并且距离小于决策器深度，则表示该点能被眺望到
                if a is not None and a[0] <= self.decider['depth']:
                    overlook_dict[a[0]].append(i)  # 依照距离存储该点
        return overlook_dict

    def self_check(self, pattern):
        '''
        检查自己的当前状态，到达目标为succeed，到达了非目标的终点为wrong，走到半截剩余资源不够做任何事情则为died
        :param: 格局pattern
        :return:no return
        '''
        if self.now == self.target:
            self.status = 'succeed'
        elif self.now in pattern.ending_positions and self.now != self.target:
            self.status = 'wrong'
        elif self.now not in pattern.ending_positions and self.is_impasse(pattern):  # 当前所在位置，所剩资源无法进行任何动作
            self.status = 'died'
        else:
            return

    def is_impasse(self, pattern):
        '''
        判断当前状态还能不能进行下一步
        :param pattern: 格局对象
        :return: 能否进行任意下一步
        '''
        next_behaviors = []
        for p in pattern.behaviors:  # 此处的p是字典
            if self.now == p['before']:
                next_behaviors.append(p)
        for p in next_behaviors:
            if self.resource >= p['weight']:
                return False
        return True

    def select_decision(self, decisions, pattern):
        """
        在诸多建议中选择一个建议
        :param decisions:列表，每个元素是一个建议，三元组，分别存储着建议的来源即ID、建议的强度与behavior即二元组
        :return:一个二元组,第一个是行为子二元组，第二个是行为权重
        :此函数需要重构
        """
        alternative_decisions = []
        alternative_decision_weights = []
        for i in decisions:  # 去重
            if i[2] not in alternative_decisions and i[2] is not None:
                alternative_decisions.append(i[2])
                for j in pattern.behaviors:
                    for k in pattern.positions:
                        if i[2][0] == j['before'] and i[2][1] == j['after'] and i[2][1] == k['pID']:
                            alternative_decision_weights.append(k['weight'] - j['weight'])
        # 把资源无法满足的选项给删掉
        for i in range(len(alternative_decisions)):
            if alternative_decision_weights[i] > self.resource:
                alternative_decisions[i] = alternative_decision_weights[i] = None
        while None in alternative_decisions:
            del alternative_decisions[alternative_decisions.index(None)]
            del alternative_decision_weights[alternative_decision_weights.index(None)]
        e = []
        for i in alternative_decisions:  # 对于每条选择,先
            ei = 0
            for j in decisions:
                if j[0] != self.id:
                    if i == j[2]:
                        ei += self.effector['advisors'][j[0]] + j[1]
                else:
                    if i == j[2]:
                        ei += j[1]
            e.append(ei)
        # 此时拿到了所有建议以及决策以及权重
        result = []
        for i in range(len(alternative_decisions)):
            result.append(e[i] * alternative_decision_weights[i])
        return (
            alternative_decisions[result.index(max(result))], alternative_decision_weights[result.index(max(result))])

    # def do_behavior(self, pattern, behavior):
    #     """
    #     执行动作，如果成功则更改自己的now，扣除动作的weight之后并获得动作结果对应的position的weight
    #     如果失败，则不更改自己的now，并扣除动作的weight，没有任何获得
    #     :param pattern:格局对象
    #     :param behavior:要做的行为
    #     :return:行为结果与行为
    #     """
    #     for i in pattern.behaviors:  # 此处的i是字典
    #         if ((i['before'], i['after']) == behavior):  # 定位到了对应的behavior
    #             r = rand()
    #             if r < float(i['success_rate']):
    #                 self.now = i['after']
    #                 self.resource -= i['weight']
    #                 self.past_way.append(i['after'])
    #                 for j in pattern.positions:
    #                     if j['pID'] == i['after']:
    #                         self.resource += j['weight']  # 在position上得到的权重被视为能够加进unit的resource里面
    #                         self.action_sequence.append(('success', behavior))
    #                         return ('success', behavior)
    #             else:
    #                 self.resource -= i['weight']
    #                 self.action_sequence.append(('fail', behavior))
    #                 return ('fail', behavior)

    def get_para_message(self, res_unit, result, round):
        '''
        获取比较信息
        :param res_unit:传来信息的unit的ID（后期会改成名字，unit中也有存名字的标签属性）
        :param result:传来信息的unit的行为
        :return:no return
        '''
        # 原本是用于在界面显示信息的代码，但由于跨线程调用资源导致不稳定而放弃

        try:
            print(self.id + " get a message from " + res_unit.id + ". " + res_unit.id + " do a behavior from " +
                  result[1][
                      0] + " to " + result[1][1] + ". " + res_unit.id + " " + result[0])
        except:
            input()
        round_message = [{"round": round, "message_from": res_unit.id, "action": result[1], "access": result[0]}]
        return {self.id: round_message}

    def reset_connection(self):
        '''
        重设连接关系，一次仿真后，要重新设定一下单元间的连接关系，否则程序不会再仿真，而是直接执行记录并退出
        目前仅仅是随机设置重连，而非有算法地重连。
        :return:
        '''
        length = len(self.effector['advisors']) + 1
        upper = self.effector['endowment']
        r, s = shatter_number(upper, length)
        itemm = 0
        for a in self.effector['advisors'].items():
            self.effector['advisors'][a[0]] = r[itemm]
            itemm += 1
        self.effector['remain'] = r[itemm]

def do_behavior(one_unit, pattern, behavior):
    """
    执行动作，如果成功则更改自己的now，扣除动作的weight之后并获得动作结果对应的position的weight
    如果失败，则不更改自己的now，并扣除动作的weight，没有任何获得
    :param pattern:格局对象
    :param behavior:要做的行为
    :return:行为结果与行为
    """
    for i in pattern.behaviors:  # 此处的i是字典
        if ((i['before'], i['after']) == behavior):  # 定位到了对应的behavior
            r = rand()
            if r < float(i['success_rate']):
                one_unit.now = i['after']
                one_unit.resource -= i['weight']
                one_unit.past_way.append(i['after'])
                for j in pattern.positions:
                    if j['pID'] == i['after']:
                        one_unit.resource += j['weight']  # 在position上得到的权重被视为能够加进unit的resource里面
                        one_unit.action_sequence.append(('success', behavior))
                        return ('success', behavior)
            else:
                one_unit.resource -= i['weight']
                one_unit.action_sequence.append(('fail', behavior))
                return ('fail', behavior)
def overlook(one_unit, pattern):
    """
    眺望，看自己能看到什么地方
    :param now: 目前的所在点
    :param pattern: 眺望的格局
    :return:能眺望到的点们，以字典形式呈现，item是眺望几步，value是对应几步后能到的点的列表
    """
    # 用dict初始化一下存储点的集合
    overlook_dict = {}
    # 对于能眺望的距离
    for i in range(1, one_unit.decider['depth'] + 1):
        # 初始化存储点的列表
        overlook_dict.update({i: []})
    # 对于以拓扑排序后的格局上的点的列表
    for i in pattern.topo_sort_sequence:
        # 排在在当前点后面的拓扑序列的点默认可达（实际上存在不可达的情况）
        if pattern.topo_sort_sequence.index(one_unit.now) < pattern.topo_sort_sequence.index(i):
            # 获取当前遍历的点到当前点的步数距离
            a = points_distance(pattern, one_unit.now, i)
            # 不为None（即不可达）并且距离小于决策器深度，则表示该点能被眺望到
            if a is not None and a[0] <= one_unit.decider['depth']:
                overlook_dict[a[0]].append(i)  # 依照距离存储该点
    return overlook_dict


def make_decision(one_unit, pattern):
    """
    成员自己本身根据自己所在的位置做决策
    :param pattern:格局
    :return:一个tuple二元组
    """
    # 先眺望自己能到什么地方，over_list是字典，key为眺望的距离，value是眺望该距离能到达的position
    overlook_dict = overlook(one_unit, pattern)
    # 对于所有的能眺望到的点
    for i in overlook_dict:
        if one_unit.target in overlook_dict[i]:  # 已经眺望到了自己的目标
            c, path = get_best_way(pattern, one_unit.now, one_unit.target)  # 能眺望到自己的目标就可以用最短路径算法了
            return (path[0], path[1])
        else:  # 没有眺望到自己的目标
            mc = inf
            mp = []
            mx = max(overlook_dict.keys())
            while not overlook_dict[mx]:
                mx -= 1
            else:  # 找到了能走到的最远的position们（可能存在眺望的距离比剩下的路更长的情况，基本在一轮仿真的后期）
                for j in overlook_dict[mx]:  # 最远的position们
                    cp = get_best_way(pattern, one_unit.now, j)  # 相继找最好的路径
                    if cp[0] < mc:  # 留最小的
                        mc = cp[0]
                        mp = cp[1]
                return (mp[0], mp[1])


def select_decision(one_unit, decisions, pattern):
    """
    在诸多建议中选择一个建议
    :param decisions:列表，每个元素是一个建议，三元组，分别存储着建议的来源即ID、建议的强度与behavior即二元组
    :return:一个二元组,第一个是行为子二元组，第二个是行为权重
    :此函数需要重构
    """
    alternative_decisions = []
    alternative_decision_weights = []
    for i in decisions:  # 去重
        if i[2] not in alternative_decisions and i[2] is not None:
            alternative_decisions.append(i[2])
            for j in pattern.behaviors:
                for k in pattern.positions:
                    if i[2][0] == j['before'] and i[2][1] == j['after'] and i[2][1] == k['pID']:
                        alternative_decision_weights.append(k['weight'] - j['weight'])
    # 把资源无法满足的选项给删掉
    for i in range(len(alternative_decisions)):
        if alternative_decision_weights[i] > one_unit.resource:
            alternative_decisions[i] = alternative_decision_weights[i] = None
    while None in alternative_decisions:
        del alternative_decisions[alternative_decisions.index(None)]
        del alternative_decision_weights[alternative_decision_weights.index(None)]
    e = []
    for i in alternative_decisions:  # 对于每条选择,先
        ei = 0
        for j in decisions:
            if j[0] != one_unit.id:
                if i == j[2]:
                    ei += one_unit.effector['advisors'][j[0]] + j[1]
            else:
                if i == j[2]:
                    ei += j[1]
        e.append(ei)
    # 此时拿到了所有建议以及决策以及权重
    result = []
    for i in range(len(alternative_decisions)):
        result.append(e[i] * alternative_decision_weights[i])
    return (
        alternative_decisions[result.index(max(result))], alternative_decision_weights[result.index(max(result))])


# 建议者类
class advisor:
    def __init__(self, xml_dom):
        '''
        构造函数
        :param xml_dom: 存储着建议者的xml的dom对象
        '''
        # 获取dom文件的根节点
        self.root = xml_dom.documentElement
        # 获取memberType标签
        membertype = self.root.getElementsByTagName('memberType')[0]
        # 初始化建议者的id，从memberType标签中的ID属性获得
        self.id = membertype.getAttribute('ID')
        # 初始化建议者的建议禀赋，从memberType标签中的endowment属性获得
        self.endowment = float(membertype.getAttribute('endowment'))
        # 获取preference标签
        pfrc = self.root.getElementsByTagName('preference')[0]
        # 初始化格局的路径（用于对比一致性）
        self.ptn = self.root.getElementsByTagName('pattern')[0].getAttribute('path')
        # 获取建议者在格局上的偏好
        self.preference = pfrc.getAttribute('value').split(',')
        # 获取unitList标签
        unit_List = self.root.getElementsByTagName('unitList')[0]
        # 获取所有unit标签
        us = self.root.getElementsByTagName('unit')
        # 用字典初始化一下与该建议者相连的units集合
        units = {}
        # 对于每个unit标签
        for i in us:
            # 以uID属性为key，strength属性为value
            a = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            # 存到units里面
            units.update(a)
        # 初始化建议者的unitList
        self.unitList = {"remain": unit_List.getAttribute('remaining'), "scale": int(unit_List.getAttribute('scale')),
                         "units": units}

    def return_suggestion(self, position, pattern):
        """
        计算当前位置的推荐动作
        :param position:
        :param pattern:
        :return:a tuple
        """
        if position in self.preference:
            # 如果unit当前的所在位置在本advisor的偏好里面，那么直接返回该position在偏好中的下一个位置即可
            return (position, self.preference[self.preference.index(position) + 1])
        else:  # 当position不在偏好路径里时,根据拓扑排序
            sp = pattern.topo_sort_sequence.index(position)  # START POINT
            for i in range(sp, len(pattern.topo_sort_sequence)):  # find the nearest point
                if pattern.topo_sort_sequence[i] in self.preference:  # 找到拓扑序列中第一个在偏好路径上的点
                    cp = pattern.get_best_way(pattern.topo_sort_sequence[sp], pattern.topo_sort_sequence[
                        i])  # the best way from now to first preference position
                    if cp == None:
                        continue
                    else:
                        return (cp[1][0], cp[1][1])
        pass


def return_suggestion(preference, position, pattern):
    '''
    计算当前位置的推荐动作
    :param preference: 偏好路径
    :param position: 当前位置
    :param pattern: 整个的格局
    :return: 一个动作二元组
    '''
    if position in preference:
        return (position, preference[preference.index(position) + 1])
    else:
        start_point_index = pattern.topo_sort_sequence.index(position)  # START POINT
        for i in range(start_point_index, len(pattern.topo_sort_sequence)):  # find the nearest point
            if pattern.topo_sort_sequence[i] in preference:  # 找到拓扑序列中第一个在偏好路径上的点
                # the best way from now to first preference position
                cp = get_best_way(pattern, pattern.topo_sort_sequence[start_point_index], pattern.topo_sort_sequence[i])
                if cp == None:
                    continue
                else:
                    return (cp[1][0], cp[1][1])


# 监控者类
class monitor:
    def __init__(self, xml_dom):
        '''
        构造函数
        :param xml_dom: 存储监控者的xml的dom对象
        '''
        # 获得dom对象的根节点
        self.root = xml_dom.documentElement
        # 获得memberType标签
        membertype = self.root.getElementsByTagName('memberType')[0]
        # 从memberType中的ID属性中获得id
        self.id = membertype.getAttribute('ID')
        # 获得监控禀赋
        self.endowment = float(membertype.getAttribute('endowment'))
        # 获得格局路径（用于对比一致性）
        self.ptn = self.root.getElementsByTagName('pattern')[0].getAttribute('path')
        # 获取monitoring标签
        rspsblty = self.root.getElementsByTagName('monitoring')[0]
        # 获取监控者的监控范围
        self.responsibility = rspsblty.getAttribute('value').split('|')
        # 对于每个监控范围，要将其格式转为tuple元组（存储时的格式就是元组）
        for i in range(len(self.responsibility)):
            if self.responsibility[i] != '':
                self.responsibility[i] = eval(self.responsibility[i])
        # 获得unitList标签
        unit_List = self.root.getElementsByTagName('unitList')[0]
        # 获得所有的unit标签
        us = self.root.getElementsByTagName('unit')
        # 用字典初始化一下与该监控者相连的units集合
        units = {}
        # 对于每个unit标签
        for i in us:
            # 以uID属性为key，strength属性为value
            a = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            # 存到units里面
            units.update(a)
        # 初始化监控者的unitList
        self.unitList = {"remain": float(unit_List.getAttribute('remaining')),
                         "scale": int(unit_List.getAttribute('scale')),
                         "units": units}


if __name__ == '__main__':
    unit = unit(xml_dom=read_xml(r"..\units\MyCrowd_Unit05.xml"))
    advisor = advisor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\advisors\\MyCrowd_advisor00.xml"))
    # monitor = monitor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\monitors\\MyCrowd_monitor01.xml"))
    ptn = pattern(xml_dom=read_xml(r'E:\code\PycharmProjects\simulation\patterns\pattern1.xml'))
    print(return_suggestion(advisor.preference, 'p2', pattern=ptn))
    # a = unit.overlook(ptn)
    # b = unit.make_decision(ptn)
    # unit.do_behavior(ptn,b)
    unit.reset_connection()
    input()
    pass
