from my_tools import *
import pandas as pd
import numpy as np


# class BaseMember(object):
#     def __init__(self, ID, preference, endowment):
#         self.ID = ID
#         self.preference = preference
#         self.endowment = endowment
#
#
# class PrimitiveMember(BaseMember):
#     def __init__(self, ID, preference, endowment, effector, decider, executor, monitor, connector):
#         super().__init__(ID, preference, endowment)
#         self.effector = effector
#         self.decider = decider
#         self.executor = executor
#         self.monitor = monitor
#         self.connector = connector
#
#     def sdgafbasfg(self):
#         print()
#
#
# class CollectiveMember(BaseMember):
#     def __init__(self, ID, preference, endowment, decomposer, executor, converger):
#         super().__init__(ID, preference, endowment)
#         self.decomposer = decomposer
#         self.executor = executor
#         self.converger = converger
#
#
# class AdviserMember(BaseMember):
#     def __init__(self, ID, preference, endowment, adviser_round_method):
#         super().__init__(ID, preference, endowment)
#         self.adviser_round_method = adviser_round_method
#
#
# class MonitorMember(BaseMember):
#     def __init__(self, ID, preference, endowment, monitor_round_method):
#         super().__init__(ID, preference, endowment)
#         self.monitor_round_method = monitor_round_method


