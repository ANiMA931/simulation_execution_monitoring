# simulators.py

# 本文件写各种仿真对应的仿真类

import sys
import threading
import numpy as np
import pandas as pd
from time import time, sleep
from math import pi, atan  # 仿真需要的反函数与圆周率
from members.cE_member import *  # 众进化仿真成员
from my_tools import *  # 一些必要的工具
from random import shuffle  # 必要的随机排列函数
from numpy.random import rand  # 随机数函数
from xml.dom import minidom  # 生成xml文件时的工具


class UnitThread(threading.Thread):
    def __init__(self, the_unit, extypal_advisors, extypal_monitors):
        super(UnitThread, self).__init__()
        self.unit = the_unit
        self.extypal_advisors = extypal_advisors
        self.extypal_momitors = extypal_monitors
        self.result_sequence = []

    def run(self):
        print('start')
        while self.unit.status == 'active':
            res = re_one_unit_run_on_pattern(self.unit, self.extypal_advisors, self.extypal_momitors)
            self.result_sequence.append(res)
        print('end')
        global thread_result_pool
        threading_lock.acquire()
        thread_result_pool.append((self.unit.id, self.result_sequence))
        threading_lock.release()


def read_members(member_file_names, members_path):
    units = {}
    advisors = {}
    monitors = {}

    member_count = {'unit': 0, 'advisor': 0, 'monitor': 0}
    for names in member_file_names:
        xml_dom = read_xml(members_path + '\\\\' + names)
        root = xml_dom.documentElement
        try:
            member_type = root.getElementsByTagName('memberType')[0]
        except IndexError:
            input(
                'File: ' + members_path + '\\\\' + names + ' error. Without label memberType. input any key to exit.')
            sys.exit()
        member_role = member_type.getAttribute('memberRole')
        if member_role == 'unit':
            temporary_unit = unit(xml_dom)
            units.update({temporary_unit.id: temporary_unit})
            member_count['unit'] += 1

        elif member_role == 'advisor':
            temporary_advisor = advisor(xml_dom)
            advisors.update({temporary_advisor.id: temporary_advisor})
            member_count['advisor'] += 1

        elif member_role == 'monitor':
            temporary_monitor = monitor(xml_dom)
            monitors.update({temporary_monitor.id: temporary_monitor})
            member_count['monitor'] += 1
        else:
            print('wrong member role, path: {}, please chaeck it file:\n.'.format(members_path))
            input('press any kay to exit')
            sys.exit()
    check_result = check_pattern(units, advisors, monitors)
    if check_result is True:
        the_ptn = pattern(read_xml(units[list(units.keys())[0]].ptn))
    else:
        input('member ' + str(
            check_result) + '\'s pattern path is different from first member, please check it. Press any key to exit.')
        sys.exit()
    return units, advisors, monitors, member_count, the_ptn


def re_one_unit_run_on_pattern(one_unit, ectypal_advisors, ectypal_monitors):
    """
    线程函数，一个unit在格局上从头走到尾的具体流程
    :param one_unit: 当前的unit
    :param ectypal_advisors: 与当前unit连接的advisor们的副本
    :param ectypal_monitors: 与当前unit连接的monitor们连接的副本
    :return:
    """
    sleep(0.1)
    if one_unit.status == 'active':
        # 声明一个保存建议的表
        dec_list = []
        # 声明一个保存外部监督强度的变量
        sum_of_external_monitoring = float(0)
        for adv in ectypal_advisors.keys():
            global advisors_units_relationship, the_pattern
            dec_list.append((adv, advisors_units_relationship[adv][one_unit.id],
                             return_suggestion(ectypal_advisors[adv], one_unit.now, the_pattern)))

        dec_list.append((one_unit.id, one_unit.decider['selfConfidence'], make_decision(one_unit, the_pattern)))
        selected_decision = select_decision(one_unit, dec_list, the_pattern)

        for mon in ectypal_monitors.keys():
            if selected_decision[0] in ectypal_monitors[mon]:
                global units_monitors_relationship
                sum_of_external_monitoring += units_monitors_relationship[one_unit.id][mon]
        alternative_behaviors = []
        for b in the_pattern.behaviors:
            if one_unit.now == b['before'] and one_unit.resource >= b['weight']:
                alternative_behaviors.append(b)
        min_behavior = {}
        temporary_min_behavior_weight = inf
        for i in alternative_behaviors:  # 定位到weight最小的behavior和
            if temporary_min_behavior_weight > i['weight']:
                min_behavior = i
                temporary_min_behavior_weight = i['weight']

        r1 = (1 - (2 / pi) * atan(sum_of_external_monitoring)) * selected_decision[1]
        if one_unit.executor['selfDiscipline'] >= one_unit.executor['selfDegeneration']:
            r0 = min_behavior['weight']
        else:
            r0 = (1 - (2 / pi) * atan(one_unit.executor['selfDegeneration'] - one_unit.executor['selfDiscipline'])) * \
                 min_behavior['weight']
        if r1 <= r0:
            # 如果发生了突变，那么就在当前境地下随便选一个behavior执行
            if rand() < one_unit.executor['mutationRate']:
                shuffle(alternative_behaviors)
                final_decision = (alternative_behaviors[0]['before'], alternative_behaviors[0]['after'])
                result = do_behavior(one_unit, the_pattern, final_decision)
            else:
                result = do_behavior(one_unit, the_pattern, (min_behavior['before'], min_behavior['after']))
        # 如果当前境地weight最小的behavior吸引力更大
        else:
            # 如果发生了突变，那么就在当前境地下随便选一个behavior执行
            if rand() < one_unit.executor['mutationRate']:
                shuffle(alternative_behaviors)
                final_decision = (alternative_behaviors[0]['before'], alternative_behaviors[0]['after'])
                result = do_behavior(one_unit, the_pattern, final_decision)
            # 没发生突变就正常执行被选择出来的behavior
            else:
                result = do_behavior(one_unit, the_pattern, selected_decision[0])
        one_unit.self_check(the_pattern)
        print(one_unit.id, result)
        return result


