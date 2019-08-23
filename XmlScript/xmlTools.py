import xml.etree.ElementTree as ET
import numpy as np
import random

from math import pi


class unit_maker:
    def __init__(self, scale=100):  # message 的内容包括：话题，角度，强度
        self.scale = scale

    def make_unit(self):
        root = ET.Element("data")
        tree = ET.ElementTree(root)


        aa = 'E:\\code\\PycharmProjects\\simulation\\Member\\' + 'MyCrowd_Unit' + '.xml'  # 首先创建一个xml文件，以备描述网络连接情况
        tree.write(aa)


if __name__ == '__main__':
    pass