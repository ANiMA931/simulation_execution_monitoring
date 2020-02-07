from copy import deepcopy
from math import pi
from my_tools import *
from random import seed, shuffle, randrange, uniform


# 基础成员
class Member(object):
    def __init__(self, self_dict: dict):
        self.id = self_dict['id']  # 成员的id
        self.metaModel_id = self_dict['metaModel_id']  # 成员的元模型id


# 原子型成员
primitives = dict()
advisors = dict()
monitorMembers = dict()


class Primitive(Member):
    def __init__(self, self_dict: dict):
        super(Primitive, self).__init__(self_dict)
        self.msg_receive_endowment = int(float(self_dict['msg_receive_endowment']))  # 信息接收禀赋，依照条目数执行
        self.msg_receive_pool = []  # 信息接收池
        self.msg_storage_endowment = float(self_dict['msg_storage_endowment'])  # 信息存储禀赋，依照信息强度执行
        self.msg_storage_pool = []  # 信息存储池
        self.confidence = self_dict['confidence']  # 个人自信水平
        self.discipline = self_dict['discipline']  # 个人自律水平
        self.browse = int(float(self_dict['browse']))  # 个人浏览禀赋
        self.pattern = self_dict['pattern']  # 个人格局
        self.affector = self_dict['affector']  # 影响器
        self.the_advisors = list()
        self.decider = self_dict['decider']  # 决策器
        self.executor = self_dict['executor']  # 执行器
        self.monitor = self_dict['monitor']  # 监控器
        self.the_monitorMembers = list()
        self.connector = self_dict['connector']  # 连接器
        self.the_connectors = dict()  # 该primitive接收谁发送的消息
        self.msg_receive_pool.append((self.decider['message_vector'].strength, deepcopy(self.decider['message_vector']), 'self'))


# 建议者
class Advisor(Member):
    def __init__(self, self_dict: dict):
        super(Advisor, self).__init__(self_dict)
        self.sug_endowment = self_dict['sug_endowment']  # 建议禀赋
        self.sug_path = self_dict['sug_path']  # 建议路径
        self.the_conn_primitive = dict()


class MonitorMember(Member):
    def __init__(self, self_dict: dict):
        super(MonitorMember, self).__init__(self_dict)
        self.mon_endowment = float(self_dict['mon_endowment'])  # 监控禀赋
        self.mon_area = self_dict['mon_area']  # 监控领域
        self.mon_range = self_dict['mon_range']  # 监控领域角度范围 tuple
        self.the_conn_primitive = dict()


# 信息偏好基础类
class BaseMessage:
    def __init__(self, self_dict: dict):
        self.id = self_dict['id']  # 信息id
        self.area = self_dict['area']  # 信息领域
        self.strength = self_dict['strength']  # 信息强度


# 信息类
class Message(BaseMessage):
    def __init__(self, self_dict: dict):
        super(Message, self).__init__(self_dict)
        self.angle = self_dict['angle']
        self.z_angle=self_dict['z_angle']


# 偏好类，与信息类差别在于
class Preference(BaseMessage):
    def __init__(self, self_dict: dict):
        super(Preference, self).__init__(self_dict)
        self.range = self_dict['range']  # 信息角度范围 tuple