def check_pattern(units, advisors, monitors):
    keys = list(units.keys())
    ptn_path = units[keys[0]].ptn
    for i in units.values():
        if ptn_path != i.ptn:
            return i.id
    for i in advisors.values():
        if ptn_path != i.ptn:
            return i.id
    for i in monitors.values():
        if ptn_path != i.ptn:
            return i.id
    return True


def all_end(units):
    """
    检查所有unit是否都走到了终点，False为都走到了终点，True为还有unit没到终点
    :param units: 仿真器本体
    :return: 是否所有人走到了终点
    """
    # 对于所有unit
    for u in units.keys():
        # 有一个unit的状态是active就继续
        if units[u].status == 'active':
            return True
    # 全都不是active表明所有人都走到了终点
    return False


def re_simulate(units, advisors, monitors, now_round, success_rate_list, record_path):
    """

    :param units:
    :param advisors:
    :param monitors:
    :param now_round:
    :param success_rate_list:
    :param record_path:
    :return:
    """
    thread_list = []
    for one_unit in units.keys():
        ectypal_advisors = {}
        ectypal_monitors = {}
        for adv in units[one_unit].effector['advisors'].keys():
            ectypal_advisors.update({advisors[adv].id: advisors[adv].preference})
        for mon in units[one_unit].executor['monitors']:
            ectypal_monitors.update({monitors[mon['mID']].id: monitors[mon['mID']].responsibility})
        unit_thread = UnitThread(units[one_unit], ectypal_advisors.copy(), ectypal_monitors.copy())
        thread_list.append(unit_thread)
        unit_thread.start()

    for t in thread_list:
        t.join()

    global thread_result_pool
    # 保存一下，然后清空
    result_list = thread_result_pool.copy()
    # 生成本轮次的仿真记录
    thread_result_pool.clear()
    # make_round_record(units, now_round, success_rate_list, record_path)
    # 重设连接关系此段内容也要改为线程
    for one_unit in units.keys():
        units[one_unit].reset_connection()
    # 重新初始化所有成员的状态准备下一轮的仿真
    for one_unit in units.keys():
        units[one_unit].status = 'active'
        units[one_unit].now = the_pattern.init_position
        units[one_unit].past_way.clear()
        units[one_unit].resource = units[one_unit].init_resource
        units[one_unit].action_sequence.clear()



def calc_success_rate(units):
    """
    计算本次迭代的成功率
    :param units: 所有的units
    :return: 本次迭代的成功率
    """
    # 初始化记录有多少unit到达了自己想要的position
    count = 0
    # 对于每个unit，如果它的最终状态是succeed则+1
    for u in units.keys():
        if units[u].status == 'succeed':
            count += 1
    # 返回比率
    return count / len(units)


