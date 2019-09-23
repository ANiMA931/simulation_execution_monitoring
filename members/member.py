from tools import *
from numpy.random import rand
from math import inf
from patterns.pattern import pattern


class unit:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.target = self.root.getElementsByTagName('target')[0].getAttribute('pID')
        self.now = self.root.getElementsByTagName('now')[0].getAttribute('pID')
        self.status = 'active'
        self.resource = float(membertype.getAttribute('resource'))
        self.init_resource = float(membertype.getAttribute('resource'))
        self.past_way = [self.now]  # 已经走过的路
        self.ptn = self.root.getElementsByTagName('pattern')[0].getAttribute('path')
        efctr = self.root.getElementsByTagName('effector')[0]
        advsrs = self.root.getElementsByTagName('advisor')
        advisors = {}
        for i in advsrs:
            b = {i.getAttribute('aID'): float(i.getAttribute('strength'))}
            advisors.update(b)
        self.effector = {"endowment": float(efctr.getAttribute('endowment')),
                         "remain": float(efctr.getAttribute('remain')),
                         "scale": int(efctr.getAttribute('scale')), "advisors": advisors}
        dsdr = self.root.getElementsByTagName('decider')[0]
        self.decider = {"depth": int(dsdr.getAttribute('depth')),
                        "selfConfidence": float(dsdr.getAttribute('selfConfidence')),
                        "strategy": dsdr.getAttribute('strategy')}
        exctr = self.root.getElementsByTagName('executor')[0]
        mntrs = self.root.getElementsByTagName('monitor')
        monitors = []
        for i in mntrs:
            a = {"mID": i.getAttribute('mID')}
            monitors.append(a)
        self.executor = {"mutationRate": float(exctr.getAttribute('mutationRate')),
                         "selfDegeneration": float(exctr.getAttribute('selfDegeneration')),
                         "selfDiscipline": float(exctr.getAttribute('selfDiscipline')),
                         "scale": int(exctr.getAttribute('scale')), "monitors": monitors}
        cprtr = self.root.getElementsByTagName('parameter')[0]
        c_unts = self.root.getElementsByTagName('cUnit')
        c_units = {}
        for i in c_unts:
            a = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            c_units.update(a)
        self.parameter = {"endowment": float(cprtr.getAttribute('endowment')),
                          "remain": float(cprtr.getAttribute('remain')),
                          "scale": int(cprtr.getAttribute('scale')), "c_units": c_units}

    def make_decision(self, pattern):
        """
        成员自己本身根据自己所在的位置做决策
        :param pattern:
        :return:
        """
        over_list = self.overlook(pattern)  # 先眺望自己能到什么地方
        for i in over_list:
            if self.target in over_list[i]:  # 已经眺望到了自己的目标
                c, path = pattern.get_best_way(self.now, self.target)  # 能眺望到自己的目标就可以用最短路径算法了
                return (path[0], path[1])
            else:  # 没有眺望到自己的目标
                mc = inf
                mp = []
                mx = max(over_list.keys())
                while not over_list[mx]:
                    mx -= 1
                else:
                    for j in over_list[mx]:  # 最远的position们
                        cp = pattern.get_best_way(self.now, j)
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
        over_list = {}
        for i in range(1, self.decider['depth'] + 1):
            over_list.update({i: []})
        for i in pattern.topo_sort_sequence:
            if pattern.topo_sort_sequence.index(self.now) < pattern.topo_sort_sequence.index(i):
                a = pattern.points_distance(self.now, i)
                if a is not None and a[0] <= self.decider['depth']:
                    over_list[a[0]].append(i)
        return over_list

    def self_check(self, pattern):
        if self.now == self.target:
            self.status = 'succeed'
        elif self.now in pattern.ending_positions and self.now != self.target:
            self.status = 'wrong'
        elif self.now not in pattern.ending_positions and self.is_impasse(pattern):  # 当前所在位置，所剩资源无法进行任何动作
            self.status = 'died'
        else:
            return

    def is_impasse(self, pattern):
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
        :return:一个二元组
        """
        a_d = []
        weights = []
        for i in decisions:  # 去重
            if i[2] not in a_d and i[2] is not None:
                a_d.append(i[2])
                for j in pattern.behaviors:
                    for k in pattern.positions:
                        if i[2][0] == j['before'] and i[2][1] == j['after'] and i[2][1] == k['pID']:
                            weights.append(k['weight'] - j['weight'])
        for i in range(len(a_d)):  # 把资源无法满足的选项给删掉
            if weights[i] > self.resource:
                a_d[i] = weights[i] = None
        while None in a_d:
            del a_d[a_d.index(None)]
            del weights[weights.index(None)]
        e = []
        for i in a_d:  # 对于每条选择,先
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
        for i in range(len(a_d)):
            result.append(e[i] * weights[i])
        return a_d[result.index(max(result))]

    def do_behavior(self, pattern, behavior):
        """
        执行动作，如果成功则更改自己的now，扣除动作的weight之后并获得动作结果对应的position的weight
        如果失败，则不更改自己的now，并扣除动作的weight，没有任何获得

        :param pattern:
        :param behavior:
        :return:
        """
        for i in pattern.behaviors:  # 此处的i是字典
            if ((i['before'], i['after']) == behavior):  # 定位到了对应的behavior
                r = rand()
                if r < float(i['success_rate']):
                    self.now = i['after']
                    self.resource -= i['weight']
                    self.past_way.append(i['after'])
                    for j in pattern.positions:
                        if j['pID'] == i['after']:
                            self.resource += j['weight']  # 在position上得到的权重被视为能够加进unit的resource里面
                            return ('success', behavior)
                else:
                    self.resource -= i['weight']
                    return ('fail', behavior)

    pass

    def get_para_message(self, res_unit, result):
        '''log.append(
            self.id + " get a message from " + res_unit.id + ". " + res_unit.id + " do a behavior from " + result[1][
                0] + " to " + result[1][1] + ". " + res_unit.id + " " + result[0])'''
        print(self.id + " get a message from " + res_unit.id + ". " + res_unit.id + " do a behavior from " + result[1][
                0] + " to " + result[1][1] + ". " + res_unit.id + " " + result[0])
        pass

    def reset_connection(self):
        length = len(self.effector['advisors']) + 1
        upper = self.effector['endowment']
        r, s = shatter_number(upper, length)
        itemm = 0
        for a in self.effector['advisors'].items():
            self.effector['advisors'][a[0]] = r[itemm]
            itemm += 1
        self.effector['remain'] = r[itemm]

    def re_init_unit(self):
        pass


class advisor:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.endowment = float(membertype.getAttribute('endowment'))
        pfrc = self.root.getElementsByTagName('preference')[0]
        self.ptn = self.root.getElementsByTagName('pattern')[0].getAttribute('path')
        self.preference = pfrc.getAttribute('value').split(',')
        unitList = self.root.getElementsByTagName('unitList')[0]
        us = self.root.getElementsByTagName('unit')
        units = {}
        for i in us:
            a = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            units.update(a)
        self.unitList = {"remain": unitList.getAttribute('remaining'), "scale": int(unitList.getAttribute('scale')),
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


class monitor:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.endowment = float(membertype.getAttribute('endowment'))
        self.ptn = self.root.getElementsByTagName('pattern')[0].getAttribute('path')
        rspsblty = self.root.getElementsByTagName('monitoring')[0]
        self.responsibility = rspsblty.getAttribute('value').split('|')
        for i in range(len(self.responsibility)):
            self.responsibility[i] = eval(self.responsibility[i])
        unitList = self.root.getElementsByTagName('unitList')[0]
        us = self.root.getElementsByTagName('unit')
        units = {}
        for i in us:
            a = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            units.update(a)
        self.unitList = {"remain": float(unitList.getAttribute('remaining')),
                         "scale": int(unitList.getAttribute('scale')),
                         "units": units}


if __name__ == '__main__':
    unit = unit(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\units\\MyCrowd_Unit05.xml"))
    # advisor = advisor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\advisors\\MyCrowd_advisor00.xml"))
    # monitor = monitor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\monitors\\MyCrowd_monitor01.xml"))
    ptn = pattern(xml_dom=read_xml(unit.ptn))
    # print(advisor.return_suggestion('p2', pattern=ptn))
    # a = unit.overlook(ptn)
    # b = unit.make_decision(ptn)
    # unit.do_behavior(ptn,b)
    unit.reset_connection()
    pass
