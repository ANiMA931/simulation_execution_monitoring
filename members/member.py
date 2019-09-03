from tools import *
from patterns.pattern import pattern


class unit:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.target = self.root.getElementsByTagName('target')[0].getAttribute('pID')
        self.now = self.root.getElementsByTagName('now')[0].getAttribute('pID')
        self.resource = float(membertype.getAttribute('resource'))
        efctr = self.root.getElementsByTagName('effector')[0]
        advsrs = self.root.getElementsByTagName('advisor')
        advisors = {}
        for i in advsrs:
            a = {"aID": i.getAttribute('aID'), "strength": float(i.getAttribute('strength'))}
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
        cunts = self.root.getElementsByTagName('cUnit')
        c_units = {}
        for i in cunts:
            a = {i.getAttribute('uID'): float(i.getAttribute('strength'))}
            c_units.update(a)
        self.parameter = {"endowment": float(cprtr.getAttribute('endowment')),
                          "remain": float(cprtr.getAttribute('remain')),
                          "scale": int(cprtr.getAttribute('scale')), "c_units": c_units}

    def make_decision(self, pattern):
        pass

    def select_decision(self, decisions):
        pass

    def get_para_message(self):
        pass

    def reset_connection(self):
        pass


class advisor:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.endowment = float(membertype.getAttribute('endowment'))
        pfrc = self.root.getElementsByTagName('preference')[0]
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
        :return:
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
                        return (cp[1][0],cp[1][1])
        pass


class monitor:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.endowment = float(membertype.getAttribute('endowment'))
        rspsblty = self.root.getElementsByTagName('monitoring')[0]
        self.responsibility = rspsblty.getAttribute('value').split('|')
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
    unit = unit(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\units\\MyCrowd_Unit00.xml"))
    advisor = advisor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\advisors\\MyCrowd_advisor00.xml"))
    monitor = monitor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\monitors\\MyCrowd_monitor01.xml"))
    print(advisor.return_suggestion('p2', pattern=pattern(
        xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml")))
          )