def make_round_record(units, the_round, success_rate_list, record_path):
    """
    生成某一迭代的记录
    :param units:
    :param the_round:
    :param success_rate_list:
    :param record_path:
    :return:
    """
    # 计算成功率
    success_rate = calc_success_rate(units)
    # 将算得的成功率存到列表里
    success_rate_list.append(success_rate)

    # 获得生成xml的工具对象实例
    dom = minidom.Document()
    # 设置标签，标签名为record
    root_node = dom.createElement('record')
    # 设置record标签的属性round为当前迭代数
    root_node.setAttribute('round', str(the_round))
    # 设置record标签的属性successRate为本轮迭代的成功率
    root_node.setAttribute('successRate', str(success_rate))
    # 将record标签设置为工具对象的Child，则表明record标签为xml文件的根标签
    dom.appendChild(root_node)

    # 然后记录本轮迭代所有unit的状态，对于每个unit
    for one_unit in units.keys():
        # 设置标签unit
        units_node = dom.createElement('unit')
        # 设置标签advisors
        advisors_node = dom.createElement('advisors')
        # 设置标签monitors
        monitors_node = dom.createElement('monitors')
        # 设置标签cUnit（connected_unit)
        cunits_node = dom.createElement('cUnits')
        # 给units_node设置ID属性，值为该unit的id
        units_node.setAttribute('ID', units[one_unit].id)
        # 给units_node设置action_sequence属性，值为该unit在本次迭代中做过的所有的动作
        units_node.setAttribute('actionSequence', str(units[one_unit].action_sequence))
        # 给unit_node设置Path属性，值为该unit经过的路径
        units_node.setAttribute('Path', str(units[one_unit].past_way))
        # 给unit_node设置target属性，值为该unit的目标
        units_node.setAttribute('target', units[one_unit].target)
        # 给unit_node设置result属性，值为该unit的状态
        units_node.setAttribute('result', units[one_unit].status)
        # 给unit_node设置resource属性，值为该unit的初始资源
        units_node.setAttribute('resource', str(units[one_unit].init_resource))
        # 给unit_node设置resourceRemain属性，值为该unit的剩余资源
        units_node.setAttribute('resourceRemain', str(units[one_unit].resource))
        # 给unit_node设置cost属性，值为该unit在此次仿真中消耗的资源
        units_node.setAttribute('resourceCost', str(units[one_unit].init_resource - units[one_unit].resource))
        # 给unit_node设置selfConfidence属性，值为该unit的自信水平
        units_node.setAttribute('selfConfidence', str(units[one_unit].decider['selfConfidence']))
        # 给unit_node设置selfDegeneration属性，值为该unit的自退化水平
        units_node.setAttribute('selfDegeneration', str(units[one_unit].executor['selfDegeneration']))
        # 给unit_node设置selfDiscipline属性，值为该unit的自律水平
        units_node.setAttribute('selfDiscipline', str(units[one_unit].executor['selfDiscipline']))
        # 给unit_node设置mutationRate属性，值为该unit的突变率
        units_node.setAttribute('mutationRate', str(units[one_unit].executor['mutationRate']))
        # 将units_node设置为root_node的子标签
        root_node.appendChild(units_node)

        # 给advisors_node设置属性endowment，值为该unit对建议接受的禀赋
        advisors_node.setAttribute('endowment', str(units[one_unit].effector['endowment']))
        # 给advisors_node设置属性remain，值为该unit禀赋剩余
        advisors_node.setAttribute('remain', str(units[one_unit].effector['remain']))
        # 给advisors_node设置属性scale，值为该unit连接建议者的个数
        advisors_node.setAttribute('scale', str(units[one_unit].effector['scale']))

        # 对于每个与该unit连接的建议者
        for temp_advisor in units[one_unit].effector['advisors'].items():
            # 初始化advisor标签
            advisor_node = dom.createElement('advisor')
            # 给advisor标签设置属性aID，值为该建议者的id
            advisor_node.setAttribute('aID', temp_advisor[0])
            # 给advisor标签设置属性strength，值为该该unit对advisor接受影响的强度
            advisor_node.setAttribute('strength', str(temp_advisor[1]))
            # 将advisor标签设置为advisors标签的子标签
            advisors_node.appendChild(advisor_node)
        # 给monitors_node设置属性scale，值为该unit连接的监控者的个数
        monitors_node.setAttribute('scale', str(units[one_unit].executor['scale']))
        # 对于每一个与unit相连的监控者
        for temp_monitor in units[one_unit].executor['monitors']:
            # 初始化monitor标签
            monitor_node = dom.createElement('monitor')
            # 给monitor设置属性mID，值为当前监控者的id
            monitor_node.setAttribute('mID', temp_monitor['mID'])
            # 将monitor标签设置为monitors标签的子标签
            monitors_node.appendChild(monitor_node)
        # 给cUnits标签设置属性endowment，值为本unit的连接禀赋
        cunits_node.setAttribute('endowment', str(units[one_unit].parameter['endowment']))
        # 给cUnits标签设置属性remain，值为本unit的连接禀赋剩余
        cunits_node.setAttribute('remain', str(units[one_unit].parameter['remain']))
        # 给cUnits标签设置属性scale，值为本unit连接的其他unit的个数
        cunits_node.setAttribute('scale', str(units[one_unit].parameter['scale']))
        # 对于每个被本unit连接的unit
        for temp_conn_unit in units[one_unit].parameter['conn_units'].items():
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
    write_xml(record_path + '\\\\' + 'cE_record_detail' + str(the_round).zfill(5) + '.xml', dom)
    # 返回本次迭代仿真的成功率
    return success_rate