def member_read(xml_dom: xml.dom.minidom.Document):
    """
    成员读取，动态xml读取为dict
    :param xml_dom:xml的dom对象
    :return:四个可以保存为json的dict
    """
    affector_dict = dict()  # 保存影响器的dict

    def read_affector(xml_dom):
        """
        读取影响器
        :param xml_dom:
        :return:
        """
        affector_labels = xml_dom.getElementsByTagName('affectorInfo')
        affector_method_label = xml_dom.getElementsByTagName('affector')[0]
        for affector_label in affector_labels:
            label_id = affector_label.getAttribute('影响器ID')
            affector_dict.update({label_id: dict()})
            affector_dict[label_id].update({'method': affector_method_label.getAttribute('外部函数名')})
            label_attribute = affector_label.attributes
            for key, value in label_attribute.items():
                try:
                    affector_dict[label_id].update({key: eval(value)})
                except:
                    affector_dict[label_id].update({key: value})

    read_affector(xml_dom)
    decider_dict = dict()  # 保存决策器的dict

    def read_decider(xml_dom):
        """
        读取决策器
        :param xml_dom:
        :return:
        """
        decider_labels = xml_dom.getElementsByTagName('deciderInfo')
        decider_method_label = xml_dom.getElementsByTagName('decider')[0]
        for decider_label in decider_labels:
            label_id = decider_label.getAttribute('决策器ID')
            decider_dict.update({label_id: dict()})
            decider_dict[label_id].update({'method': decider_method_label.getAttribute('外部函数名')})
            label_attribute = decider_label.attributes
            for key, value in label_attribute.items():
                try:
                    decider_dict[label_id].update({key: eval(value)})
                except:
                    decider_dict[label_id].update({key: value})

    read_decider(xml_dom)
    executor_dict = dict()  # 保存执行器的dict

    def read_executor(xml_dom):
        """
        读取执行器
        :param xml_dom:
        :return:
        """
        executor_labels = xml_dom.getElementsByTagName('executorInfo')
        executor_method_label = xml_dom.getElementsByTagName('executor')[0]
        for executor_label in executor_labels:
            label_id = executor_label.getAttribute('执行器ID')
            executor_dict.update({label_id: dict()})
            executor_dict[label_id].update({'method': executor_method_label.getAttribute('外部函数名')})
            label_attribute = executor_label.attributes
            for key, value in label_attribute.items():
                try:
                    executor_dict[label_id].update({key: eval(value)})
                except:
                    executor_dict[label_id].update({key: value})

    read_executor(xml_dom)
    monitor_dict = dict()  # 保存监控器的dict

    def read_monitor(xml_dom):
        """
        读取监控器
        :param xml_dom:
        :return:
        """
        monitor_labels = xml_dom.getElementsByTagName('monitorInfo')
        monitor_method_label = xml_dom.getElementsByTagName('monitor')[0]
        for monitor_label in monitor_labels:
            label_id = monitor_label.getAttribute('监控器ID')
            monitor_dict.update({label_id: dict()})
            monitor_dict[label_id].update({'method': monitor_method_label.getAttribute('外部函数名')})
            label_attribute = monitor_label.attributes
            for key, value in label_attribute.items():
                try:
                    monitor_dict[label_id].update({key: eval(value)})
                except:
                    monitor_dict[label_id].update({key: value})

    read_monitor(xml_dom)
    connector_dict = dict()  # 保存连接器的dict

    def read_connector(xml_dom):
        """
        读取连接器
        :param xml_dom:
        :return:
        """
        connector_labels = xml_dom.getElementsByTagName('connectorInfo')
        connector_method_label = xml_dom.getElementsByTagName('connector')[0]
        for connector_label in connector_labels:
            label_id = connector_label.getAttribute('联接器ID')
            connector_dict.update({label_id: dict()})
            connector_dict[label_id].update({'method': connector_method_label.getAttribute('外部函数名')})
            label_attribute = connector_label.attributes
            for key, value in label_attribute.items():
                try:
                    connector_dict[label_id].update({key: eval(value)})
                except:
                    connector_dict[label_id].update({key: value})

    read_connector(xml_dom)
    primitives_dict = dict()  # 保存原子型成员的dict

    def read_primitive(xml_dom):
        """
        读取原子型成员
        :param xml_dom:
        :return:
        """
        primitives_labels = xml_dom.getElementsByTagName('primitiveInfo')
        for primitives_label in primitives_labels:
            label_id = primitives_label.getAttribute('原子型成员ID')
            primitives_dict.update({label_id: dict()})
            label_attribute = primitives_label.attributes
            for key, value in label_attribute.items():
                try:
                    primitives_dict[label_id].update({key: eval(value)})
                except:
                    primitives_dict[label_id].update({key: value})
            # 配置影响器
            primitives_dict[label_id]['影响器'] = affector_dict[primitives_dict[label_id]['影响器']]
            # 配置决策器
            primitives_dict[label_id]['决策器'] = decider_dict[primitives_dict[label_id]['决策器']]
            # 配置监控器
            primitives_dict[label_id]['监控器'] = monitor_dict[primitives_dict[label_id]['监控器']]
            # 配置执行器
            primitives_dict[label_id]['执行器'] = executor_dict[primitives_dict[label_id]['执行器']]
            # 配置连接器
            primitives_dict[label_id]['联接器'] = connector_dict[primitives_dict[label_id]['联接器']]

    advisers_dict = dict()  # 保存建议者成员的dict

    def read_advisers(xml_dom):
        """
        读取建议者
        :param xml_dom:
        :return:
        """
        adviserInfo_labels = xml_dom.getElementsByTagName('advisorInfo')
        for adviserInfo_label in adviserInfo_labels:
            label_id = adviserInfo_label.getAttribute('建议者ID')
            advisers_dict.update({label_id: dict()})
            label_attribute = adviserInfo_label.attributes
            for key, value in label_attribute.items():
                try:
                    advisers_dict[label_id].update({key: eval(value)})
                except:
                    advisers_dict[label_id].update({key: value})

    monitorMembers_dict = dict()  # 保存监控者成员的dict

    def read_monitorMembers(xml_dom):
        """
        读取监控者
        :param xml_dom:
        :return:
        """
        monitorMembers_labels = xml_dom.getElementsByTagName('monitorMemberInfo')
        for monitorMembers_label in monitorMembers_labels:
            label_id = monitorMembers_label.getAttribute('监控者ID')
            monitorMembers_dict.update({label_id: dict()})
            label_attribute = monitorMembers_label.attributes
            for key, value in label_attribute.items():
                try:
                    monitorMembers_dict[label_id].update({key: eval(value)})
                except:
                    monitorMembers_dict[label_id].update({key: value})

    # 分解器
    decomposer_dict = dict()

    def read_decomposer(xml_dom):
        """
        读取分解器
        :param xml_dom:
        :return:
        """
        decomposer_labels = xml_dom.getElementsByTagName('decomposerInfo')
        decomposer_method_label = xml_dom.getElementsByTagName('decomposer')[0]
        for decomposer_label in decomposer_labels:
            label_id = decomposer_label.getAttribute('分解器ID')
            decomposer_dict.update({label_id: dict()})
            decomposer_dict[label_id].update({'method': decomposer_method_label.getAttribute('外部函数名')})
            label_attribute = decomposer_label.attributes
            for key, value in label_attribute.items():
                try:
                    decomposer_dict[label_id].update({key: eval(value)})
                except:
                    decomposer_dict[label_id].update({key: value})

    read_decomposer(xml_dom)
    # 汇聚器
    converger_dict = dict()

    def read_converger(xml_dom):
        converger_labels = xml_dom.getElementsByTagName('convergerInfo')
        converger_method_label = xml_dom.getElementsByTagName('converger')[0]
        for converger_label in converger_labels:
            label_id = converger_label.getAttribute('汇聚器ID')
            converger_dict.update({label_id: dict()})
            converger_dict[label_id].update({'method': converger_method_label.getAttribute('外部函数名')})
            label_attribute = converger_label.attributes
            for key, value in label_attribute.items():
                try:
                    converger_dict[label_id].update({key: eval(value)})
                except:
                    converger_dict[label_id].update({key: value})

    read_converger(xml_dom)
    # 集合型决策器
    c_decider_dict = dict()

    def read_c_decider(xml_dom):
        c_decider_labels = xml_dom.getElementsByTagName('c_deciderInfo')
        c_decider_method_label = xml_dom.getElementsByTagName('c_decider')[0]
        for c_decider_label in c_decider_labels:
            label_id = c_decider_label.getAttribute('决策器ID')
            c_decider_dict.update({label_id: dict()})
            c_decider_dict[label_id].update({'method': c_decider_method_label.getAttribute('外部函数名')})
            label_attribute = c_decider_label.attributes
            for key, value in label_attribute.items():
                try:
                    c_decider_dict[label_id].update({key: eval(value)})
                except:
                    c_decider_dict[label_id].update({key: value})

    read_c_decider(xml_dom)
    # 集合型执行器
    c_executor_dict = dict()

    def read_c_executor(xml_dom):
        c_executor_labels = xml_dom.getElementsByTagName('c_executorInfo')
        c_executor_method_label = xml_dom.getElementsByTagName('c_executor')[0]
        for c_executor_label in c_executor_labels:
            label_id = c_executor_label.getAttribute('执行器ID')
            c_executor_dict.update({label_id: dict()})
            c_executor_dict[label_id].update({'method': c_executor_method_label.getAttribute('外部函数名')})
            label_attribute = c_executor_label.attributes
            for key, value in label_attribute.items():
                try:
                    c_executor_dict[label_id].update({key: eval(value)})
                except:
                    c_executor_dict[label_id].update({key: value})

    read_c_executor(xml_dom)

    # 集合型成员
    collective_dict = dict()  # 保存集合型成员的dict

    def read_collective(xml_dom):
        """
        读取集合型成员
        :param xml_dom:
        :return:
        """
        collective_labels = xml_dom.getElementsByTagName('collectiveInfo')
        for collective_label in collective_labels:
            label_id = collective_label.getAttribute('集合型成员ID')
            collective_dict.update({label_id: dict()})
            label_attribute = collective_label.attributes
            for key, value in label_attribute.items():
                try:
                    collective_dict[label_id].update({key: eval(value)})
                except:
                    collective_dict[label_id].update({key: value})
            # 配置影响器
            collective_dict[label_id]['影响器'] = affector_dict[collective_dict[label_id]['影响器']]
            # 配置分解器
            collective_dict[label_id]['分解器'] = decomposer_dict[collective_dict[label_id]['分解器']]
            # 配置汇聚器
            collective_dict[label_id]['汇聚器'] = converger_dict[collective_dict[label_id]['汇聚器']]
            # 配置决策器
            collective_dict[label_id]['决策器'] = c_decider_dict[collective_dict[label_id]['决策器']]
            # 配置执行器
            collective_dict[label_id]['执行器'] = c_executor_dict[collective_dict[label_id]['执行器']]
            # 配置监控器
            collective_dict[label_id]['监控器'] = monitor_dict[collective_dict[label_id]['监控器']]
            # 配置连接器
            collective_dict[label_id]['联接器'] = connector_dict[collective_dict[label_id]['联接器']]

    read_advisers(xml_dom)
    read_monitorMembers(xml_dom)
    read_primitive(xml_dom)
    read_collective(xml_dom)
    return primitives_dict, advisers_dict, monitorMembers_dict, collective_dict


