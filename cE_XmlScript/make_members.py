import random
from math import pi
import xml.etree.ElementTree as ET
import numpy as np


class member_maker:
    def __init__(self, member_num=100):
        self.member_num = member_num

    def make_members(self):
        Network = ET.parse(
            "E:\\code\\PycharmProjects\\simulation\\NetWorkXml\\MyCrowd_Network.xml")  # 读取MyCrowd_Network.xml文件
        Network_root = Network.getroot()  # 获得Network的根节点
        Nodes = Network_root.find("Nodes")  # 获得Network的Nodes元素

        # acc = Nodes.tag#获取标签名
        ac = Nodes.attrib  # Nodes属性为一个字典型
        # ad=sorted(ac.keys())[3]#sorted函数按key值对字典排序
        # for key in ac: #查看字典型变量的全部关键字和值
        #    print(key)
        #    print(ac[key])
        Matr = Network_root.find("Matrix_link")  # 获得Network的Nodes元素
        am = Matr.attrib  # Nodes属性为一个字典型
        amm = sorted(am.keys())[155]  # 索引规律为Nodei-Nodej,['i''j']#没看出来这句话有啥用啊

        GroupXml = []  # GroupXml来存放一系列xml文件的名
        for i in range(self.member_num):
            GroupXml.append([])

        for i in range(self.member_num):
            GroupXml[i] = 'MyCrowd_Primitive' + str(i).zfill(2)  # MyCrowd_Primitivei来命名xml文件名，给两个位

        # 创建根节点
        # resetTime=0 #重复设定连接关系的次数
        for k in range(self.member_num):
            root = ET.Element("data")  # 根节点为data
            tree = ET.ElementTree(root)
            # 以根节点为父节点，设定子节点modelInformation。
            node_model_information = ET.SubElement(root, "modelInformation")
            node_model_information.attrib = {"version": '0.0',
                                             "modifyDate": '2019.04',
                                             "author": "MA",
                                             "comment": "No"}  # modelInformation设定属性version、modifyDate、author、comment
            member_type = ET.SubElement(root, "memberType")  # 以根节点为父节点，设定子节点memberType
            # memberType设定属性memberRole与memberTypeCode
            member_type.attrib = {"memberRole": 'Primitive', "memberTypeCode": '1'}
            # 在子节点memberType中设定子节点memberInformation
            node_member_information = ET.SubElement(member_type, "memberInformation")
            name = sorted(ac.keys())[k]  # sorted函数按key值对字典排序
            ESS = 10  # 信息存储禀赋
            EGE = 10  # 信息浏览禀赋
            node_member_information.attrib = {"name": name,
                                              "ID": ac[name],  # 查字典，得name对应的ID
                                              # 存储一下信息存储禀赋
                                              "Es_informationStorage": str(ESS),
                                              # 存储一下信息浏览禀赋
                                              "Eg_informationExplor": str(EGE),
                                              }
            node_ms_information_storage = ET.SubElement(
                root, "Ms_informationStorage")  # 信息存储
            for n in range(ESS):  # 信息存储禀赋来决定
                node_ms_information_storage_sub = ET.SubElement(
                    node_ms_information_storage, 'message' + str(n))  # 逐条信息
                AGL = round(np.random.rand() * 2 * pi, 2)  # 话题偏好，保留两位小数,取值范围0-2π
                FLD = np.random.randint(0, 10)  # 话题编号，0-10之间的随机整数，含0不含10
                STL = round(np.random.rand(), 2)  # 信息强度，保留两位小数
                node_ms_information_storage_sub.attrib = {"field": str(FLD),
                                                          "angle": str(AGL),
                                                          "strenth": str(STL)}

            node_variables = ET.SubElement(root, "Variables")  # 要用到的变量
            tg = round(random.uniform(0.5, 1), 2)  # 群发阈值，保留两位小数,范围(-1,1),
            # 不过-1开始取未免也太低了，至少也得是个0.4或者0.5的吧
            tf = round(random.uniform(0, tg), 2)  # 转发阈值,该阈值小于群发阈值，保留两位小数
            tc = round(random.uniform(-0.5, tf), 2)  # 改变强度阈值，该阈值小于转发阈值，保留两位小数
            tn = round(random.uniform(-1, tc), 2)  # 改变结构阈值，该阈值小于改变强度阈值，保留两位小数
            node_variables.attrib = {"Tf": str(tf),
                                     "Tg": str(tg),
                                     "Tc": str(tc),
                                     "Tn": str(tn),
                                     "Othervariable": '0'}
            node_neighbor = ET.SubElement(root, "Neighbor")  # 根节点为父节点,邻居
            node_be_advised = ET.SubElement(node_neighbor, "BeAdvised")  # 上家
            node_to_advising = ET.SubElement(node_neighbor, "ToAdvising")  # 下家

            aa = 'E:\\code\\PycharmProjects\\simulation\\primitive\\' + GroupXml[k] + '.xml'
            tree.write(aa)

            # 考虑到随机数是自己的特殊情况，算法一套流程下来自连概率为十分之一。
            BAs = np.random.randint(0, 100, size=10)  # 0-100之间的随机整数，10个上家邻居
            # BAs = [k] #先将k放到BAs的第一个位置

            while k in BAs:
                BAs = np.random.randint(0, 100, size=10)  # 如果k被随机函数选中说明随机到了本体，需要再次随机选
                # resetTime+=1#测试一下会重复几次
            for n in range(10):
                Nodes = root.find("Neighbor")
                Nodes = Nodes.find("BeAdvised")
                # 以set的方式追加Nodes属性，由于第一个位置是本节点编号k，所以要后移一个开始
                Nodes.set('BeAdvised' + str(n), 'Node' + str(BAs[n]))
                # set只能对已有的节点进行属性设置及追加，因此前文必须先创建xml文件。

            TAs = np.random.randint(0, 100, size=10)  # 0-100之间的随机整数，10个下家邻居

            while k in TAs:
                TAs = np.random.randint(0, 100, size=10)  # 如果k被随机函数选中说明随机到了本体，需要再次随机选
                # resetTime+=1# 测试一下会重复几次
            for n in range(10):
                Nodes = root.find("Neighbor")
                Nodes = Nodes.find("ToAdvising")
                Nodes.set('ToAdvising' + str(n), 'Node' + str(TAs[n]))  # 以set的方式追加Nodes属性
                # set只能对已有的节点进行属性设置及追加，因此前文必须先创建xml文件。
            aa = 'E:\\code\\PycharmProjects\\simulation\\primitive\\' + GroupXml[k] + '.xml'
            tree.write(aa)


if __name__ == '__main__':
    member_maker(member_num=50).make_members()