def format_xml_to_member(xml_dom):
    root = xml_dom.documentElement
    # 偏好整合
    preference_info_labels = root.getElementsByTagName('preferenceInfo')
    preferences = dict()
    for one_preference_label in preference_info_labels:
        start, end = one_preference_label.getAttribute('偏好方向').split('-')
        one_preference = {
            'id': one_preference_label.getAttribute('偏好ID'),
            'area': one_preference_label.getAttribute('所属领域ID'),
            'strength': float(one_preference_label.getAttribute('偏好大小')),
            'range': (pi * float(start) / 180, pi * float(end) / 180),
        }
        preferences.update({one_preference_label.getAttribute('偏好ID'): Preference(one_preference)})
    # 信息整合
    message_info_labels = root.getElementsByTagName('messageInfo')
    messages = dict()
    for one_message_label in message_info_labels:
        one_message = {
            'id': one_message_label.getAttribute('信息ID'),
            'area': one_message_label.getAttribute('所属领域ID'),
            'strength': float(one_message_label.getAttribute('信息大小')),
            'angle': pi * float(one_message_label.getAttribute('信息方向')) / 180,
            'z_angle': pi* float(one_message_label.getAttribute('信息相关度')),
        }
        messages.update({one_message_label.getAttribute('信息ID'): Message(one_message)})
    # 影响器整合
    affector_info_labels = root.getElementsByTagName('affectorInfo')
    affectors = dict()
    for one_affector_label in affector_info_labels:
        one_affector = {
            'id': one_affector_label.getAttribute('影响器ID'),
            'conn_upper': int(one_affector_label.getAttribute('连接成员数量')),
            'average_strength': float(one_affector_label.getAttribute('平均影响强度'))
        }
        affectors.update({one_affector_label.getAttribute('影响器ID'): one_affector})

    # 决策器整合
    deciderInfo_labels = root.getElementsByTagName('deciderInfo')
    deciders = dict()
    for one_decider_label in deciderInfo_labels:
        one_decider = {
            'id': one_decider_label.getAttribute('决策器ID'),
            # 'forward_threshold': one_decider_label.getAttribute('转发阈值'),
            # 'mass_threshold': one_decider_label.getAttribute('群发阈值'),
            # 'struct_change_threshold': one_decider_label.getAttribute('改变连接结构阈值'),
            # 'weak_strength_threshold': one_decider_label.getAttribute('减弱信息强度阈值'),
            'forward_threshold': 0.25,
            'mass_threshold': 0.00000005,
            'struct_change_threshold': -0.75,
            'weak_strength_threshold': -0.0000025,
            'preference_vector': preferences[one_decider_label.getAttribute('偏好矢量')],
            'message_vector': messages[one_decider_label.getAttribute('信息矢量')]
        }
        deciders.update({one_decider_label.getAttribute('决策器ID'): one_decider})

    # 执行器整合
    executor_info_labels = root.getElementsByTagName('executorInfo')
    executors = dict()
    for one_executor_label in executor_info_labels:
        one_executor = {
            'id': one_executor_label.getAttribute('执行器ID'),
            'mutation': float(one_executor_label.getAttribute('突变率')),
            'spreading_threshold': float(one_executor_label.getAttribute('传播阈值')),
            'preference_behavior': one_executor_label.getAttribute('偏好行为'),
            'message_vector': messages[one_executor_label.getAttribute('信息矢量')],
        }
        executors.update({one_executor_label.getAttribute('执行器ID'): one_executor})
    # 监控器整合
    monitorsInfo_labels = root.getElementsByTagName('monitorInfo')
    monitors = dict()
    for one_monitor_label in monitorsInfo_labels:
        one_monitor = {
            'id': one_monitor_label.getAttribute('监控器ID'),
            'mon_strength': float(one_monitor_label.getAttribute('监控强度')),
        }
        monitors.update({one_monitor_label.getAttribute('监控器ID'): one_monitor})
    # 连接器整合
    connectorsInfo_labels = root.getElementsByTagName('connectorInfo')
    connectors = dict()
    for one_connector_label in connectorsInfo_labels:
        one_connector = {
            'id': one_connector_label.getAttribute('联接器ID'),
            'conn_number': int(one_connector_label.getAttribute('连接成员数量')),
            'average_conn_strength': float(one_connector_label.getAttribute('平均连接强度')),
        }
        connectors.update({one_connector_label.getAttribute('联接器ID'): one_connector})
    # 原子形成员整合
    primitiveInfo_labels = root.getElementsByTagName('primitiveInfo')
    for one_primitive_label in primitiveInfo_labels:
        primitive_dict = dict()
        primitive_dict.update({
            'id': one_primitive_label.getAttribute('原子型成员ID'),
            'metaModel_id': one_primitive_label.getAttribute('成员模型'),
            'msg_receive_endowment': int(float(one_primitive_label.getAttribute('信息接收禀赋'))),
            'msg_storage_endowment': int(float(one_primitive_label.getAttribute('信息存储禀赋'))),
            'confidence': float(one_primitive_label.getAttribute('个人自信水平')),
            'discipline': float(one_primitive_label.getAttribute('自律水平')),
            'browse': float(one_primitive_label.getAttribute('浏览禀赋')),
            'pattern': one_primitive_label.getAttribute('格局'),
            'affector': affectors[one_primitive_label.getAttribute('影响器')],
            'decider': deciders[one_primitive_label.getAttribute('决策器')],
            'executor': executors[one_primitive_label.getAttribute('执行器')],
            'monitor': monitors[one_primitive_label.getAttribute('监控器')],
            'connector': connectors[one_primitive_label.getAttribute('联接器')],
        })
        primitives.update({
            one_primitive_label.getAttribute('原子型成员ID'): Primitive(primitive_dict),
        })
    # 建议者整合
    advisor_info_labels = root.getElementsByTagName('advisorInfo')
    for one_advisor_label in advisor_info_labels:
        advisor_dict = dict()
        advisor_dict.update({
            'id': one_advisor_label.getAttribute('建议者ID'),
            'metaModel_id': one_advisor_label.getAttribute('成员模型'),
            'sug_endowment': float(one_advisor_label.getAttribute('建议禀赋')),
            'sug_path': one_advisor_label.getAttribute('建议路径'),
        })
        advisors.update({
            one_advisor_label.getAttribute('建议者ID'): Advisor(advisor_dict),
        })
    # 监控者整合
    monitorMemberInfo_labels = root.getElementsByTagName('monitorMemberInfo')
    for one_monitorMember_label in monitorMemberInfo_labels:
        monitorMember_dict = dict()
        start, end = one_monitorMember_label.getAttribute('监控范围').split('-')
        monitorMember_dict.update({
            'id': one_monitorMember_label.getAttribute('监控者ID'),
            'metaModel_id': one_monitorMember_label.getAttribute('成员模型'),
            'mon_endowment': one_monitorMember_label.getAttribute('监控禀赋'),
            'mon_area': one_monitorMember_label.getAttribute('监控领域'),
            'mon_range': (pi * float(start) / 180, pi * float(end) / 180),
        })
        monitorMembers.update({
            one_monitorMember_label.getAttribute('监控者ID'): MonitorMember(monitorMember_dict),
        })


