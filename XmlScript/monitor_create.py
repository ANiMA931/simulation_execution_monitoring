import xml.etree.ElementTree as ET
import numpy as np

class monitor_maker:
    def __init__(self,scale):
        self.scale=scale
    def make_monitor(self,count):
        root = ET.Element("monitor")
        tree = ET.ElementTree(root)
        commonInformation = ET.SubElement(root, 'commonInformation')
        commonInformation.attrib = {"author": "MA", "remark": "No", "modifyDate": "2019.04.09", "version": "0.0"}
        memberType = ET.SubElement(root, 'memberType')
        memberType.attrib = {"memberRole": "monitor", "memberTypeCode": "3", "MetaModelID": "p-67.258",
                             "ID": "m-" + str(count).zfill(2), "endowment": str(round(np.random.rand()*20, 5))}
        pattern = ET.SubElement(root, 'pattern')
        pattern.attrib = {"path": "C:simulation/patterns/ptn-1.xml"}
        monitoring=ET.SubElement(root,'monitoring')
        monitoring.attrib={"value":""}
        unitList = ET.SubElement(root, 'unitList')
        unitList.attrib = {"scale": ""}
        unitList.text = "\n"

        aa = 'E:\\code\\PycharmProjects\\simulation\\monitors\\' + 'MyCrowd_monitor' + str(count).zfill(2) + '.xml'  # 首先创建一个xml文件，以备描述网络连接情况
        tree.write(aa)
if __name__ == '__main__':
    mm=monitor_maker(scale=20)
    for i in range(mm.scale):
        mm.make_monitor(i)