def make_simulate_result(self, generation):
    """
    生成此次仿真总体的仿真记录
    :param self:
    :param generation: 迭代数
    :return:
    """
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


def main():
    """
    表面上这个函数不需要任何参数，但是在实际应用中是需要的
    :needed args:
        :generation:仿真总迭代数
        :record_path:仿真记录目标目录
        :member_path:仿真所需成员目录
        :version:仿真的版本
        :ex_id:仿真的id
    :return: no return
    """
    generation = 5
    record_path = 'record'
    members_path = 'member_xml'
    version = '0.0'
    ex_id = 'cE_ex01'

    global units_relationship, units_advisors_relationship
    global advisors_units_relationship, units_monitors_relationship, the_pattern
    member_file_names = member_file_name(members_path)
    units, advisors, monitors, member_count, the_pattern = read_members(member_file_names, members_path)

    # units之间相连的权重矩阵，该矩阵非对称
    units_relationship = np.zeros((len(units), len(units)), dtype=np.float)
    units_relationship[:] = np.nan
    units_relationship = pd.DataFrame(units_relationship)
    units_relationship.index = list(units.keys())
    units_relationship.columns = list(units.keys())

    for one_unit in units.keys():
        for another_unit in units[one_unit].parameter['conn_units'].keys():
            units_relationship[one_unit][another_unit] = units[one_unit].parameter['conn_units'][another_unit]

    # units到advisor的权重矩阵，不对称，
    units_advisors_relationship = np.zeros((len(advisors), len(units)), dtype=np.float)
    units_advisors_relationship[:] = np.nan
    units_advisors_relationship = pd.DataFrame(units_advisors_relationship)
    units_advisors_relationship.index = list(advisors.keys())
    units_advisors_relationship.columns = list(units.keys())
    for one_unit in units.keys():
        for one_advisor in units[one_unit].effector['advisors'].keys():
            units_advisors_relationship[one_unit][one_advisor] = units[one_unit].effector['advisors'][one_advisor]

    # advisor到unit的权重矩阵，不对称
    advisors_units_relationship = np.zeros((len(units), len(advisors)), dtype=np.float)
    advisors_units_relationship[:] = np.nan
    advisors_units_relationship = pd.DataFrame(advisors_units_relationship)
    advisors_units_relationship.index = list(units.keys())
    advisors_units_relationship.columns = list(advisors.keys())
    for one_advisor in advisors.keys():
        for one_unit in advisors[one_advisor].unitList['units'].keys():
            advisors_units_relationship[one_advisor][one_unit] = advisors[one_advisor].unitList['units'][one_unit]

    # units到monitors的权重矩阵，不对称
    units_monitors_relationship = np.zeros((len(monitors), len(units)), dtype=np.float)
    units_monitors_relationship[:] = np.nan
    units_monitors_relationship = pd.DataFrame(units_monitors_relationship)
    units_monitors_relationship.index = list(monitors.keys())
    units_monitors_relationship.columns = list(units.keys())
    for one_unit in units.keys():
        for one_monitor in units[one_unit].executor['monitors']:
            units_monitors_relationship[one_unit][one_monitor['mID']] = monitors[one_monitor['mID']].unitList['units'][
                one_unit]

    start_time = time()
    success_rate_list = []
    for g in range(generation):
        re_simulate(units, advisors, monitors, g, success_rate_list, record_path)
    b = time() - start_time
    print('\n', '本次仿真共计{}代，共花费时间{}秒'.format(generation, b))
    # cs.make_simulate_result(generation)


if __name__ == '__main__':
    global units_relationship, units_advisors_relationship, thread_result_pool
    global advisors_units_relationship, units_monitors_relationship, the_pattern
    thread_result_pool = []
    threading_lock = threading.Lock()
    main()
