# -*- coding: utf-8 -*-
"""
生成一个xml文件,以描述100个网络成员之间的连接关系
100个成员用100个ID表示，连接关系为100*100的连接矩阵，描述建议关系，
由i到j与由j到i的建议权值不同，因此该矩阵关于对角线非对称
"""
import random
import string
import xml.etree.ElementTree as ET
import numpy as np

root = ET.Element("data")  # 创建根节点
tree = ET.ElementTree(root)

Nodes_Group = []  # Nodes_Group用来存储节点名称
for i in range(100):
    Nodes_Group.append([])  # Nodes_Group规模100

# for i in range(10):
#     for j in range(10):
#         Nodes_Group[i*10+j]='Node'+str(i)+str(j)#Nodes_Group每一个索引存储Nodeij
for i in range(100):
    Nodes_Group[i] = 'Node'+str(i)
Node01 = ET.SubElement(root, "Nodes")  # 网络节点

Rand_A = np.random.rand(100, 100)  # 根据给定维度生成[0,1)之间的数据，包含0，不包含1
Node02 = ET.SubElement(root, "Matrix_link")  # 连接矩阵

aa = 'MyCrowd_Network'+'.xml'  # 首先创建一个xml文件，以备描述网络连接情况
tree.write(aa)

for k in range(100):
    Nodes = root.find("Nodes")
    Nodes.set(Nodes_Group[k], '200.100.01.'+str(k))  # 以set的方式追加Nodes属性
    # set只能对已有的节点进行属性设置及追加，因此前文必须先创建xml文件。


for i in range(100):
    for j in range(100):
        if i != j:
            link = round(Rand_A[i][j], 2)
            Matr = root.find("Matrix_link")
            Matr.set(Nodes_Group[i]+'-'+Nodes_Group[j],
                     str(link))  # 以set的方式追加Matrix_link属性
        else:#矩阵方式存储不能避免自连，所以设定为固定值0
            link = 0.0
            Matr = root.find("Matrix_link")
            Matr.set(Nodes_Group[i]+'-'+Nodes_Group[j],
                     str(link))  # 以set的方式追加Matrix_link属性


aa = 'MyCrowd_Network'+'.xml'  # 重写xml文件
tree.write(aa)
