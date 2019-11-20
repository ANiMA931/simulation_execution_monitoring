#connect_um.py
'''
本文件用于随机连接unit与monitor监控者，属于前期工具，现已无用
'''
import numpy as np
from random import shuffle
import xml.dom.minidom
from my_tools import *

class um_linker:
    def __init__(self):
        pass

    def link_um(self):
        dom = xml.dom.minidom.Document()
        unit_dir = r'..\units'
        monitor_dir = r'..\monitors'
        units_name = member_file_name(unit_dir)
        monitors_name = member_file_name(monitor_dir)

        for i in units_name:
            scale = np.random.randint(0, len(monitors_name) // 2)
            unitdom = read_xml(unit_dir + '\\\\' + i)
            '''unitdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml")'''
            root = unitdom.documentElement
            unit_memberType = root.getElementsByTagName('memberType')[0]
            monitorList = root.getElementsByTagName('executor')[0]
            monitorList.setAttribute('scale', str(scale))
            m_s = monitors_name.copy()
            shuffle(m_s)
            m_s = m_s[:scale]  # 拿到了编号

            for j in m_s:
                mntrdom = read_xml(monitor_dir+'\\\\'+j)
                '''mntrdom = read_xml(
                    "E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(j).zfill(2) + ".xml")'''
                mntr_root = mntrdom.documentElement
                mntr_memberType = mntr_root.getElementsByTagName('memberType')[0]
                monitor = dom.createElement('monitor')
                monitor.setAttribute('mID', mntr_memberType.getAttribute('ID'))
                monitorList.appendChild(monitor)

                unitList = mntr_root.getElementsByTagName('unitList')[0]
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
                write_xml(monitor_dir+'\\\\'+j,mntrdom)
            write_xml(unit_dir+'\\\\'+i,unitdom)

if __name__ == '__main__':
    um_linker().link_um()
