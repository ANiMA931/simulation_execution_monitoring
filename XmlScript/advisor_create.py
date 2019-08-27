import xml.etree.ElementTree as ET
import numpy as np
class advisor_maker:
    def __init__(self, scale=100):
        self.scale = scale

    def make_advisor(self,count):
        root = ET.Element("advisor")
        tree = ET.ElementTree(root)
        commonInformation = ET.SubElement(root, 'commonInformation')
        commonInformation.attrib = {"author": "MA", "remark": "No", "modifyDate": "2019.04.09", "version": "0.0"}
        memberType = ET.SubElement(root, 'memberType')
        memberType.attrib = {"memberRole": "advisor", "memberTypeCode": "2", "MetaModelID": "p-67.258",
                             "ID": "a-" + str(count).zfill(2), "endowment": str(round(np.random.rand()*20, 5))}
        pattern = ET.SubElement(root, 'pattern')
        pattern.attrib = {"path": "C:simulation/patterns/ptn-1.xml"}
        preference=ET.SubElement(root,'preference')
        preference.attrib={"value":""}
        unitList=ET.SubElement(root,'unitList')
        unitList.attrib={"scale":""}
        unitList.text="\n"

        aa = 'E:\\code\\PycharmProjects\\simulation\\advisors\\' + 'MyCrowd_advisor' + str(count).zfill(2) + '.xml'  # 首先创建一个xml文件，以备描述网络连接情况
        tree.write(aa)
if __name__ == '__main__':
    am=advisor_maker(scale=20)
    for i in range(am.scale):
        am.make_advisor(i)