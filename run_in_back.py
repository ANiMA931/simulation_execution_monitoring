from random_start import random_starter
from math import pi,atan,inf
from member import *
from tools import *
from random import shuffle
from numpy.random import rand
# random_starter().init_random()
units_path = 'E:\\code\\PycharmProjects\\simulation\\units'
advisor_path = 'E:\\code\\PycharmProjects\\simulation\\advisors'
monitor_path = 'E:\\code\\PycharmProjects\\simulation\\monitors'
pattern_path = 'E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml'

units_names = member_file_name(units_path)
advisors_names = member_file_name(advisor_path)
monitors_names = member_file_name(monitor_path)
units = {}
advisors = {}
monitors = {}
ptn = pattern(xml_dom=read_xml(pattern_path))
"""拿到所有的成员"""
for i in units_names:
    u = unit(xml_dom=read_xml(units_path + '\\\\' + i))
    units.update({u.id: u})
for i in advisors_names:
    a = advisor(xml_dom=read_xml(advisor_path + '\\\\' + i))
    advisors.update({a.id: a})
for i in monitors_names:
    m = monitor(xml_dom=read_xml(monitor_path + '\\\\' + i))
    monitors.update({m.id: m})
ptn = pattern(read_xml(pattern_path))
"""对于每一个unit"""
for u in units.items():

    dec_list = []
    ex_m = float(0)  # 外部监督强度
    """向它的advisor们"""
    for a in u[1].effector['advisors'].items():
        dec_list.append((advisors[a[0]].id, advisors[a[0]].unitList['units'][u[1].id],
                         advisors[a[0]].return_suggestion(u[1].now, ptn)))
        pass
    """unit根据自己在格局上的位置用自己的方法make一个决策出来"""
    dec_list.append((u[1].id, u[1].decider['selfConfidence'], u[1].make_decision(ptn)))
    """从自己的决策+建议者们的建议挑一个要执行的方案"""
    dec=u[1].select_decision(dec_list,ptn)
    """挑出来之后，遍历这个执行方案是不是在某些监控者的范围内，累加它们的监控权重"""

    for m in u[1].executor['monitors']:  # 此处的m是monitor的字典
        if dec in monitors[m['mID']].responsibility:#当某个行为是被监控者监控的，那么就加上外部的监督强度
            ex_m += monitors[m['mID']].unitList['units'][u[1].id]
        pass
    """外部监控权重+自律水平对抗自身的自退化水平以及突变，通过代价计算将要执行的动作"""
    tmp_b=[]
    tmp_w=[]
    for i in ptn.behaviors:
        if dec[0]==i['before']:
            tmp_b.append(i)
    min_b=dec_b={}
    min_w_temp=inf
    for i in tmp_b:#定位到weight最小与决定的behavior
        if min_w_temp>i['weight']:
            min_b=i
            min_w_temp=i['weight']
        if dec[0]==i['before'] and dec[1]==i['after']:
            dec_b=i
    del min_w_temp
    r1=(1-(2/pi)*atan(ex_m))*dec_b['weight']
    if u[1].executor['selfDiscipline']>=u[1].executor['selfDegeneration']:
        r0=min_b['weight']
    else:
        r0=(1-(2/pi)*atan(u[1].executor['selfDegeneration']-u[1].executor['selfDispline']))*min_b['weight']
    """依照成功率执行，执行成功就更新unit的now，不成功就不更新"""
    if r1<r0:
        if rand()<u[1].executor['mutationRate']:
            shuffle(tmp_b)
            dec=(tmp_b[0]['before'],tmp_b[0]['after'])
            u[1].do_behavior(ptn,dec)
        else:
            u[1].do_behavior(ptn, dec)
    else:
        if rand() < u[1].executor['mutationRate']:
            shuffle(tmp_b)
            dec = (tmp_b[0]['before'], tmp_b[0]['after'])
            u[1].do_behavior(ptn, dec)
        else:
            u[1].do_behavior(ptn,(min_b['before'],min_b['after']))
    """广播自己的执行内容给其他相连的"""
    for c_u in u[1].parameter['c_units']:  # 此处的c_u是本unit连接的unit的id
        units[c_u].get_para_message()
        """此处可能会有一段根据获得信息更改自己与其他单位的连接权重的代码"""
        units[c_u].reset_connection()
    pass
pass
