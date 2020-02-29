from math import cos
from time import time
import xlsxwriter
from members.fP_member import *


def thread_main_loop_for_collective(collective_id: str, the_round: int):
    """
    集合型单元主循环
    :param collective_id: 主循环的collective的id
    :param the_round: 主循环的当前轮
    :return: no return
    """
    # 任务获得至任务槽，通过取余数实现任务轮转
    group = (collectives[collective_id].decomposer['group'] + the_round) % group_N
    the_len = len(message_group[group])
    true_len = randrange(the_len // 20)
    shuffle(collectives[collective_id].mission_msg_pool)
    collectives[collective_id].mission_msg_pool = message_group[group][:true_len]
    # 对任务槽中的任务信息进行轮换转发，在任务槽不为空时转发
    for m in collectives[collective_id].mission_msg_pool:
        for p in collectives[collective_id].conn_primitive.keys():
            transmit_message_for_collective(collective_id, deepcopy(messages[m]), p)


def transmit_message_for_collective(id_from_where: str, message: Message, id_to_where: str):
    """
    集合型成员的转发信息函数
    :param id_from_where:
    :param message:
    :param id_to_where:
    :return:
    """
    # 由于存在你还在转发过程，就有目标已经把你删好友的可能性
    if id_from_where in primitives[id_to_where].the_connectors.keys():
        message.strength *= primitives[id_to_where].the_connectors[id_from_where]
        primitives[id_to_where].msg_receive_pool.append(
            [primitives[id_to_where].the_connectors[id_from_where] * message.strength, deepcopy(message), id_from_where]
        )
        # print('水军', id_from_where, '转发了信息', message.id, '给', id_to_where)


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
        return abs(a.angle - b.angle) <= similar_threshold and a.area == b.area

    def projection(preference: Preference, the_message: Message) -> float:
        """
        投影函数，计算信息在偏好上的投影
        :param preference: 偏好
        :param the_message: 投影
        :return:
        """
        the_projection = 0
        if preference.area != the_message.area:
            return the_projection
        # if the_message.area == preference.area:  # 如果话题相同
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
        if is_similar(storage_msg[1], message):
            sum_strength += storage_msg[1].strength
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
    # proj = projection(local_preference, message)
    if message.area == local_preference.area:
        proj = cos(message.z_angle)
    else:
        proj = 0
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


def message_filtering(primitive_id: str):
    """
    信息过滤，当信息池中的信息量超出了primitive的禀赋时，将信息来源与自己连接强度低的个体的信息过滤掉
    :param primitive_id: 需要过滤信息的primitive的id
    :return:
    """
    # 首先按照强度排序，元组的第一个元素是连接强度,从大到小排序
    primitives[primitive_id].msg_receive_pool = list(
        reversed(sorted(primitives[primitive_id].msg_receive_pool, key=lambda x: (x[0]))))
    # 当信息池中的信息量超出了primitive的禀赋时,通过切片丢弃掉
    if len(primitives[primitive_id].msg_receive_pool) > primitives[primitive_id].msg_receive_endowment:
        primitives[primitive_id].msg_receive_pool = primitives[primitive_id].msg_receive_pool[
                                                    :primitives[primitive_id].msg_receive_endowment]


def transmit_message(id_from_where: str, message: Message, id_to_where: str):
    """
    信息转发函数, 向目标单元的信息接收池中添加转发信息，信息包括成员间连接强度(用于排序)，信息实体，信息来源，信息来源性质
    :param id_from_where: 信息来源的primitive的id
    :param message: 发送的信息
    :param id_to_where: 信息接收方的id
    :return: no return
    """
    # 理论上讲，primitive成员同样连接着collective成员，但是collective成员不接收信息，所以需要一步识别
    if id_to_where in primitives.keys():
        message.strength *= primitives[id_to_where].the_connectors[id_from_where]
        primitives[id_to_where].msg_receive_pool.append(
            [primitives[id_to_where].the_connectors[id_from_where] * message.strength, deepcopy(message), id_from_where]
        )


def broadcast_message(id_from_where: str, message: Message, id_to_where: str):
    """
    信息群发函数，在概率的情况下，计算信息被接收的概率
    :param id_from_where: 信息来源的id
    :param message: 发送的信息
    :param id_to_where: 信息的接收方的id
    :return: no return
    """
    print(id_from_where, '群发了信息', message.id, '给', id_to_where, end='')
    if id_to_where in primitives.keys():
        # 接受概率等于（浏览禀赋/建议规模）+影响强度，通过反三角函数y=(2/Π)*arctan(x)归一化，降低变化斜率需对x做商
        x = primitives[id_to_where].browse / primitives[id_to_where].connector['conn_number'] + \
            primitives[id_to_where].the_connectors[id_from_where]
        r = random()
        # 当r小于x，则表明落入接收概率
        if r < x:
            message.strength *= primitives[id_to_where].the_connectors[id_from_where]
            primitives[id_to_where].msg_receive_pool.append(
                [primitives[id_to_where].the_connectors[id_from_where] * message.strength, deepcopy(message),
                 id_from_where])
            print('成功')
        else:
            print('失败')
    else:
        print('\n', id_to_where, '是collective成员，对方不感兴趣')


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
    message.strength *= (1 - primitives[primitive_id].confidence) * primitives[primitive_id].the_connectors[from_where]


def remove_relationship(primitive_id: str, who: str):
    """
    移除连接关系
    :param primitive_id: 谁要移除连接关系
    :param who: 移除与谁的连接关系
    :return: no return
    """
    # 存在初始信息是极端反面的可能，但是初始信息标记的源头为自己，所以假装无事发生
    if who != 'self':
        # 如果在的话就移除，不在的话表示已经移除了
        if who in primitives[primitive_id].the_connectors.keys():
            primitives[primitive_id].the_connectors.pop(who)
        if who in primitives.keys():  # 存在对方是集合型单元的可能
            # 存在早已移除对方但对方的旧信息还未来得及处理的可能性，此处假装无事发生
            if primitive_id in primitives[who].the_connectors.keys():
                primitives[who].the_connectors.pop(primitive_id)
        else:
            # 线程出差错时，存在多次移除的问题，当遇到多次移除时，我们假装无事发生
            if primitive_id in collectives[who].conn_primitive.keys():
                collectives[who].conn_primitive.pop(primitive_id)


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
    true_dec = ''
    true_dec_weight = 0
    for sug in sug_dict.keys():
        if true_dec_weight < sug_dict[sug]:
            true_dec = sug
            true_dec_weight = sug_dict[sug]
    return true_dec


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
    path_decision = ['转发', '群发', '减弱信息强度', '改变连接强度', '静默']
    # 随机数小于突变率，表明发生突变
    if random() < primitives[primitive_id].executor['mutation']:
        path_decision.remove(decision)
        shuffle(path_decision)
        true_decision = path_decision[0]

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

    # 如果监控成功
    if monitoring() and true_decision in ['转发', '群发']:
        print(primitive_id, '对信息', message.id, '原定操作为', true_decision)
        true_decision = '静默'
    # 真正的执行
    if true_decision == '转发':
        transmit_list = []
        for conn in primitives[primitive_id].the_connectors.keys():
            if primitives[primitive_id].the_connectors[conn] > primitives[primitive_id].executor['spreading_threshold']:
                transmit_list.append(conn)
        for conn_id in transmit_list:
            transmit_message(primitive_id, message, conn_id)
            print(primitive_id, '转发了信息', message.id, '给', conn_id)
    elif true_decision == '群发':
        for conn_id in primitives[primitive_id].the_connectors.keys():
            broadcast_message(primitive_id, message, conn_id)
    elif true_decision == '改变信息强度':
        weak_weight(primitive_id, message, from_where)
        print(primitive_id, '由于信息', message.id, '减弱了该信息的强度')
    elif true_decision == '改变连接强度':
        remove_relationship(primitive_id, from_where)
        print(primitive_id, '由于信息', message.id, '移除了与', from_where, '的连接关系')
    else:
        silence()
        print(primitive_id, '由于信息', message.id, '选择静默。')


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
    new_msg_flag = True
    for message in message_list:
        for s_message in primitives[primitive_id].msg_storage_pool:
            if message[1].id == s_message[1].id:
                s_message[1].strength = max(s_message[1].strength, message[1].strength)
                s_message[0] = s_message[1].strength
                new_msg_flag = False
            else:
                continue
        if new_msg_flag:
            primitives[primitive_id].msg_storage_pool.append([message[0], message[1], the_round])
    # 根据已有的信息强度排序
    primitives[primitive_id].msg_storage_pool = list(
        reversed(sorted(primitives[primitive_id].msg_storage_pool, key=lambda x: (x[0]))))
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


def make_record(primitive_id, the_round, receive_msg_pool):
    """
    生成仿真记录
    :param primitive_id: 要生成记录的成员id
    :param the_round: 该成员仿真了几代
    :return:
    """
    # 要记录这个人在这一轮收到了谁的信息，信息内容是什么，对这个信息的处理结果是什么，最后是所有信息处理完之后，存储信息还剩什么内容
    global record_dict
    strg_strength_sum = 0
    rcv_strength_sum = 0
    for strg in primitives[primitive_id].msg_storage_pool:
        strg_strength_sum += strg[1].strength
    for strg_c in receive_msg_pool:
        rcv_strength_sum += strg_c[1].strength
        message_rec_dict[the_round][strg_c[1].id] += strg_c[1].strength
    record_dict.get(the_round).update({
        primitive_id: {
            'storage': primitives[primitive_id].msg_storage_pool,
            'receive': receive_msg_pool,
            'strength_sum': strg_strength_sum,
            'rcv_strength_sum': rcv_strength_sum,
        }
    })


def record_format():
    global record_dict, record_sum_stngth_list, record_sum_stngth_rcv_list
    for key in record_dict.keys():
        glb_msg_sum_strength = 0
        glb_msg_sum_rcv_strength = 0
        for p_id in record_dict[key].keys():
            glb_msg_sum_strength += record_dict[key][p_id]['strength_sum']
            glb_msg_sum_rcv_strength += record_dict[key][p_id]['rcv_strength_sum']
        record_dict[key].update({
            'glb_msg_sum_strength': glb_msg_sum_strength,
            'glb_msg_sum_rcv_strength': glb_msg_sum_rcv_strength,
        })
        record_sum_stngth_list.append(glb_msg_sum_strength)
        record_sum_stngth_rcv_list.append(glb_msg_sum_rcv_strength)


if __name__ == '__main__':
    format_xml_to_member(read_xml(r'..\members\fpMemberXml_C.xml'))
    connect_all_member()
    message_distribute()

    record_dict = dict()
    message_rec_dict = dict()
    record_sum_stngth_list = list()
    record_sum_stngth_rcv_list = list()

    all_round = 200
    base_collective_foot_size_upper = 50
    base_collective_foot_size_floor = 20
    tmp_rcv_pool = dict()
    tmp_dec = dict()

    for i in range(all_round):
        record_dict.update({i: dict()})
        msg_round_record = dict()
        for msg_id in messages.keys():
            msg_round_record.update({msg_id: 0.0})
        message_rec_dict.update({i: msg_round_record})

    for p in primitives.keys():
        tmp_rcv_pool.update({
            p: list()
        })
        tmp_dec.update({
            p: list()
        })
    a = time()
    true_size = randrange(base_collective_foot_size_floor, base_collective_foot_size_upper)  # 第一轮不投放信息
    # true_size = 0 # 第一轮投放信息
    for r in range(all_round):
        # 如果到了步长，collective转发就要运行
        if true_size == 0:
            tl = randrange(1, len(collectives.keys()))
            t_lst = list(collectives.keys())
            shuffle(t_lst)
            for c in t_lst[:tl]:
                thread_main_loop_for_collective(c, r)
                true_size = randrange(base_collective_foot_size_floor, base_collective_foot_size_upper)
        # 无论运行与否，primitive都要走它自己的流程，但必须同步，
        for p in primitives.keys():
            # 第一步流程是信息过滤，暂存，同时清空接收池
            # 过滤
            message_filtering(p)
            # 暂存
            tmp_rcv_pool[p] = primitives[p].msg_receive_pool.copy()
            # 清空
            primitives[p].msg_receive_pool.clear()
        for p in primitives.keys():
            # 对接收到的信息进行决策
            for msg in tmp_rcv_pool[p]:
                dec = make_decision(p, msg[1])
                true_dec = gathering(p, dec)
                tmp_dec[p].append(true_dec)
        for p in primitives.keys():
            # 得到的决策统一处理
            for msg, dec in zip(tmp_rcv_pool[p], tmp_dec[p]):
                execute(dec, p, msg[1], msg[-1])
            storage_message(p, tmp_rcv_pool[p], r)
            make_record(p, r, tmp_rcv_pool[p])
            tmp_dec[p].clear()
            tmp_rcv_pool[p].clear()
        true_size -= 1
    record_format()
    print('simulation end.\nTime =', time() - a)

    filename = open('a.txt', 'w')
    for v in record_sum_stngth_rcv_list:
        filename.write(str(v) + '\n')
    filename.close()
    filename = open('b.txt', 'w')
    for r in message_rec_dict.keys():
        filename.write(str(r) + '---')
        for msg in message_rec_dict[r].keys():
            filename.write(msg + ':' + str(message_rec_dict[r][msg]) + ',')
        filename.write('\n')
    filename.close()
    wb = xlsxwriter.Workbook('simu_rec_table')
    ws = wb.add_worksheet('simu_record')
    ws.write(0, 1, 'sum')
    for i, m in zip(range(all_round), record_sum_stngth_rcv_list):
        ws.write(i + 1, 0, i)
        ws.write(i + 1, 1, m)

    for j, k in zip(messages.keys(), range(messages.__len__())):
        ws.write(0, k + 2, j)
        for n in range(all_round):
            ws.write(n + 1, k + 2, message_rec_dict[n][j])
    wb.close()
    print(1)
