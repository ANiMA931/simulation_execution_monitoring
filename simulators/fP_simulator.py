import threading
from time import sleep
from math import atan, cos
from members.fP_member import *


# 控制primitive线程的类
class PrimitiveThread(threading.Thread):
    def __init__(self, generation, primitive_name):
        super(PrimitiveThread, self).__init__()
        self.setName('Thread_' + primitive_name)
        self.primitive_id = primitive_name
        self.generation = generation

    def run(self) -> None:
        print(self.name, 'start')
        count = 0
        while count < self.generation:
            thread_main_loop(self.primitive_id, count)
            sleep(0.01)
        print(self.name, 'end')


def storage_message(primitive_id: str, message_list: list, the_round):
    """
    存储信息函数，存储的内容为tuple三元组，第一位为强度，第二位为信息本体，第三位为当前轮
    存储结束之后按照信息强度排列
    :param primitive_id: 要存信息的primitive的id
    :param message_list: 要被存储的message的列表
    :param the_round: 当前轮是第几轮
    :return: no return
    """
    # 将所有信息放到存储池中,存储池不会被别的线程修改内容，所以无需加锁
    # threading.Lock().acquire()
    for message in message_list:
        primitives[primitive_id].msg_storage_pool.append((message[0], message[1], the_round))
    # 根据已有的信息强度排序
    reversed(sorted(primitives[primitive_id].msg_storage_pool,key=lambda x:(x[0])))
    # 初始化计数器与信息强度总和
    count = 0
    the_sum = 0
    # 对于存储池中的所有信息
    for i in primitives[primitive_id].msg_storage_pool:
        # 如果当前的信息强度总和超出了存储禀赋
        if the_sum > primitives[primitive_id].msg_storage_endowment:
            # 通过切片截断后面的小信息强度的信息丢弃
            primitives[primitive_id].msg_storage_pool = primitives[primitive_id].msg_storage_pool[:count]
        # 如果未超出
        else:
            # 总和累加，计数器自增1，并继续
            the_sum += i[0]
            count += 1
            continue
    # threading.Lock().release()


def transmit_message(id_from_where: str, message: Message, id_to_where: str):
    """
    信息转发函数, 向目标单元的信息接收池中添加转发信息，信息包括成员间连接强度(用于排序)，信息实体，信息来源，信息来源性质
    :param id_from_where: 信息来源的primitive的id
    :param message: 发送的信息
    :param id_to_where: 信息接收方的id
    :return: no return
    """
    threading.Lock().acquire()
    primitives[id_to_where].msg_receive_pool.append(
        (primitives[id_to_where].the_connectors[id_from_where], deepcopy(message), id_from_where, 'transmit')
    )
    threading.Lock().release()


def broadcast_message(id_from_where: str, message: Message, id_to_where: str):
    """
    信息群发函数，在概率的情况下，计算信息被接收的概率
    :param id_from_where: 信息来源的id
    :param message: 发送的信息
    :param id_to_where: 信息的接收方的id
    :return: no return
    """
#    threading.Lock().acquire()
    # 接受概率等于（浏览禀赋/建议规模）+影响强度，通过反三角函数y=(2/Π)*arctan(x)归一化，降低变化斜率需对x做商
    x = (2 / pi) * atan(primitives[id_to_where].browse / primitives[id_to_where].connector['conn_number'] +
                        primitives[id_to_where].the_connectors[id_from_where])
    r = random()
    # 当r小于x，则表明落入接收概率
    if r < x:
        primitives[id_to_where].msg_receive_pool.append(
            (primitives[id_to_where].the_connectors[id_from_where], deepcopy(message), id_from_where, 'broadcast')
        )
#    threading.Lock().release()


def silence():
    """
    静默
    :return:no return
    """
    pass


def weak_weight(primitive_id: str, message: Message, from_where: str):
    """
    减弱信息强度
    :param primitive_id: 哪个单元要减弱信息强度
    :param message: 哪条信息的信息强度要被减弱
    :param from_where: 该信息来自谁
    :return: no return
    """
    threading.Lock().acquire()
    message.strength *= (1 - primitives[primitive_id].confidence) * primitives[primitive_id].the_connectors[from_where]
    threading.Lock().release()


def remove_relationship(primitive_id: str, who: str):
    """
    移除连接关系
    :param primitive_id: 谁要移除连接关系
    :param who: 移除与谁的连接关系
    :return: no return
    """
    threading.Lock().acquire()
    primitives[primitive_id].the_connectors.pop(who)
    threading.Lock().release()


