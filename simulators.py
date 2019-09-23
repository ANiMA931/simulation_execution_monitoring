from math import pi, atan
from member import *
from tools import *
from random import shuffle
from numpy.random import rand
from xml.dom import minidom



class cE_simulator:
    def __init__(self, units_path, advisor_path, monitor_path, record_path):
        units_names = member_file_name(units_path)
        advisors_names = member_file_name(advisor_path)
        monitors_names = member_file_name(monitor_path)
        self.units = {}
        self.advisors = {}
        self.monitors = {}
        self.record_path = record_path
        self.success_rate_list = list()
        for i in units_names:
            u = unit(xml_dom=read_xml(units_path + '\\\\' + i))
            self.units.update({u.id: u})
        for i in advisors_names:
            a = advisor(xml_dom=read_xml(advisor_path + '\\\\' + i))
            self.advisors.update({a.id: a})
        for i in monitors_names:
            m = monitor(xml_dom=read_xml(monitor_path + '\\\\' + i))
            self.monitors.update({m.id: m})
        if self.check_pattern():
            self.ptn = pattern(read_xml(u.ptn))
        else:
            print('pattern path error, press any key to exit.')
            return

    def check_pattern(self):
        keys = list(self.units.keys())
        ptn_path = self.units[keys[0]].ptn
        for i in self.units.values():
            if ptn_path != i.ptn:
                return False
        for i in self.advisors.values():
            if ptn_path != i.ptn:
                return False
        for i in self.monitors.values():
            if ptn_path != i.ptn:
                return False
        return True

    def simulate(self,round):
        def all_check(self):
            for u in self.units.items():
                if u[1].status == 'active':
                    return True
            return False

        while all_check(self):  # 判断所有单元是否结束
            for u in self.units.items():
                if u[1].status == 'active':
                    dec_list = []
                    ex_m = float(0)  # 外部监督强度
                    """向它的advisor们寻求建议"""
                    for a in u[1].effector['advisors'].items():
                        dec_list.append((self.advisors[a[0]].id, self.advisors[a[0]].unitList['units'][u[1].id],
                                         self.advisors[a[0]].return_suggestion(u[1].now, self.ptn)))
                    """unit根据自己在格局上的位置用自己的方法make一个决策出来"""
                    dec_list.append((u[1].id, u[1].decider['selfConfidence'], u[1].make_decision(self.ptn)))
                    """从自己的决策+建议者们的建议挑一个要执行的方案"""
                    dec = u[1].select_decision(dec_list, self.ptn)
                    """挑出来之后，遍历这个执行方案是不是在某些监控者的范围内，累加它们的监控权重"""

                    for m in u[1].executor['monitors']:  # 此处的m是monitor的字典
                        if dec in self.monitors[m['mID']].responsibility:  # 当某个行为是被监控者监控的，那么就加上外部的监督强度
                            ex_m += self.monitors[m['mID']].unitList['units'][u[1].id]
                    """外部监控权重+自律水平对抗自身的自退化水平以及突变，通过代价计算将要执行的动作"""
                    tmp_b = []
                    for i in self.ptn.behaviors:
                        if dec[0] == i['before']:
                            tmp_b.append(i)
                    min_b = dec_b = {}
                    min_w_temp = inf
                    for i in tmp_b:  # 定位到weight最小与决定的behavior
                        if min_w_temp > i['weight']:
                            min_b = i
                            min_w_temp = i['weight']
                        if dec[0] == i['before'] and dec[1] == i['after']:
                            dec_b = i
                    del min_w_temp
                    r1 = (1 - (2 / pi) * atan(ex_m)) * dec_b['weight']
                    if u[1].executor['selfDiscipline'] >= u[1].executor['selfDegeneration']:
                        r0 = min_b['weight']
                    else:
                        r0 = (1 - (2 / pi) * atan(
                            u[1].executor['selfDegeneration'] - u[1].executor['selfDiscipline'])) * min_b['weight']
                    """依照成功率执行，执行成功就更新unit的now，不成功就不更新"""

                    if r1 < r0:
                        if rand() < u[1].executor['mutationRate']:
                            shuffle(tmp_b)
                            dec = (tmp_b[0]['before'], tmp_b[0]['after'])
                            result = u[1].do_behavior(self.ptn, dec)
                        else:
                            result = u[1].do_behavior(self.ptn, dec)
                    else:
                        if rand() < u[1].executor['mutationRate']:
                            shuffle(tmp_b)
                            dec = (tmp_b[0]['before'], tmp_b[0]['after'])
                            result = u[1].do_behavior(self.ptn, dec)
                        else:
                            result = u[1].do_behavior(self.ptn, (min_b['before'], min_b['after']))
                    """广播自己的执行内容给其他相连的"""
                    for c_u in u[1].parameter['c_units']:  # 此处的c_u是本unit连接的unit的id
                        self.units[c_u].get_para_message(u[1], result)
                    """此处可能会有一段根据获得信息更改自己与其他单位的连接权重的代码"""
                   # units[c_u].reset_connection()
                    u[1].self_check(self.ptn)

        self.make_round_record(round)
        for u in self.units.items():
            u[1].reset_connection()
            u[1].status='active'
            u[1].now='p24'
            u[1].past_way=[]

    def calc_success_rate(self):
        count = 0
        for u in self.units.items():
            if u[1].status == 'succeed':
                count += 1
        return count / len(self.units)

    def make_round_record(self, round):
        success_rate = self.calc_success_rate()
        dom = minidom.Document()
        self.success_rate_list.append(success_rate)
        root_node = dom.createElement('record')
        root_node.setAttribute('round', str(round))
        root_node.setAttribute('successRate', str(success_rate))
        dom.appendChild(root_node)
        for u in self.units.items():
            units_node = dom.createElement('unit')
            advisors_node = dom.createElement('advisors')
            monitors_node = dom.createElement('monitors')
            cunits_node = dom.createElement('cUnits')
            units_node.setAttribute('ID', u[1].id)
            units_node.setAttribute('Path', str(u[1].past_way))
            units_node.setAttribute('target', u[1].target)
            units_node.setAttribute('result', u[1].status)
            units_node.setAttribute('resource', str(u[1].init_resource))
            units_node.setAttribute('resourceRemain', str(u[1].resource))
            units_node.setAttribute('selfConfidence', str(u[1].decider['selfConfidence']))
            units_node.setAttribute('selfDegeneration', str(u[1].executor['selfDegeneration']))
            units_node.setAttribute('selfDiscipline', str(u[1].executor['selfDiscipline']))
            units_node.setAttribute('mutationRate', str(u[1].executor['mutationRate']))
            root_node.appendChild(units_node)

            advisors_node.setAttribute('endowment', str(u[1].effector['endowment']))
            advisors_node.setAttribute('remain', str(u[1].effector['remain']))
            advisors_node.setAttribute('scale', str(u[1].effector['scale']))
            for a in u[1].effector['advisors'].items():
                advisor_node = dom.createElement('advisor')
                advisor_node.setAttribute('aID', a[0])
                advisor_node.setAttribute('strength', str(a[1]))
                advisors_node.appendChild(advisor_node)

            monitors_node.setAttribute('scale', str(u[1].executor['scale']))
            for m in u[1].executor['monitors']:
                monitor_node = dom.createElement('monitor')
                monitor_node.setAttribute('mID', m['mID'])
                monitors_node.appendChild(monitor_node)

            cunits_node.setAttribute('endowment', str(u[1].parameter['endowment']))
            cunits_node.setAttribute('remain', str(u[1].parameter['remain']))
            cunits_node.setAttribute('scale', str(u[1].parameter['scale']))
            for c_u in u[1].parameter['c_units'].items():
                cunit_node = dom.createElement('cUnit')
                cunit_node.setAttribute('uID', c_u[0])
                cunit_node.setAttribute('strength', str(c_u[1]))
                cunits_node.appendChild(cunit_node)
            units_node.appendChild(advisors_node)
            units_node.appendChild(monitors_node)
            units_node.appendChild(cunits_node)

        write_xml(self.record_path + '\\\\' + 'cE_record_detail' + str(round).zfill(5) + '.xml', dom)
        return success_rate

    def make_simulate_result(self, generation):
        dom = minidom.Document()
        root_node = dom.createElement('result')
        root_node.setAttribute('generation', str(generation))
        dom.appendChild(root_node)
        for g in range(len(self.success_rate_list)):
            record_node = dom.createElement('record')
            record_node.setAttribute('round', str(g))
            record_node.setAttribute('successRate', str(self.success_rate_list[g]))
            root_node.appendChild(record_node)

        write_xml(self.record_path + '\\\\' + 'cE_record' + '.xml', dom)



if __name__ == '__main__':

    generation = 10
    units_path = 'E:\\code\\PycharmProjects\\simulation\\units'
    advisor_path = 'E:\\code\\PycharmProjects\\simulation\\advisors'
    monitor_path = 'E:\\code\\PycharmProjects\\simulation\\monitors'
    record_path = 'E:\\code\\PycharmProjects\\simulation\\record'
    cs= cE_simulator(units_path, advisor_path, monitor_path, record_path)
    for i in range(generation):
        cs.simulate(i)
    cs.make_simulate_result(generation)
