#advisor_create.py
'''
本文件用于生成建议者，属于前期生成工具，现已无用
'''
import xml.etree.ElementTree as ET
import numpy as np
class advisor_maker:
    def __init__(self, scale=20):
        self.scale = scale

    def make_advisor(self,count):
        root = ET.Element("advisor")
        tree = ET.ElementTree(root)
        commonInformation = ET.SubElement(root, 'commonInformation')
        commonInformation.attrib = {"author": "MA", "remark": "No", "modifyDate": "2019.04.09", "version": "0.0"}
        memberType = ET.SubElement(root, 'memberType')
        endowment=np.random.rand()*20
        memberType.attrib = {"memberRole": "advisor", "memberTypeCode": "2", "MetaModelID": "p-67.258",
                             "ID": "a-" + str(count).zfill(2), "endowment": str(round(endowment, 5))}
        pattern = ET.SubElement(root, 'pattern')
        pattern.attrib = {"path": "..\patterns\pattern1.xml"}
        preference=ET.SubElement(root,'preference')
        preference.attrib={"value":""}
        unitList=ET.SubElement(root,'unitList')
        unitList.attrib={"scale":"0","remaining":str(round(endowment, 5))}
        unitList.text="\n"

        aa = r'..\advisors' + r'\MyCrowd_advisor' + str(count).zfill(2) + '.xml'
        tree.write(aa)
if __name__ == '__main__':
    am=advisor_maker(scale=100)
    for i in range(am.scale):
        am.make_advisor(i)