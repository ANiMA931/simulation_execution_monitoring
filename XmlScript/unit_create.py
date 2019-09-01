import xml.etree.ElementTree as ET
import numpy as np
import random


class unit_maker:
    def __init__(self, scale=20):
        self.scale = scale

    def make_unit(self, count):
        root = ET.Element("unit")
        tree = ET.ElementTree(root)
        commonInformation = ET.SubElement(root, 'commonInformation')
        commonInformation.attrib = {"author": "MA", "remark": "No", "modifyDate": "2019.04.09", "version": "0.0"}

        memberType = ET.SubElement(root, 'memberType')
        memberType.attrib = {"memberRole": "unit", "memberTypeCode": "1", "MetaModelID": "p-67.258",
                             "ID": "u-" + str(count).zfill(2), "resource": str(round(random.uniform(2000, 8000), 5))}

        pattern = ET.SubElement(root, 'pattern')
        pattern.attrib = {"path": "C:simulation/patterns/ptn-1.xml"}
        target = ET.SubElement(pattern, 'target')
        target.attrib = {"pID": "p22"}

        now_p = ET.SubElement(pattern, 'now')
        now_p.attrib = {"pID": ""}

        effector = ET.SubElement(root, 'effector')
        e_endowment=np.random.rand() * 20
        effector.attrib = {"endowment": str(round(e_endowment, 5)), "scale": "0","remain":str(round(e_endowment, 5))}
        effector.text = "\n"

        decider = ET.SubElement(root, 'decider')
        decider.attrib = {"selfConfidence": str(round(np.random.rand() * 10, 5)),
                          "depth": str(np.random.randint(0, 10)), "strategy": "normal"}
        decisionList = ET.SubElement(decider, 'decisionList')
        decisionList.attrib = {"scale": "0"}
        decisionList.text = "\n"

        executor = ET.SubElement(root, 'executor')
        executor.attrib = {"selfDiscipline": str(round(np.random.rand() * 10, 5)),
                           "selfDegeneration": str(round(np.random.rand(), 5)), "mutationRate": "0.0005","scale": "0"}
        executor.text = "\n"

        parameter = ET.SubElement(root, 'parameter')
        c_endowment=np.random.rand() * 20
        parameter.attrib = {"endowment": str(round(c_endowment, 5)), "scale": "0","remain":str(round(c_endowment, 5))}
        parameter.text = "\n"
        comment = ET.SubElement(root, "comment")
        comment.text = "default"

        aa = 'E:\\code\\PycharmProjects\\simulation\\units\\' + 'MyCrowd_Unit' + str(
            count).zfill(2) + '.xml'
        tree.write(aa)



if __name__ == '__main__':
    um = unit_maker(scale=20)
    for i in range(um.scale):
        um.make_unit(i)