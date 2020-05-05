from copy import deepcopy
from math import pi
from my_tools import read_xml, random
from random import seed, shuffle, randrange, uniform


# 基础成员
class Member(object):
    def __init__(self, self_dict: dict):
        self.id = self_dict['id']  # 成员的id
        self.metaModel_id = self_dict['metaModel_id']  # 成员的元模型id


# 原子型成员字典
primitives = dict()
# 建议者单元字典
advisors = dict()
# 监控者单元字典
monitorMembers = dict()
# 集合型成员字典
collectives = dict()
# 信息字典
messages = dict()
# 信息分组字典
message_group = dict()
# 领域集合
area_list = list()
# group
group_N = int()


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
        self.reduce_g_round = randrange(100)
        self.msg_receive_pool.append(
            [self.decider['message_vector'].strength, deepcopy(self.decider['message_vector']), 'self'])


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


class Collective(Member):
    def __init__(self, self_dict: dict):
        super(Collective, self).__init__(self_dict)
        self.converger = self_dict['converger']['way']
        self.decomposer = self_dict['decomposer']
        self.executor = self_dict['executor']
        self.connector = self_dict['connector']
        self.conn_primitive = dict()
        self.monitorMembers = list()
        self.mission_msg_pool = list()


# 信息偏好基础类
class BaseMessage(object):
    def __init__(self, self_dict: dict):
        self.id = self_dict['id']  # 信息id
        self.area = self_dict['area']  # 信息领域
        self.strength = self_dict['strength']  # 信息强度


# 信息类
class Message(BaseMessage):
    def __init__(self, self_dict: dict):
        super(Message, self).__init__(self_dict)
        self.angle = self_dict['angle']
        self.z_angle = self_dict['z_angle']


# 偏好类，与信息类差别在于
class Preference(BaseMessage):
    def __init__(self, self_dict: dict):
        super(Preference, self).__init__(self_dict)
        self.range = self_dict['range']  # 信息角度范围 tuple


def preference_format(root) -> dict:
    # 偏好整合
    preference_info_labels = root.getElementsByTagName('preferenceInfo')
    the_preferences = dict()
    for one_preference_label in preference_info_labels:
        start, end = one_preference_label.getAttribute('偏好方向').split('-')
        one_preference = {
            'id': one_preference_label.getAttribute('偏好ID'),
            'area': one_preference_label.getAttribute('所属领域ID'),
            'strength': float(one_preference_label.getAttribute('偏好大小')),
            'range': (pi * float(start) / 180, pi * float(end) / 180),
        }
        the_preferences.update({one_preference_label.getAttribute('偏好ID'): Preference(one_preference)})
    return the_preferences


def message_format(root):
    message_info_labels = root.getElementsByTagName('messageInfo')
    for one_message_label in message_info_labels:
        one_message = {
            'id': one_message_label.getAttribute('信息ID'),
            'area': one_message_label.getAttribute('所属领域ID'),
            'strength': float(one_message_label.getAttribute('信息大小')),
            'angle': pi * float(one_message_label.getAttribute('信息方向')) / 180,
            'z_angle': pi * float(one_message_label.getAttribute('信息相关度')),
        }
        messages.update({one_message_label.getAttribute('信息ID'): Message(one_message)})


