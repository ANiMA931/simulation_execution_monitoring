#create_responsibility.py
'''
本文件用于给监控者monitor添加格局上的监控范围即每个behavior
前期工具，现已无用
'''
import numpy as np
from random import shuffle
from tools import *


class responsibility_creator:
    def __init__(self):
        pass

    def create_responsibility(self):
        ptndom = read_xml(r"..\patterns\pattern1.xml")

        root = ptndom.documentElement
        behaviors = root.getElementsByTagName('behavior')
        responsible_upper = len(behaviors)
        b = []
        for i in range(len(behaviors)):
            b.append((behaviors[i].getAttribute('before'), behaviors[i].getAttribute('after')))
        monitors_dir=r"..\monitors"
        monitors_name=member_file_name(monitors_dir)
        for i in monitors_name:
            mntrdom=read_xml(monitors_dir+'\\\\'+i)
            root = mntrdom.documentElement
            monitoring = root.getElementsByTagName('monitoring')[0]
            shuffle(b)
            responsible_count = np.random.randint(0, responsible_upper//2)
            v = str(b[0])
            for j in range(1, responsible_count):
                v += "|" + str(b[j])
            monitoring.setAttribute('scale',str(responsible_count))
            monitoring.setAttribute('value', v)
            write_xml(monitors_dir+'\\\\'+i, mntrdom)
        # 旧代码只能操作固定个数
        '''for i in range(20):
            mntrdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(i).zfill(2) + ".xml")
            root = mntrdom.documentElement
            monitoring = root.getElementsByTagName('monitoring')[0]
            shuffle(b)
            responsible_count = np.random.randint(0, responsible_upper)
            v = str(b[0])
            for j in range(1, responsible_count):
                v += "|" + str(b[j])
            monitoring.setAttribute('value', v)
            write_xml("E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(i).zfill(
                2) + ".xml", mntrdom)'''


if __name__ == '__main__':
    responsibility_creator().create_responsibility()
