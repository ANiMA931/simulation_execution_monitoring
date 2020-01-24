# simulators.py
'''
本文件写各种仿真对应的仿真类
'''
import sys
import threading
from math import pi, atan  # 仿真需要的反函数与圆周率
from members.cE_member import *  # 众进化仿真成员
from my_tools import *  # 一些必要的工具
from random import shuffle  # 必要的随机排列函数
from numpy.random import rand  # 随机数函数
from xml.dom import minidom  # 生成xml文件时的工具



# 用于存储或读取仿真运行时成员之间的各种信息
class Observer:
    def __init__(self, unit_ids, advisor_ids, monitor_ids):
        '''
        警告信息尚不明确，交流信息内容明确，数据结构不明确，服务信息不明确
        '''
        self.warning_message = None
        self.communication_message = dict()
        for u in unit_ids:
            self.communication_message.update({u: []})
        for a in advisor_ids:
            self.communication_message.update({a: []})
        for m in monitor_ids:
            self.communication_message.update({m: []})
        self.service_message = None

    def simulation_message_engage(self):
        '''
        获得消息
        :return:
        '''
        pass

    def send_message(self):
        '''
        发送消息
        :return:
        '''
        pass

    def get_new_round(self):
        '''
        获得最新回合
        :return:
        '''
        pass

    def store_new_communication(self, new_round_message):
        key = list(new_round_message.keys())
        for k in key:
            self.communication_message[k].append(new_round_message[k])
        pass


def one_unit_run_on_pattern(cE_simulator, one_unit):
    if one_unit[1].status == 'active':
        # 声明一个保存建议的表
        dec_list = []
        # 声明 一个保存外部监督强度的变量
        sum_of_external_monitoring = float(0)
        # 向one_unit的advisor们寻求建议
        for a in one_unit[1].effector['cE_advisors'].items():
            # 建议的结构是一个tuple三元组，第一个是建议者的id，第二个是建议者对该unit的建议强度，第三个是建议
            dec_list.append(
                (cE_simulator.advisors[a[0]].id, cE_simulator.advisors[a[0]].unitList['cE_units'][one_unit[1].id],
                 cE_simulator.advisors[a[0]].return_suggestion(one_unit[1].now, cE_simulator.ptn)))
        # 然后unit根据自己在格局上的位置用自己的方法make一个决策出来
        dec_list.append(
            (one_unit[1].id, one_unit[1].decider['selfConfidence'], one_unit[1].make_decision(cE_simulator.ptn)))
        # 从自己的决策与建议者们的建议挑一个要执行的方案
        selected_decision = one_unit[1].select_decision(dec_list, cE_simulator.ptn)
        # 挑出来之后，遍历这个执行方案是不是在与该unit连接的监控者的监控范围内
        for m in one_unit[1].executor['cE_monitors']:  # 此处的m是monitor的字典
            # 当要执行的方案动作是被监控者m监控的，那么就累加它的外部的监督强度
            if selected_decision[0] in cE_simulator.monitors[m['mID']].responsibility:
                sum_of_external_monitoring += cE_simulator.monitors[m['mID']].unitList['cE_units'][one_unit[1].id]
        # 外部监控权重+自律水平对抗自身的自退化水平以及突变，通过代价计算将要执行的动作
        # 声明一个临时存储当前能有的所有behavior集合
        tmp_b = []
        for i in cE_simulator.ptn.behaviors:
            if one_unit[1].now == i['before'] and one_unit[1].resource >= i['weight']:
                tmp_b.append(i)
        min_b = {}
        min_w_temp = inf
        for i in tmp_b:  # 定位到weight最小的behavior和
            if min_w_temp > i['weight']:
                min_b = i
                min_w_temp = i['weight']
        del min_w_temp

        # r0与r1是当前能够选择的weight最小的behavior与自己决定的behavior对unit的吸引力，吸引力大的将会作为决定behavior

        r1 = (1 - (2 / pi) * atan(sum_of_external_monitoring)) * selected_decision[1]
        if one_unit[1].executor['selfDiscipline'] >= one_unit[1].executor['selfDegeneration']:
            r0 = min_b['weight']
        else:
            r0 = (1 - (2 / pi) * atan(
                one_unit[1].executor['selfDegeneration'] - one_unit[1].executor['selfDiscipline'])) * min_b[
                     'weight']
        # 如果自己决定的behavior的吸引力更大
        if r1 <= r0:
            # 如果发生了突变，那么就在当前境地下随便选一个behavior执行
            if rand() < one_unit[1].executor['mutationRate']:
                shuffle(tmp_b)
                final_decision = (tmp_b[0]['before'], tmp_b[0]['after'])
                result = one_unit[1].do_behavior(cE_simulator.ptn, final_decision)
            else:
                result = one_unit[1].do_behavior(cE_simulator.ptn, (min_b['before'], min_b['after']))
        # 如果当前境地weight最小的behavior吸引力更大
        else:
            # 如果发生了突变，那么就在当前境地下随便选一个behavior执行
            if rand() < one_unit[1].executor['mutationRate']:
                shuffle(tmp_b)
                final_decision = (tmp_b[0]['before'], tmp_b[0]['after'])
                result = one_unit[1].do_behavior(cE_simulator.ptn, final_decision)
            # 没发生突变就正常执行被选择出来的behavior
            else:
                result = one_unit[1].do_behavior(cE_simulator.ptn, selected_decision[0])
        # 广播自己的执行内容给其他与自身相连的unit
        for c_u in one_unit[1].parameter['conn_units']:  # 此处的c_u是本unit连接的unit的id
            cE_simulator.observer.store_new_communication(
                cE_simulator.units[c_u].get_para_message(one_unit[1], result, round))
        # 此处会有一段根据获得信息更改自己与其他单位的连接权重的代码

        # cE_units[c_u].reset_connection()

        # 执行结束之后检查当前unit的状态
        one_unit[1].self_check(cE_simulator.ptn)
    pass