def primitive_format(root):
    preferences = preference_format(root)
    # 信息整合
    message_format(root)
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
        # 选择偏好
        preference_pool = list()
        t_pref_id_list = list(preferences.keys())
        shuffle(t_pref_id_list)
        for one_preference_id in t_pref_id_list[:randrange(1, len(root.getElementsByTagName('areaInfo'))//2)]:
            preference_pool.append(preferences[one_preference_id])
        one_decider = {
            'id': one_decider_label.getAttribute('决策器ID'),
            # 'forward_threshold': one_decider_label.getAttribute('转发阈值'),
            # 'mass_threshold': one_decider_label.getAttribute('群发阈值'),
            # 'struct_change_threshold': one_decider_label.getAttribute('改变连接结构阈值'),
            # 'weak_strength_threshold': one_decider_label.getAttribute('减弱信息强度阈值'),
            'forward_threshold': 0.75,
            'mass_threshold': 0.55,
            'struct_change_threshold': -0.55,
            'weak_strength_threshold': -0.25,
            'preference_vector': preference_pool,
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
        primitives.update({primitive_dict['id']: Primitive(primitive_dict), })


def collective_format(root):
    # 分解器整合
    area_info_labels = root.getElementsByTagName('areaInfo')
    global message_group
    group_N = len(area_info_labels)
    for one_area_label in area_info_labels:
        area_list.append(one_area_label.getAttribute('领域ID'))
    for i in range(group_N):
        message_group.update({i: list()})
    for msg_id in messages.keys():
        for j in message_group.keys():
            if messages[msg_id].area == area_list[j]:
                message_group[j].append(msg_id)

    decomposerInfo_labels = root.getElementsByTagName('decomposerInfo')
    decomposers = dict()
    for one_decomposer_label in decomposerInfo_labels:
        one_decomposer = {
            'id': one_decomposer_label.getAttribute('分解器ID'),
            'group': randrange(group_N),
            'msg_expectation': one_decomposer_label.getAttribute('期望信息强度'),
            'spreading_threshold': one_decomposer_label.getAttribute('传播阈值'),
        }
        decomposers.update({one_decomposer['id']: one_decomposer})
    # 执行器整合
    c_executorInfo_labels = root.getElementsByTagName('c_executorInfo')
    c_executors = dict()
    for one_c_executor_label in c_executorInfo_labels:
        one_c_executor = {
            'id': one_c_executor_label.getAttribute('执行器ID'),
            'transmit_frequency': one_c_executor_label.getAttribute('传播频率'),
        }
        c_executors.update({one_c_executor['id']: one_c_executor})
    # 汇聚器整合
    convergerInfo_labels = root.getElementsByTagName('convergerInfo')
    convergers = dict()
    for one_converger_label in convergerInfo_labels:
        one_converger = {
            'id': one_converger_label.getAttribute('汇聚器ID'),
            'way': one_converger_label.getAttribute('汇聚方式')
        }
        convergers.update({one_converger['id']: one_converger})
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
    collectiveInfo_labels = root.getElementsByTagName('collectiveInfo')
    for one_collective_label in collectiveInfo_labels:
        one_collective_dict = {
            'id': one_collective_label.getAttribute('集合型成员ID'),
            'metaModel_id': one_collective_label.getAttribute('成员模型'),
            'converger': convergers[one_collective_label.getAttribute('汇聚器')],
            'executor': c_executors[one_collective_label.getAttribute('执行器')],
            'decomposer': decomposers[one_collective_label.getAttribute('分解器')],
            'connector': connectors[one_collective_label.getAttribute('联接器')]
        }

        collectives.update({one_collective_dict['id']: Collective(one_collective_dict)})
        collectives[one_collective_dict['id']].mission_msg_pool = message_group[
            collectives[one_collective_dict['id']].decomposer['group']]


def format_xml_to_member(xml_dom):
    root = xml_dom.documentElement
    primitive_format(root)
    collective_format(root)
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
    global collectives
    # collective与primitive连接为二部图，该连接为双向非对称网络
    for c in collectives.keys():
        pid_list = list(primitives.keys())
        mid_list = list(monitorMembers.keys())
        shuffle(pid_list)
        shuffle(mid_list)
        real_link_number = randrange(collectives[c].connector['conn_number'])
        for one_pid in pid_list[:real_link_number]:
            collectives[c].conn_primitive.update({one_pid: collectives[c].connector['average_conn_strength']})
            primitives[one_pid].the_connectors.update({c: primitives[one_pid].connector['average_conn_strength']})
        real_link_number = randrange(len(mid_list))
        remove_flag = False
        if c in mid_list:
            mid_list.remove(c)
            remove_flag = True
            print('remove self monitoring.')
        for one_mid in mid_list[:real_link_number]:
            collectives[c].monitorMembers.append(one_mid)
            monitorMembers[one_mid].the_conn_primitive.update({c: monitorMembers[one_mid].mon_endowment})
        if remove_flag:
            mid_list.append(c)
    # promitive相连，该连接为双向非对称网络
    for p in primitives.keys():
        pid_list = list(primitives.keys())
        aid_list = list(advisors.keys())
        mid_list = list(monitorMembers.keys())
        shuffle(pid_list)
        shuffle(aid_list)
        shuffle(mid_list)
        # 如果当前单元已有的连接关系还未饱和
        if primitives[p].connector['conn_number'] > len(primitives[p].the_connectors):
            real_link_number = randrange(primitives[p].connector['conn_number'] - len(primitives[p].the_connectors))
            remove_flag = False
            if p in pid_list[:real_link_number]:
                pid_list.remove(p)
                remove_flag = True
                print('remove self connect.')  # 测试发生移除自我连接的次数
            for one_pid in pid_list[:real_link_number]:  # 添加连接信息
                # 对方的连接关系中没有自己，且对方的连接关系尚未饱和
                if len(primitives[one_pid].the_connectors) < primitives[one_pid].connector['conn_number'] \
                        and one_pid not in primitives[p].the_connectors.keys():
                    primitives[p].the_connectors.update({one_pid: primitives[p].connector['average_conn_strength']})
                    primitives[one_pid].the_connectors.update(
                        {p: primitives[one_pid].connector['average_conn_strength']})
            if remove_flag:
                pid_list.append(p)
                remove_flag = False
        # 说明这个单元已经被动连接连满了
        else:
            pass
        # primitive与advisor相连，
        # 注意事项:拥有primitive角色的advisor不与自己连接
        real_link_number = randrange(len(aid_list))
        remove_flag = False
        if p in aid_list:
            aid_list.remove(p)
            remove_flag = True
            print('remove self advice.')  # 测试发生移除自我建议的次数
        for one_aid in aid_list[:real_link_number]:
            # 确定该primitive接收谁的建议
            primitives[p].the_advisors.append(one_aid)
            # 由于不确定本建议者会给多少个primitive提建议，所以建议强度初始值设置为禀赋
            advisors[one_aid].the_conn_primitive.update({p: advisors[one_aid].sug_endowment})
        if remove_flag:
            aid_list.append(p)
            remove_flag = False
        # 建议关系生成结束后要重置建议强度
        for a in advisors.keys():
            for cp in advisors[a].the_conn_primitive.keys():
                advisors[a].the_conn_primitive[cp] = advisors[a].sug_endowment / len(advisors[a].the_conn_primitive)
        # primitive与monitor相连，
        # 注意事项:拥有primitive角色的monitor不与自己连接
        real_link_number = randrange(len(mid_list))
        if p in mid_list:
            mid_list.remove(p)
            remove_flag = True
            print('remove self monitoring.')
        for one_mid in mid_list[:real_link_number]:
            primitives[p].the_monitorMembers.append(one_mid)
            monitorMembers[one_mid].the_conn_primitive.update({p: monitorMembers[one_mid].mon_endowment})
        if remove_flag:
            mid_list.append(p)
        # 监控关系生成结束后要重置监控强度
        for m in monitorMembers.keys():
            for cp in monitorMembers[m].the_conn_primitive.keys():
                monitorMembers[m].the_conn_primitive[cp] = monitorMembers[m].mon_endowment / len(
                    monitorMembers[m].the_conn_primitive)


if __name__ == '__main__':
    dom=read_xml(r'fpMemberXml_C.xml')
    print(dom.__class__)
    format_xml_to_member(read_xml(r'fpMemberXml_C.xml'))
    connect_all_member()
    print()