def connect_all_member():
    """
    连接已有成员
    :return:
    """
    seed(1)  # 随机结果可复现
    # promitive相连，该连接为双向非对称网络
    for p in primitives.keys():
        pid_list = list(primitives.keys())
        aid_list = list(advisors.keys())
        mid_list = list(monitorMembers.keys())
        shuffle(pid_list)
        shuffle(aid_list)
        shuffle(mid_list)
        real_link_number = randrange(primitives[p].connector['conn_number'])
        if p in pid_list[:real_link_number]:
            pid_list.remove(p)
            print('remove self connect.')  # 测试发生移除自我连接的次数
        for one_pid in pid_list[:real_link_number]:  # 添加连接信息
            # 这个primitive接收哪些primitive的信息，同时给哪些primitive发信息，这个信息带有权重
            primitives[p].the_connectors.update({one_pid: primitives[p].connector['average_conn_strength']})
            primitives[one_pid].the_connectors.update({p: primitives[one_pid].connector['average_conn_strength']})
        # primitive与advisor相连，
        # 注意事项:拥有primitive角色的advisor不与自己连接
        real_link_number = randrange(len(aid_list))
        if p in aid_list:
            aid_list.remove(p)
            print('remove self advice.')  # 测试发生移除自我建议的次数
        for one_aid in aid_list[:real_link_number]:
            # 确定该primitive接收谁的建议
            primitives[p].the_advisors.append(one_aid)
            # 由于不确定本建议者会给多少个primitive提建议，所以建议强度初始值设置为禀赋
            advisors[one_aid].the_conn_primitive.update({p: advisors[one_aid].sug_endowment})
        # 建议关系生成结束后要重置建议强度
        for a in advisors.keys():
            for cp in advisors[a].the_conn_primitive.keys():
                advisors[a].the_conn_primitive[cp] = advisors[a].sug_endowment / len(advisors[a].the_conn_primitive)
        # primitive与monitor相连，
        # 注意事项:拥有primitive角色的monitor不与自己连接
        real_link_number = randrange(len(mid_list))
        if p in mid_list:
            mid_list.remove(p)
            print('remove self monitoring.')
        for one_mid in mid_list[:real_link_number]:
            primitives[p].the_monitorMembers.append(one_mid)
            monitorMembers[one_mid].the_conn_primitive.update({p: monitorMembers[one_mid].mon_endowment})
        # 监控关系生成结束后要重置监控强度
        for m in monitorMembers.keys():
            for cp in monitorMembers[m].the_conn_primitive.keys():
                monitorMembers[m].the_conn_primitive[cp] = monitorMembers[m].mon_endowment / len(
                    monitorMembers[m].the_conn_primitive)


if __name__ == '__main__':
    format_xml_to_member(read_xml(r'fP_Members.xml'))
    connect_all_member()
    print()