def message_filtering(primitive_id: str):
    """
    信息过滤，当信息池中的信息量超出了primitive的禀赋时，将信息来源与自己连接强度低的个体的信息过滤掉
    :param primitive_id: 需要过滤信息的primitive的id
    :return:
    """
    # 首先按照强度排序，元组的第一个元素是连接强度,从大到小排序
    #threading.Lock().acquire()
    reversed(sorted(primitives[primitive_id].msg_receive_pool,key=lambda x:(x[0])))
    # 当信息池中的信息量超出了primitive的禀赋时,通过切片丢弃掉
    if len(primitives[primitive_id].msg_receive_pool) > primitives[primitive_id].msg_receive_endowment:
        primitives[primitive_id].msg_receive_pool = primitives[primitive_id].msg_receive_pool[
                                                    :primitives[primitive_id].msg_receive_endowment]
    #threading.Lock().release()


def gathering(primitive_id: str, self_decision: str):
    sug_pool = []  # 建议池
    # 建议统计字典
    sug_dict = {
        '转发': 0,
        '群发': 0,
        '减弱信息强度': 0,
        '改变连接强度': 0,
        '静默': 0,
    }
    # 对于每一个与本单元相连的个体，建议者给予建议，并连带建议强度
    for adv in primitives[primitive_id].the_advisors:
        sug_pool.append((advisors[adv].sug_path, advisors[adv].the_conn_primitive[primitive_id]))
    # 再将自己的决策添加进统计
    sug_dict[self_decision] += primitives[primitive_id].confidence
    for one_sug in sug_pool:
        sug_dict[one_sug[0]] += one_sug[1]
    true_dec=''
    true_dec_weight=0
    for sug in sug_dict.keys():
        if true_dec_weight<sug_dict[sug]:
            true_dec=sug
            true_dec_weight=sug_dict[sug]
    return true_dec


def make_decision(primitive_id: str, message: Message):
    """
    决策器得出决策的函数
    :param primitive_id: 做决策的primitive
    :param message: 要对什么信息做决策
    :return: no return
    """

    def is_similar(a: Message, b: Message):
        """
        判断a与b的相似性，领域相同且范围差绝对值小于10则为相似信息
        :param a: 信息a
        :param b: 信息b
        :return: 信息a与信息b是否相似
        """
        similar_threshold = pi / 18  # 相似阈值
        return abs(a.angle - b.angle) <= similar_threshold

    def projection(preference: Preference, the_message: Message) -> float:
        """
        投影函数，计算信息在偏好上的投影
        :param preference: 偏好
        :param the_message: 投影
        :return:
        """
        the_projection = 0
        #if the_message.area == preference.area:  # 如果话题相同
        green_range = preference.range  # 绿色区域，即该偏好覆盖的区域
        # 如果角度相符，就对该信息算投影
        if green_range[0] <= the_message.angle <= green_range[1] or green_range[
            0] <= the_message.angle <= 2 * pi or 0 <= the_message.angle <= green_range[1]:
            the_projection = the_message.strength * cos(the_message.z_angle)
        return the_projection

    sum_strength, count = 0, 0
    p_storage = primitives[primitive_id].msg_storage_pool.copy()
    # 对于每一条存储的信息
    flag = False
    for storage_msg in p_storage:
        # 如果与当前对比的信息相似
        if is_similar(storage_msg, message):
            sum_strength += storage_msg[0]
            flag = True
            count += 1
    if flag:
        new_strength = ((message.strength + sum_strength) / (count + 1)) * primitives[primitive_id].confidence
        message.strength = new_strength
    else:
        new_strength = message.strength * (1 - primitives[primitive_id].confidence)
        message.strength = new_strength
    p_decider = primitives[primitive_id].decider.copy()
    local_preference = p_decider['preference_vector']
    proj = projection(local_preference, message)
    if proj > 1:
        indicator = 1
    elif proj < -1:
        indicator = -1
    else:
        indicator = proj
    if indicator >= p_decider['forward_threshold']:
        # 转发
        return '转发'
    elif p_decider['mass_threshold'] <= indicator < p_decider['forward_threshold']:
        # 群发
        return '群发'
    elif p_decider['struct_change_threshold'] <= indicator < p_decider['weak_strength_threshold']:
        # 减弱信息强度
        return '减弱信息强度'
    elif indicator < p_decider['struct_change_threshold']:
        # 改变连接结构
        return '改变连接强度'
    else:
        # 静默
        return '静默'


