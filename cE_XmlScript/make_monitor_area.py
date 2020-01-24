import random
import xml.etree.ElementTree as ET
import numpy as np

from math import pi


class monitor_area_maker:
    def __init__(self, topic_range=10, monitor_count=20, precision=5):
        self.topic_range = topic_range
        self.monitor_count = monitor_count
        self.precision = precision
        pass

    def make_area(self):
        root = ET.Element("monitor_areas")
        tree = ET.ElementTree(root)
        monitor_areas = ET.SubElement(root, "monitor_area")
        topic_range_bewatched = []
        monitor_count_real = 0

        def right_topic_range_bewatched(tpc, start_angle, end_angle):
            # 起始角度大于终止角度的直接返回
            if start_angle > end_angle:
                return True
            else:
                sub_topic_range_bewatched = []
                # 找出topic相同的子范围,放到sub_topic_range_bewatched里面去
                for i in range(len(topic_range_bewatched)):
                    if tpc == topic_range_bewatched[i][0]:
                        sub_topic_range_bewatched.append([topic_range_bewatched[i][1], topic_range_bewatched[i][2]])
                    else:
                        pass

                # 在已经挑出来的sub_topic_range_bewatched里面计算
                for i in range(len(sub_topic_range_bewatched)):
                    # 起始角度大于已有的终止角度,或终止角度大于已有的起始角度，都表明没有交集，否则就是有交集
                    if start_angle > sub_topic_range_bewatched[i][1] or end_angle < sub_topic_range_bewatched[i][0]:
                        pass
                    else:
                        return True
                # 所有范围均无交集
                return False

        for m in range(self.topic_range):  # 单独给每一个话题设定监控区域。
            rand_num_for_item = random.randint(0, self.monitor_count // self.topic_range * 2)  # 条目数的期望为监控条目期望整除话题数*2
            monitor_count_real += rand_num_for_item
            topic = ET.SubElement(monitor_areas, 'monitor_topic')
            topic.attrib = {"scale": str(rand_num_for_item), "topic": str(m)}
            # 这里要写一层topic+m的标签
            for rnfi in range(rand_num_for_item):
                monitor_area = ET.SubElement(topic, 'monitor_item')
                tpc = m  # 话题编号
                start_angle = round(np.random.rand() * 2 * pi, self.precision)  # 起始角度，保留设定精度
                end_angle = round(np.random.rand() * 2 * pi, self.precision)  # 终止角度，保留设定精度
                # 当两个角度代表的范围不正确或与已有的监控范围重叠时，重新设定开始角度与结束角度
                while (right_topic_range_bewatched(tpc, start_angle, end_angle)):
                    tpc = m
                    start_angle = round(np.random.rand() * 2 * pi, self.precision)
                    end_angle = round(np.random.rand() * 2 * pi, self.precision)
                    pass
                topic_range_bewatched.append([tpc, start_angle, end_angle])
                monitor_area.attrib = {
                    "start_angle": str(start_angle),
                    "end_angle": str(end_angle),
                    "item": str(rnfi + 1)
                }
        monitor_areas.attrib = {
            'Monitor_Count': str(monitor_count_real)
        }  # 这个要移到最后加上
        aa = 'E:\\code\\PycharmProjects\\simulation\\monitorArea\\' + 'Monitor_Area' + '.xml'
        tree.write(aa)


if __name__ == '__main__':
    monitor_area_maker().make_area()
