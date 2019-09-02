#from random_start import random_starter
from patterns.pattern import pattern

from member import *
from tools import *

#random_starter().init_random()
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
    """向它的advisor们"""
    dec_list=[]
    for a in u[1].effector['advisors'].items():
        print(a[0])
        advisors[a[0]].return_suggestion(u[1].now,ptn)
        pass
    """unit根据自己在格局上的位置用自己的方法make一个决策出来"""
    u[1].make_decision(ptn)
    """从自己的决策+建议者们的建议挑一个要执行的方案"""
    u[1].select_decision(dec_list)
    """挑出来之后，遍历这个执行方案是不是在某些监控者的范围内，累加它们的监控权重"""
    for m in u[1].executor['monitors']:#此处的m是monitor的id
        print(m['mID'])
        pass
    """外部监控权重+自律水平对抗自身的自退化水平，通过代价计算将要执行的动作"""
    """依照成功率执行，执行成功就更新unit的now，不成功就不更新"""
    """广播自己的执行内容给其他相连的"""
pass
