# connect_ua.py
'''
本文件用于随机连接unit与advisor建议者，属于前期工具，现已无用
'''
import numpy as np
from random import shuffle
import xml.dom.minidom
from tools import *


class ua_linker:
    def __init__(self):
        pass

    def link_ua(self):

        dom = xml.dom.minidom.Document()
        unit_dir = r'..\units'
        advisor_dir = r'..\advisors'
        units_name = member_file_name(unit_dir)
        advisors_name = member_file_name(advisor_dir)

        for i in units_name:
            scale = np.random.randint(0, len(advisors_name) // 2)
            unitdom = read_xml(unit_dir + '\\\\' + i)
            '''unitdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml")'''
            root = unitdom.documentElement
            unit_memberType = root.getElementsByTagName('memberType')[0]
            effector = root.getElementsByTagName('effector')[0]
            effector.setAttribute('scale', str(scale))
            u_endowment = float(effector.getAttribute('remain'))
            a_s = advisors_name.copy()
            shuffle(a_s)
            a_s = a_s[:scale]  # 拿到了编号

            for j in a_s:
                advsrdom = read_xml(advisor_dir + '\\\\' + j)
                '''advsrdom = read_xml(
                    "E:\\code\\PycharmProjects\\simulation\\advisors\\" + "MyCrowd_advisor" + str(j).zfill(2) + ".xml")'''
                advsr_root = advsrdom.documentElement
                advsr_memberType = advsr_root.getElementsByTagName('memberType')[0]
                advisor = dom.createElement('advisor')
                advisor.setAttribute('aID', advsr_memberType.getAttribute('ID'))
                rand_a_strength = round(np.random.rand() * u_endowment, 5)
                u_endowment -= rand_a_strength
                advisor.setAttribute('strength', str(rand_a_strength))
                effector.appendChild(advisor)
                effector.setAttribute('remain', str(round(u_endowment, 5)))

                unitList = advsr_root.getElementsByTagName('unitList')[0]
                unit_scale = int(unitList.getAttribute('scale')) + 1
                unitList.setAttribute('scale', str(unit_scale))
                remain = float(unitList.getAttribute('remaining'))
                rand_u_strength = round(np.random.rand() * remain, 5)
                remain -= rand_u_strength
                unitList.setAttribute('remaining', str(round(remain, 5)))
                unit = dom.createElement('unit')
                unit.setAttribute('uID', unit_memberType.getAttribute('ID'))
                unit.setAttribute('strength', str(rand_u_strength))
                unitList.appendChild(unit)
                write_xml(advisor_dir + '\\\\' + j, advsrdom)

            write_xml(unit_dir + '\\\\' + i, unitdom)


if __name__ == '__main__':
    ua_linker().link_ua()
