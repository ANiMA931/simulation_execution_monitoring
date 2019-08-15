# -*- coding: utf-8 -*-
"""
随机生成监控区间

"""

import random
import xml.etree.ElementTree as ET
import numpy as np

from math import pi



TOPIC_RANGE = 10#话题种类数
Monitor_Count = 20#监控的总条目数期望
monitor_count_real = 0#实际监控的总条目数
topic_range_bewatched = []
precision = 5#角度的小数点精度

root = ET.Element("monitor_areas")
tree = ET.ElementTree(root)

monitor_areas = ET.SubElement(root,"monitor_area")



#判断随机设定的监控范围是否与已有的监控范围相交
def right_topic_range_bewatched(TPC,SAGL,EAGL):
    #起始角度大于终止角度的直接返回
    if SAGL > EAGL:
        return True
    else:
        sub_topic_range_bewatched = []
        #找出topic相同的子范围,放到sub_topic_range_bewatched里面去
        for i in range(len(topic_range_bewatched)):
            if TPC == topic_range_bewatched[i][0]:
                sub_topic_range_bewatched.append([topic_range_bewatched[i][1],topic_range_bewatched[i][2]])
            else:
                pass

        #在已经挑出来的sub_topic_range_bewatched里面计算
        for i in range(len(sub_topic_range_bewatched)):
            #起始角度大于已有的终止角度,或终止角度大于已有的起始角度，都表明没有交集，否则就是有交集
            if SAGL > sub_topic_range_bewatched[i][1] or EAGL < sub_topic_range_bewatched[i][0]:
                pass
            else:
                return True
        #所有范围均无交集
        return False


for m in range(TOPIC_RANGE):#单独给每一个话题设定监控区域。
    rand_num_for_item = random.randint(0,Monitor_Count // TOPIC_RANGE * 2)#条目数的期望为监控条目期望整除话题数*2
    monitor_count_real+=rand_num_for_item
    topic = ET.SubElement(monitor_areas,'monitor_topic')
    topic.attrib = {"scale":str(rand_num_for_item),"topic":str(m)}
    #这里要写一层topic+m的标签
    for rnfi in range(rand_num_for_item):
        monitor_area = ET.SubElement(topic,'monitor_item')
        TPC = m  # 话题编号
        SAGL = round(np.random.rand() * 2 * pi, precision)#起始角度，保留设定精度
        EAGL = round(np.random.rand() * 2 * pi, precision)#终止角度，保留设定精度
        #当两个角度代表的范围不正确或与已有的监控范围重叠时，重新设定开始角度与结束角度
        while(right_topic_range_bewatched(TPC,SAGL,EAGL)):
            TPC = m
            SAGL = round(np.random.rand() * 2 * pi, precision)
            EAGL = round(np.random.rand() * 2 * pi, precision)
            pass
        topic_range_bewatched.append([TPC,SAGL,EAGL])
        monitor_area.attrib = {
            "start_angle":str(SAGL),
            "end_angle":str(EAGL),
            "item":str(rnfi+1)
            }
        pass
    pass

#resetTimeSum+=resetTime
monitor_areas.attrib = {
    'Monitor_Count': str(monitor_count_real)
    }#这个要移到最后加上
     #print(resetTimeSum / CYCLE_RANGE)
aa = 'Monitor_Area' + '.xml'
tree.write(aa)

#print(time.time() - start)