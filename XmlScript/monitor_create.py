#monitor_create.py
'''
本文件用于生成监控者xml，前期工具，现已无用
'''
import xml.etree.ElementTree as ET
import numpy as np

class monitor_maker:
    def __init__(self,scale=20):
        self.scale=scale
    def make_monitor(self,count):
        root = ET.Element("monitor")
        tree = ET.ElementTree(root)
        commonInformation = ET.SubElement(root, 'commonInformation')
        commonInformation.attrib = {"author": "MA", "remark": "No", "modifyDate": "2019.04.09", "version": "0.0"}
        memberType = ET.SubElement(root, 'memberType')
        endowment=round(np.random.rand()*20, 5)
        memberType.attrib = {"memberRole": "monitor", "memberTypeCode": "3", "MetaModelID": "p-67.258",
                             "ID": "m-" + str(count).zfill(2), "endowment": str(endowment)}
        pattern = ET.SubElement(root, 'pattern')
        pattern.attrib = {"path": ".\patterns\pattern1.xml"}
        monitoring=ET.SubElement(root,'monitoring')
        monitoring.attrib={"value":""}
        unitList = ET.SubElement(root, 'unitList')
        unitList.attrib = {"scale": "0","remaining":str(endowment)}
        unitList.text = "\n"

        aa = r'..\monitors' + r'\MyCrowd_monitor' + str(count).zfill(2) + '.xml'  # 首先创建一个xml文件，以备描述网络连接情况
        tree.write(aa)
if __name__ == '__main__':
    mm=monitor_maker(scale=100)
    for i in range(mm.scale):
        mm.make_monitor(i)