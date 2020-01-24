from my_tools import *


# 基础成员
class member(object):
    def __init__(self, self_dict: dict):
        self.id = self_dict['id']  # 成员的id
        self.metaModel_id = self_dict['metaModel_id']  # 成员的元模型id


# 原子型成员
primitives = dict()
advisors=dict()
monitorMembers=dict()

class primitive(member):
    def __init__(self, self_dict: dict):
        super(primitive, self).__init__(self_dict)
        self.msg_receive_endowment = self_dict['msg_receive_endowment']  # 信息接收禀赋
        self.msg_receive_pool = []  # 信息接收池
        self.msg_storage_endowment = self_dict['msg_storage_endowment']  # 信息存储禀赋
        self.msg_storage_pool = []  # 信息存储池
        self.confidence = self_dict['confidence']  # 个人自信水平
        self.discipline = self_dict['discipline']  # 个人自律水平
        self.browse = self_dict['browse']  # 个人浏览禀赋
        self.pattern = self_dict['pattern']  # 个人格局
        self.affector = self_dict['affector']  # 影响器
        self.decider = self_dict['decider']  # 决策器
        self.executor = self_dict['executor']  # 执行器
        self.monitor = self_dict['monitor']  # 监控器
        self.connector = self_dict['connector']  # 连接器


# 建议者
class advisor(member):
    def __init__(self, self_dict: dict):
        super(advisor, self).__init__(self_dict)
        self.sug_endowment = self_dict['sug_endowment']  # 建议禀赋
        self.sug_path = self_dict['sug_path']  # 建议路径


class monitorMember(member):
    def __init__(self, self_dict: dict):
        super(monitorMember, self).__init__(self_dict)
        self.mon_endowment = self_dict['mon_endowment']  # 监控禀赋
        self.mon_area = self_dict['mon_area']  # 监控领域
        self.mon_range = self_dict['mon_range']  # 监控领域角度范围 tuple


# 信息类
class message:
    def __init__(self, self_dict: dict):
        self.id = self_dict['id']  # 信息id
        self.area = self_dict['area']  # 信息领域
        self.strength = self_dict['strength']  # 信息强度
        self.range = self_dict['range']  # 信息角度范围 tuple


# 偏好类，与信息类完全相同
class preference(message):
    def __init__(self, self_dict: dict):
        super(preference, self).__init__(self_dict)


def formatXmltoMember(xml_dom):
    root = xml_dom.documentElement
    # 偏好整合
    preferenceInfo_labels = root.getElementsByTagName('preferenceInfo')
    preferences = dict()
    for one_preference_label in preferenceInfo_labels:
        start, end = one_preference_label.getAttribute('偏好方向').split('-')
        one_preference = {
            'id': one_preference_label.getAttribute('偏好ID'),
            'area': one_preference_label.getAttribute('所属领域ID'),
            'strength': float(one_preference_label.getAttribute('偏好大小')),
            'range': (float(start), float(end))
        }
        preferences.update({one_preference_label.getAttribute('偏好ID'): preference(one_preference)})
    # 信息整合
    messageInfo_labels = root.getElementsByTagName('messageInfo')
    messages = dict()
    for one_message_label in messageInfo_labels:
        start, end = one_message_label.getAttribute('信息方向').split('-')
        one_message = {
            'id': one_message_label.getAttribute('信息ID'),
            'area': one_message_label.getAttribute('所属领域ID'),
            'strength': float(one_message_label.getAttribute('信息大小')),
            'range': (float(start), float(end))
        }
        messages.update({one_message_label.getAttribute('信息ID'): message(one_message)})
    # 影响器整合
    affectorInfo_labels = root.getElementsByTagName('affectorInfo')
    affectors = dict()
    for one_affector_label in affectorInfo_labels:
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
            'forward_threshold': one_decider_label.getAttribute('转发阈值'),
            'mass_threshold': one_decider_label.getAttribute('群发阈值'),
            'struct_change_threshold': one_decider_label.getAttribute('改变连接结构阈值'),
            'weak_strength_threshold': one_decider_label.getAttribute('减弱信息强度阈值'),
            'preference_vector': preferences[one_decider_label.getAttribute('偏好矢量')],
            'message_vector': messages[one_decider_label.getAttribute('信息矢量')]
        }
        deciders.update({one_decider_label.getAttribute('决策器ID'): one_decider})

    # 执行器整合
    executorInfo_labels = root.getElementsByTagName('executorInfo')
    executors = dict()
    for one_executor_label in executorInfo_labels:
        one_executor = {
            'id': one_executor_label.getAttribute('执行器ID'),
            'mutation': float(one_executor_label.getAttribute('突变率')),
            'spreading_threshold': float(one_executor_label.getAttribute('传播阈值')),
            'preference_behavior': one_executor_label.getAttribute('偏好行为'),
            'message_vector': messages[one_executor_label.getAttribute('信息矢量')]
        }
        executors.update({one_executor_label.getAttribute('执行器ID'): one_executor})
    # 监控器整合
    monitorsInfo_labels = root.getElementsByTagName('monitorInfo')
    monitors = dict()
    for one_monitor_label in monitorsInfo_labels:
        one_monitor = {
            'id': one_monitor_label.getAttribute('监控器ID'),
            'mon_strength': float(one_monitor_label.getAttribute('监控强度'))
        }
        monitors.update({one_monitor_label.getAttribute('监控器ID'):one_monitor})
    # 连接器整合
    connectorsInfo_labels = root.getElementsByTagName('connectorInfo')
    connectors=dict()
    for one_connector_label in connectorsInfo_labels:
        one_connector={
            'id':one_connector_label.getAttribute('联接器ID'),
            'conn_number':int(one_connector_label.getAttribute('连接成员数量')),
            'average_conn_strength':float(one_connector_label.getAttribute('平均连接强度'))
        }
        connectors.update({one_connector_label.getAttribute('联接器ID'):one_connector})
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
            one_primitive_label.getAttribute('原子型成员ID'): primitive(primitive_dict),
        })
    # 建议者整合
    advisorInfo_labels = root.getElementsByTagName('advisorInfo')
    for one_advisor_label in advisorInfo_labels:
        advisor_dict=dict()
        advisor_dict.update({
            'id':one_advisor_label.getAttribute('建议者ID'),
            'metaModel_id':one_advisor_label.getAttribute('成员模型'),
            'sug_endowment':float(one_advisor_label.getAttribute('建议禀赋')),
            'sug_path':one_advisor_label.getAttribute('建议路径')
        })
        advisors.update({
            one_advisor_label.getAttribute('建议者ID'):advisor(advisor_dict),
        })
    # 监控者整合
    monitorMemberInfo_labels = root.getElementsByTagName('monitorMemberInfo')
    for one_monitorMember_label in monitorMemberInfo_labels:
        monitorMember_dict=dict()
        start, end = one_monitorMember_label.getAttribute('监控范围').split('-')
        monitorMember_dict.update({
            'id':one_monitorMember_label.getAttribute('监控者ID'),
            'metaModel_id':one_monitorMember_label.getAttribute('成员模型'),
            'mon_endowment':one_monitorMember_label.getAttribute('监控禀赋'),
            'mon_area':one_monitorMember_label.getAttribute('监控领域'),
            'mon_range':(float(start),float(end))
        })
        monitorMembers.update({
            one_monitorMember_label.getAttribute('监控者ID'):monitorMember(monitorMember_dict),
        })
def connectAllMember():



if __name__ == '__main__':
    formatXmltoMember(read_xml(r'fP_Members.xml'))
    connectAllMember()
    print()
