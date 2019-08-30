import numpy as np
from random import shuffle
import xml.dom.minidom

class responsibility_creator:
    def __init__(self):
        pass
    def create_responsibility(self):
        def read_xml(in_path):
            '''''读取并解析xml文件
               in_path: xml路径
               return: ElementTree'''
            dom = xml.dom.minidom.parse(in_path)
            return dom

        ptndom = read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml")
        responsible_upper = 20
        root = ptndom.documentElement
        behaviors = root.getElementsByTagName('behavior')
        b = []
        for i in range(len(behaviors)):
            b.append(behaviors[i].getAttribute('bID'))
        for i in range(20):
            mntrdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(i).zfill(2) + ".xml")
            root = mntrdom.documentElement
            monitoring = root.getElementsByTagName('monitoring')
            shuffle(b)
            responsible_count = np.random.randint(0, responsible_upper)
            v = b[0]
            for i in range(1, responsible_count):
                v += "," + b[i]
            monitoring[0].setAttribute('value', v)
            try:
                with open("E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(i).zfill(
                        2) + ".xml", 'w', encoding='UTF-8') as fh:
                    mntrdom.writexml(fh)
            except:
                print("error")
if __name__ == '__main__':
    responsibility_creator().create_responsibility()