def simulate(cE_simulator, round):
    '''
    仿真器仿真函数
    :param round:本次仿真是第几代仿真
    :return: no return
    '''

    def all_check(cE_simulator):
        '''
        检查所有unit是否都走到了终点，False为都走到了终点，True为还有unit没到终点
        :param cE_simulator: 仿真器本体
        :return: 是否所有人走到了终点
        '''
        # 对于所有unit
        for u in cE_simulator.units.items():
            # 有一个unit的状态是active就继续
            if u[1].status == 'active':
                return True
        # 全都不是active表明所有人都走到了终点
        return False

    while all_check(cE_simulator):  # 当还有单元没有结束的时候。
        # 对于仿真中的每一个unit
        # 做成成员函数
        thread_list = []
        for one_unit in cE_simulator.units.items():
            # 并行函数
            t=threading.Thread(target=one_unit_run_on_pattern,args=(cE_simulator, one_unit))
            t.start()
            thread_list.append(t)
            #print(thread_list)
            # 如果该unit的状态是active，那么

    # 跳出while循环说明所有的unit已经不能再执行，记录本迭代仿真的内容
    cE_simulator.make_round_record(round)
    # 重置所有参与仿真的unit，重设它们的连接关系，状态，当前位置与已走过的路径,为可能有的下一轮仿真准备
    for one_unit in cE_simulator.units.items():
        one_unit[1].reset_connection()
    for one_unit in cE_simulator.units.items():
        one_unit[1].status = 'active'
        one_unit[1].now = cE_simulator.ptn.init_position
        one_unit[1].past_way = []
        one_unit[1].resource = one_unit[1].init_resource
        one_unit[1].action_sequence.clear()


