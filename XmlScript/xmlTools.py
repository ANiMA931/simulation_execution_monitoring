import xml.etree.ElementTree as ET
import numpy as np
import random

from math import pi


class msg_maker:
    def __init__(self, scale=100, topic_range=10):  # message 的内容包括：话题，角度，强度
        self.scale = scale
        self.topic_range = topic_range

    def make_msg(self):
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        messages = ET.SubElement(root, 'messages')
        messages.attrib = {"scale": str(self.scale)}

        for m in range(self.scale):
            message = ET.SubElement(messages, 'message')
            tpc = random.randint(0, self.topic_range)
            strength = round(np.random.rand(), 5)
            angle = round(np.random.rand() * pi * 2, 5)
            message.attrib = {"ID": "msg-"+str(id(message)), "topic": str(tpc), "strength": str(strength), "angle": str(angle)}

        aa = 'E:\\code\\PycharmProjects\\simulation\\MessAge\\' + 'MyCrowd_MessAge' + '.xml'  # 首先创建一个xml文件，以备描述网络连接情况
        tree.write(aa)


if __name__ == '__main__':
    msg_maker().make_msg()