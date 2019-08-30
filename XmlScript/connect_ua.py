import numpy as np
from random import shuffle
import xml.dom.minidom

"""我们先试一试一个普通的办法
首先第一点问题就是,ua表示unit和advisor
两者的连接关系是笛卡尔积子集
两者连接是双向的
一个连接的关系的形成，要两者都能保存连接关系
所以，随机数设定连接几个，再用shuffle函数随机确定连接具体哪几个
写连接关系的时候，要u与a都写
连接权重则需要写完连接关系的时候再重新分配"""


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
            """拿到了下标，接下
            来就是写关系
            可是关系该怎么写呢？"""
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