# 众进化仿真的仿真器
class cE_simulator:
    def __init__(self, record_path, member_path, version, ce_exID):
        '''
        众进化仿真的仿真器需要四种路径参数
        :param record_path: 仿真记录路径
        :param member_path: 成员路径
        '''
        # 读取成员路径成员的文件名字并保存为list
        members_names = member_file_name(member_path)
        # 初始化三种成员的群体，以字典形式存储，key是成员的id，value是成员对象
        self.version = version
        self.ID = ce_exID
        self.units = {}
        self.advisors = {}
        self.monitors = {}
        # 初始化仿真记录保存路径
        self.record_path = record_path
        # 记录每一代的成功率
        self.success_rate_list = list()  # 在仿真迭代比较小的时候可以使用，但是大了话可能就不能这么用了
        # 根据文件名列表，来依次初始化各个成员，并存进字典里面去
        self.member_count = {'unit': 0, 'advisor': 0, 'monitor': 0}
        for i in members_names:
            self.read_members(member_path + '\\\\' + i)

        # 检查pattern的一致性
        if self.check_pattern():
            self.ptn = pattern(read_xml(self.units[list(self.units.keys())[0]].ptn))
        else:
            input('pattern path error, press any key to exit.')
            sys.exit()

        self.observer = Observer(list(self.units.keys()),list(self.advisors.keys()),list(self.monitors.keys()))

    def read_members(self, member_path):
        '''
        通过路径读取成员
        :param member_path: 成员路径
        :return: 成员实体与字典各个成员有多少个
        '''
        xml_dom = read_xml(member_path)
        root = xml_dom.documentElement
        member_type = None
        member_role = None
        try:
            member_type = root.getElementsByTagName('memberType')[0]

        except:
            input('File: ' + member_path + ' error.' + ' Without label memberType. input any key to exit.')
            sys.exit()
        try:
            member_role = member_type.getAttribute('memberRole')
        except:
            input(
                'File: {} error. Label memberType don\'t have attribute \'\'memberRole\'\'. input any key to exit.'.format(
                    member_path))
            sys.exit()
        if member_role == 'unit':
            temporary_unit = unit(xml_dom)
            self.units.update({temporary_unit.id: temporary_unit})
            self.member_count['unit'] += 1

        elif member_role == 'advisor':
            temporary_advisor = advisor(xml_dom)
            self.advisors.update({temporary_advisor.id: temporary_advisor})
            self.member_count['advisor'] += 1

        elif member_role == 'monitor':
            temporary_monitor = monitor(xml_dom)
            self.monitors.update({temporary_monitor.id: temporary_monitor})
            self.member_count['monitor'] += 1
        else:
            print('wrong member role, path: {}, please chaeck it file:\n.'.format(member_path))
            input('press any kay to exit')
            sys.exit()

    def check_pattern(self):
        '''
        检测pattern，若所有成员的pattern都相同，则通过，有一个不同的就不通过，适用于本仿真
        :return: #是否通过，True or False
        '''
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

    def calc_success_rate(self):
        '''
        计算成功率，计算本次迭代的成功率
        :return: 本次迭代成功率
        '''
        # 初始化记录有多少unit到达了自己想要的position
        count = 0
        # 对于每个unit，如果它的最终状态是succeed则+1
        for u in self.units.items():
            if u[1].status == 'succeed':
                count += 1
        # 返回比率
        return count / len(self.units)

    def make_round_record(self, round):
        '''
        生成某一迭代的记录
        :param round: 某迭代数
        :return: no return
        '''
        # 计算成功率
        success_rate = self.calc_success_rate()
        # 将算得的成功率存到列表里
        self.success_rate_list.append(success_rate)

        # 获得生成xml的工具对象实例
        dom = minidom.Document()
        # 设置标签，标签名为record
        root_node = dom.createElement('record')
        # 设置record标签的属性round为当前迭代数
        root_node.setAttribute('round', str(round))
        # 设置record标签的属性successRate为本轮迭代的成功率
        root_node.setAttribute('successRate', str(success_rate))
        # 将record标签设置为工具对象的Child，则表明record标签为xml文件的根标签
        dom.appendChild(root_node)

        # 然后记录本轮迭代所有unit的状态，对于每个unit
        for u in self.units.items():
            # 设置标签unit
            units_node = dom.createElement('unit')
            # 设置标签advisors
            advisors_node = dom.createElement('cE_advisors')
            # 设置标签monitors
            monitors_node = dom.createElement('cE_monitors')
            # 设置标签cUnit（connected_unit)
            cunits_node = dom.createElement('cUnits')
            # 给units_node设置ID属性，值为该unit的id
            units_node.setAttribute('ID', u[1].id)
            # 给units_node设置action_sequence属性，值为该unit在本次迭代中做过的所有的动作
            units_node.setAttribute('actionSequence', str(u[1].action_sequence))
            # 给unit_node设置Path属性，值为该unit经过的路径
            units_node.setAttribute('Path', str(u[1].past_way))
            # 给unit_node设置target属性，值为该unit的目标
            units_node.setAttribute('target', u[1].target)
            # 给unit_node设置result属性，值为该unit的状态
            units_node.setAttribute('result', u[1].status)
            # 给unit_node设置resource属性，值为该unit的初始资源
            units_node.setAttribute('resource', str(u[1].init_resource))
            # 给unit_node设置resourceRemain属性，值为该unit的剩余资源
            units_node.setAttribute('resourceRemain', str(u[1].resource))
            # 给unit_node设置cost属性，值为该unit在此次仿真中消耗的资源
            units_node.setAttribute('resourceCost', str(u[1].init_resource - u[1].resource))
            # 给unit_node设置selfConfidence属性，值为该unit的自信水平
            units_node.setAttribute('selfConfidence', str(u[1].decider['selfConfidence']))
            # 给unit_node设置selfDegeneration属性，值为该unit的自退化水平
            units_node.setAttribute('selfDegeneration', str(u[1].executor['selfDegeneration']))
            # 给unit_node设置selfDiscipline属性，值为该unit的自律水平
            units_node.setAttribute('selfDiscipline', str(u[1].executor['selfDiscipline']))
            # 给unit_node设置mutationRate属性，值为该unit的突变率
            units_node.setAttribute('mutationRate', str(u[1].executor['mutationRate']))
            # 将units_node设置为root_node的子标签
            root_node.appendChild(units_node)

            # 给advisors_node设置属性endowment，值为该unit对建议接受的禀赋
            advisors_node.setAttribute('endowment', str(u[1].effector['endowment']))
            # 给advisors_node设置属性remain，值为该unit禀赋剩余
            advisors_node.setAttribute('remain', str(u[1].effector['remain']))
            # 给advisors_node设置属性scale，值为该unit连接建议者的个数
            advisors_node.setAttribute('scale', str(u[1].effector['scale']))

            # 对于每个与该unit连接的建议者
            for temp_advisor in u[1].effector['cE_advisors'].items():
                # 初始化advisor标签
                advisor_node = dom.createElement('advisor')
                # 给advisor标签设置属性aID，值为该建议者的id
                advisor_node.setAttribute('aID', temp_advisor[0])
                # 给advisor标签设置属性strength，值为该该unit对advisor接受影响的强度
                advisor_node.setAttribute('strength', str(temp_advisor[1]))
                # 将advisor标签设置为advisors标签的子标签
                advisors_node.appendChild(advisor_node)
            # 给monitors_node设置属性scale，值为该unit连接的监控者的个数
            monitors_node.setAttribute('scale', str(u[1].executor['scale']))
            # 对于每一个与unit相连的监控者
            for temp_monitor in u[1].executor['cE_monitors']:
                # 初始化monitor标签
                monitor_node = dom.createElement('monitor')
                # 给monitor设置属性mID，值为当前监控者的id
                monitor_node.setAttribute('mID', temp_monitor['mID'])
                # 将monitor标签设置为monitors标签的子标签
                monitors_node.appendChild(monitor_node)
            # 给cUnits标签设置属性endowment，值为本unit的连接禀赋
            cunits_node.setAttribute('endowment', str(u[1].parameter['endowment']))
            # 给cUnits标签设置属性remain，值为本unit的连接禀赋剩余
            cunits_node.setAttribute('remain', str(u[1].parameter['remain']))
            # 给cUnits标签设置属性scale，值为本unit连接的其他unit的个数
            cunits_node.setAttribute('scale', str(u[1].parameter['scale']))
            # 对于每个被本unit连接的unit
            for temp_conn_unit in u[1].parameter['conn_units'].items():
                # 初始化标签cUnit
                cunit_node = dom.createElement('connUnit')
                # 给cUnit标签设置属性uID，值为与本unit连接的当前unit的id
                cunit_node.setAttribute('uID', temp_conn_unit[0])
                # 给cUnit标签设置属性strength，值为本unit对当前unit连接的权重
                cunit_node.setAttribute('strength', str(temp_conn_unit[1]))
                # 将cUnit标签设置为cUnits标签的子标签
                cunits_node.appendChild(cunit_node)
            # 将advisors标签设置为unit标签的子标签
            units_node.appendChild(advisors_node)
            # 将monitors标签设置为unit标签的子标签
            units_node.appendChild(monitors_node)
            # 将cUnits标签设置为unit标签的子标签
            units_node.appendChild(cunits_node)
        # 存储设置好的xml文件
        write_xml(self.record_path + '\\\\' + 'cE_record_detail' + str(round).zfill(5) + '.xml', dom)
        # 返回本次迭代仿真的成功率
        return success_rate

    def make_simulate_result(self, generation):
        '''
        生成此次仿真总体的仿真记录
        :param generation: 迭代数
        :return: no return
        '''
        # 初始化dom对象
        dom = minidom.Document()
        # 设置标签result
        root_node = dom.createElement('result')
        # 给result标签设置属性ID，值为仿真执行ID
        root_node.setAttribute('ID', self.ID)
        # 给result标签设置属性version，值为版本号
        root_node.setAttribute('version', self.version)
        # 给result标签设置属性generation，值为迭代数
        root_node.setAttribute('generation', str(generation))
        # 将result标签设置为根标签
        dom.appendChild(root_node)
        # 对于每一轮迭代
        for g in range(len(self.success_rate_list)):
            # 初始化record标签
            record_node = dom.createElement('record')
            # 给record标签设置round属性，值为当前迭代数
            record_node.setAttribute('round', str(g))
            # 给record标签设置successRate属性，值为当前迭代的成功率
            record_node.setAttribute('successRate', str(self.success_rate_list[g]))
            # 将record标签设为result标签的子标签
            root_node.appendChild(record_node)
        # 存储xml文件
        write_xml(self.record_path + '\\\\' + 'cE_record' + '.xml', dom)


if __name__ == '__main__':

    generation = 100
    '''
    # #不再需要三种成员的路径了，一个member_path足够
    # units_path = 'cE_units'
    # advisor_path = 'cE_advisors'
    # monitor_path = 'cE_monitors'
    '''
    record_path = 'record'
    member_path = 'cE_member_xml'
    version = '0.0'
    ex_id = 'cE_ex01'

    member_file_names = member_file_name(member_path)
    from time import time

    cs = cE_simulator(record_path=record_path, member_path=member_path, version=version, ce_exID=ex_id)

    for i in member_file_names:
        cs.read_members(member_path + '\\\\' + i)
    a = time()
    for g in range(generation):
        simulate(cs, g)
    b = time() - a
    print('\n', '本次仿真共计{}代，共花费时间{}秒'.format(generation, b))
    cs.make_simulate_result(generation)
