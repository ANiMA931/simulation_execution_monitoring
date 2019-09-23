import numpy as np
from random import shuffle
import xml.dom.minidom

class ua_linker:
    def __init__(self):
        pass

    def link_ua(self):
        def read_xml(in_path):
            '''''读取并解析xml文件
               in_path: xml路径
               return: ElementTree'''
            dom = xml.dom.minidom.parse(in_path)
            return dom

        dom = xml.dom.minidom.Document()
        for i in range(20):
            scale = np.random.randint(0, 10)
            unitdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml")
            root = unitdom.documentElement
            unit_memberType = root.getElementsByTagName('memberType')[0]
            effector = root.getElementsByTagName('effector')[0]
            effector.setAttribute('scale', str(scale))
            u_endowment = float(effector.getAttribute('remain'))
            a_s = list(range(20))
            shuffle(a_s)
            a_s = a_s[:scale]  # 拿到了编号

            for j in a_s:
                advsrdom = read_xml(
                    "E:\\code\\PycharmProjects\\simulation\\advisors\\" + "MyCrowd_advisor" + str(j).zfill(2) + ".xml")
                advsr_root = advsrdom.documentElement
                advsr_memberType = advsr_root.getElementsByTagName('memberType')[0]
                advisor = dom.createElement('advisor')
                advisor.setAttribute('aID', advsr_memberType.getAttribute('ID'))
                rand_a_strength = round(np.random.rand() * u_endowment, 5)
                u_endowment -= rand_a_strength
                advisor.setAttribute('strength', str(rand_a_strength))
                effector.appendChild(advisor)
                effector.setAttribute('remain',str(round(u_endowment,5)))

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
                try:
                    with open("E:\\code\\PycharmProjects\\simulation\\advisors\\" + "MyCrowd_advisor" + str(j).zfill(
                            2) + ".xml", 'w',
                              encoding='UTF-8') as fh:
                        advsrdom.writexml(fh)
                except:
                    print("error")
            try:
                with open("E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml",
                          'w',
                          encoding='UTF-8') as fh:
                    unitdom.writexml(fh)
            except:
                print("error")


if __name__ == '__main__':
    ua_linker().link_ua()
