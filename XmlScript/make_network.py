import xml.etree.ElementTree as ET
import numpy as np

class network_maker:
    def __init__(self,net_scale=100):
        self.net_scale=net_scale
    def make_network(self):
        root = ET.Element("data")  # 创建根节点
        tree = ET.ElementTree(root)

        Nodes_Group = []  # Nodes_Group用来存储节点名称
        for i in range(self.net_scale):
            Nodes_Group.append([])  # Nodes_Group规模100

        for i in range(self.net_scale//10):
            for j in range(10):
                Nodes_Group[i*10+j]='Node'+str(i)+str(j)#Nodes_Group每一个索引存储Nodeij
        # for i in range(self.net_scale):
        #     Nodes_Group[i] = 'Node' + str(i)
        Node01 = ET.SubElement(root, "Nodes")  # 网络节点

        Rand_A = np.random.rand(self.net_scale, self.net_scale)  # 根据给定维度生成[0,1)之间的数据，包含0，不包含1
        Node02 = ET.SubElement(root, "Matrix_link")  # 连接矩阵

        aa = 'MyCrowd_Network' + '.xml'  # 首先创建一个xml文件，以备描述网络连接情况
        tree.write(aa)

        for k in range(self.net_scale):
            Nodes = root.find("Nodes")
            Nodes.set(Nodes_Group[k], '200.100.01.' + str(k))  # 以set的方式追加Nodes属性
            # set只能对已有的节点进行属性设置及追加，因此前文必须先创建xml文件。

        for i in range(self.net_scale):
            for j in range(self.net_scale):
                if i != j:
                    link = round(Rand_A[i][j], 2)
                    Matr = root.find("Matrix_link")
                    Matr.set(Nodes_Group[i] + '-' + Nodes_Group[j],
                             str(link))  # 以set的方式追加Matrix_link属性
                else:  # 矩阵方式存储不能避免自连，所以设定为固定值None
                    link = None
                    Matr = root.find("Matrix_link")
                    Matr.set(Nodes_Group[i] + '-' + Nodes_Group[j],
                             str(link))  # 以set的方式追加Matrix_link属性

        aa = 'MyCrowd_Network' + '.xml'  # 重写xml文件
        tree.write(aa)
if __name__ == '__main__':
    network_maker(net_scale=50).make_network()