def execute(decision: str, primitive_id: str, message: Message, from_where: str):
    """
    执行函数，决策要经过变异计算，
    :param decision: 决策器与连接器共同作用得到的决策
    :param primitive_id: 哪个单元要执行
    :param message: 对哪个信息进行操作
    :param from_where: 这条信息来自谁
    :return: no return
    """
    # 变异
    true_decision = decision
    path_decision = ['转发', '群发', '改变信息强度', '改变连接强度', '静默']
    # 随机数小于突变率，表明发生突变
    if random() < primitives[primitive_id].executor['mutation']:
        path_decision.remove(decision)
        true_decision = shuffle(path_decision)[0]

    # 监控
    def monitoring():
        """
        监控信息是否在本单元的监控者的监控范围内，以及是否被监控到
        :return:
        """

        def angle_in_range(angle, the_range) -> bool:
            """
            某个角度是否在范围里
            :param angle: 角度
            :param the_range: 范围
            :return: bool
            """
            # 不跨越0度
            if the_range[0] <= the_range[1]:
                return the_range[0] <= angle <= the_range[1]
            # 跨越0度
            else:
                return the_range[0] <= angle <= 2 * pi or 0 <= angle <= the_range[1]

        for one_monitor in primitives[primitive_id].the_monitorMembers:
            # 话题相同
            if monitorMembers[one_monitor].mon_area == message.area:
                # 在范围内
                if angle_in_range(message.angle, monitorMembers[one_monitor].mon_range):
                    # 随机数低于监控强度，表明监控成功
                    if random() < monitorMembers[one_monitor].the_conn_primitive[primitive_id]:
                        print(primitive_id, '由于信息', message.id, '被', one_monitor, '成功监控，信息转为静默')
                        return True
                    else:
                        return False
            else:
                return False

    #如果监控成功
    if monitoring() and true_decision in ['转发','群发']:
        print(primitive_id,'对信息',message.id,'原定操作为',true_decision)
        true_decision = '静默'
    # 真正的执行
    if true_decision == '转发':
        transmit_list = []
        for conn in primitives[primitive_id].the_connectors.keys():
            if primitives[primitive_id].the_connectors[conn] > primitives[primitive_id].executor['spreading_threshold']:
                transmit_list.append(conn)
        for conn_id in transmit_list:
            transmit_message(primitive_id, message, conn_id)
        print(primitive_id, '转发了信息', message.id)
    elif true_decision == '群发':
        for conn_id in primitives[primitive_id].the_connectors.keys():
            broadcast_message(primitive_id, message, conn_id)
        print(primitive_id, '群发了信息', message.id)
    elif true_decision == '改变信息强度':
        weak_weight(primitive_id, message, from_where)
        print(primitive_id, '由于信息', message.id, '减弱了该信息的强度')
    elif true_decision == '改变连接强度':
        remove_relationship(primitive_id, from_where)
        print(primitive_id, '由于信息', message.id, '移除了与', from_where, '的连接关系')
    else:
        silence()
        print(primitive_id, '由于信息', message.id, '选择静默。')


def thread_main_loop(primitive_id: str, the_round: int):
    """
    单元主循环，内容包括所有的成员，迭代数
    :param primitive_id: 主循环的primitive的id
    :param the_round: 主循环的当前轮
    :return: no return
    """
    # 信息过滤
    message_filtering(primitive_id)
    # 加锁
    #threading.Lock().acquire()
    # 将接收池中的所有信息移动到临时变量中
    temporary_pool = primitives[primitive_id].msg_receive_pool.copy()
    # 清空接收池
    primitives[primitive_id].msg_receive_pool.clear()
    # 解锁
    #threading.Lock().release()
    # {
    #       对于每一条临时变量中的信息
    for msg in temporary_pool:
        dec = make_decision(primitive_id, msg[1])
        true_dec = gathering(primitive_id, dec)
        execute(true_dec,primitive_id,deepcopy(msg[1]),msg[-1])

    storage_message(primitive_id, temporary_pool, the_round)


def looptest():
    """
    循环测试
    :return:
    """
    for id in primitives.keys():
        thread_main_loop(id,1)
    pass


def threadstest():
    """
    多线程测试
    :return:
    """
    pass


if __name__ == '__main__':
    format_xml_to_member(read_xml(r'F:\pythonCode\PycharmProjects\simulation_execution_monitoring\members\fP_Members.xml'))  # 读xml
    connect_all_member()  # 设置连接关系
    looptest()
    print()
