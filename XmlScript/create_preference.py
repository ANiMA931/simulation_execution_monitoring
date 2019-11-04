# create_preference.py
'''
本文件用于给描述advisor的xml中添加preference标签的value属性
即给一个xml生成偏好路径所用，前期工具，现已无用
'''
import numpy as np
import pandas as pd
from random import shuffle
from patterns.pattern import pattern
from tools import *


class preference_creator:
    def __init__(self,pattern):
        self.pattern=pattern

    def creat_preference(self):
        ptndom = read_xml(r"..\patterns\pattern1.xml")
        root = ptndom.documentElement
        position_p = root.getElementsByTagName('position')

        positions = np.zeros((len(position_p), len(position_p)), dtype=np.float)
        positions_=pd.DataFrame(positions)
        positions_id=[]
        for pi in position_p:
            positions_id.append(pi.getAttribute('pID'))
        positions_.columns=positions_id
        positions_.index=positions_id
        behaviors = root.getElementsByTagName('behavior')
        for i in range(len(behaviors)):
            before = behaviors[i].getAttribute('before')
            after = behaviors[i].getAttribute('after')
            positions_[before][after] = float(behaviors[i].getAttribute('weight'))
        def make_preference(positions,pattern):
            '''
            本函数能够给出一套从起点到终点的完整路径
            :param positions: position的Dataframe
            :param pattern: pattern本体
            :return:
            '''
            start = pattern.init_position
            p = [start]
            while positions[start].any() != 0:
                gate = []
                for i in positions.index:
                    if positions[start][i] != 0:
                        gate.append(i)
                shuffle(gate)
                start = gate[0]
                p.append(start)
            pfrc = str(p[0])
            for i in range(1, len(p)):
                pfrc += "," + str(p[i])
            return pfrc

        advisor_dir = r'..\advisors'
        advisors_name = member_file_name(advisor_dir)
        for i in advisors_name:
            advsrdom = read_xml(advisor_dir + '\\\\' + i)
            root = advsrdom.documentElement
            preference = root.getElementsByTagName('preference')
            pfrc = make_preference(positions_,self.pattern)
            preference[0].setAttribute('value', pfrc)
            write_xml(advisor_dir + '\\\\' + i, advsrdom)
        '''for i in range(20):
            advsrdom = read_xml(
                "..\\advisors\\" + "MyCrowd_advisor" + str(i).zfill(2) + ".xml")
            root = advsrdom.documentElement
            preference = root.getElementsByTagName('preference')
            pfrc = make_preference(positions)
            preference[0].setAttribute('value', pfrc)
            write_xml("..\\advisors\\" + "MyCrowd_advisor" + str(i).zfill(
                2) + ".xml", advsrdom)'''


if __name__ == '__main__':
    pattern_dir=r'E:\code\PycharmProjects\simulation\patterns\pattern1.xml'
    preference_creator(read_xml(pattern_dir)).creat_preference()