def net_work_read(xml_dom: xml.dom.minidom.Document):
    """
    网络读取，静态读取为dataframe，返回6个dataframe网络
    :param xml_dom:xml的dom对象
    :return:六个网络，net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c
    """
    global net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c

    primitive_ids, adviser_ids, monitorMember_ids, collective_ids = [], [], [], []
    primitive_labels = xml_dom.getElementsByTagName('primitiveInfo')
    for one_primitive_label in primitive_labels:
        ID = one_primitive_label.getAttribute('原子型成员ID')
        primitive_ids.append(ID)
    adviser_labels = xml_dom.getElementsByTagName('advisorInfo')
    for one_adviser_label in adviser_labels:
        ID = one_adviser_label.getAttribute('建议者ID')
        adviser_ids.append(ID)
    monitorMember_labels = xml_dom.getElementsByTagName('monitorMemberInfo')
    for one_monitor_label in monitorMember_labels:
        ID = one_monitor_label.getAttribute('监控者ID')
        monitorMember_ids.append(ID)
    collective_labels = xml_dom.getElementsByTagName('collectiveInfo')
    for one_collective_label in collective_labels:
        ID = one_collective_label.getAttribute('集合型成员ID')
        collective_ids.append(ID)

    net_labels = xml_dom.getElementsByTagName('networkStructure')
    for one_net_label in net_labels:
        if one_net_label.getAttribute('type') == 'p2p':
            conn_labels = one_net_label.getElementsByTagName('connectInfo')
            tmp = np.zeros((len(primitive_ids), len(primitive_ids)), dtype=np.float)
            # tmp[:]=np.nan
            net_p2p = pd.DataFrame(tmp)
            net_p2p.index, net_p2p.columns = primitive_ids, primitive_ids
            for conn_label in conn_labels:
                _from, _to = conn_label.getAttribute('from'), conn_label.getAttribute('to'),
                _strength = eval(conn_label.getAttribute('strength'))
                net_p2p[_to][_from] = _strength

        elif one_net_label.getAttribute('type') == 'p2a':
            conn_labels = one_net_label.getElementsByTagName('connectInfo')
            tmp = np.zeros((len(primitive_ids), len(adviser_ids)), dtype=np.float)
            tmp[:] = np.nan
            net_p2a = pd.DataFrame(tmp)
            net_p2a.index, net_p2a.columns = primitive_ids, adviser_ids
            for conn_label in conn_labels:
                _from, _to = conn_label.getAttribute('from'), conn_label.getAttribute('to'),
                _strength = eval(conn_label.getAttribute('strength'))
                net_p2a[_to][_from] = _strength

        elif one_net_label.getAttribute('type') == 'p2m':
            conn_labels = one_net_label.getElementsByTagName('connectInfo')
            tmp = np.zeros((len(primitive_ids), len(monitorMember_ids)), dtype=np.float)
            tmp[:] = np.nan
            net_p2m = pd.DataFrame(tmp)
            net_p2m.index, net_p2m.columns = primitive_ids, monitorMember_ids
            for conn_label in conn_labels:
                _from, _to = conn_label.getAttribute('from'), conn_label.getAttribute('to'),
                _strength = eval(conn_label.getAttribute('strength'))
                net_p2m[_to][_from] = _strength

        elif one_net_label.getAttribute('type') == 'p2c':
            conn_labels = one_net_label.getElementsByTagName('connectInfo')
            tmp = np.zeros((len(primitive_ids), len(collective_ids)), dtype=np.float)
            tmp[:] = np.nan
            net_p2c = pd.DataFrame(tmp)
            net_p2c.index, net_p2c.columns = primitive_ids, collective_ids
            for conn_label in conn_labels:
                _from, _to = conn_label.getAttribute('from'), conn_label.getAttribute('to'),
                _strength = eval(conn_label.getAttribute('strength'))
                net_p2c[_to][_from] = _strength

        elif one_net_label.getAttribute('type') == 'c2m':
            conn_labels = one_net_label.getElementsByTagName('connectInfo')
            tmp = np.zeros((len(collective_ids), len(monitorMember_ids)), dtype=np.float)
            tmp[:] = np.nan
            net_c2m = pd.DataFrame(tmp)
            net_c2m.index, net_c2m.columns = collective_ids, monitorMember_ids
            for conn_label in conn_labels:
                _from, _to = conn_label.getAttribute('from'), conn_label.getAttribute('to'),
                _strength = eval(conn_label.getAttribute('strength'))
                net_c2m[_to][_from] = _strength

        elif one_net_label.getAttribute('type') == 'c2c':
            conn_labels = one_net_label.getElementsByTagName('connectInfo')
            tmp = np.zeros((len(collective_ids), len(collective_ids)), dtype=np.float)
            tmp[:] = np.nan
            net_c2c = pd.DataFrame(tmp)
            net_c2c.index, net_c2c.columns = collective_ids, collective_ids
            for conn_label in conn_labels:
                _from, _to = conn_label.getAttribute('from'), conn_label.getAttribute('to'),
                _strength = eval(conn_label.getAttribute('strength'))
                net_c2c[_to][_from] = _strength

    return net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c


if __name__ == '__main__':
    xml_dom = read_xml(r'F:\pythonCode\PycharmProjects\simulation_execution_monitoring\members\fpMemberXml_C.xml')
    primitives_dict, advisers_dict, monitorMembers_dict, collective_dict = member_read(xml_dom)
