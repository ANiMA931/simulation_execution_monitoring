import numpy as np
from random import shuffle
import xml.dom.minidom
"""与同类相连，该用什么办法呢？
相连的方法是对称的
先把谁会和谁相连写清楚"""
class uu_linker:
    def __init__(self,link_matrix=np.zeros((20, 20), dtype=np.int),link_strength_matrix=np.zeros((20, 20), dtype=np.float)):
        self.link_matrix=link_matrix
        self.link_strength_matrix=link_strength_matrix


    def link_uu(self):
        def read_xml(in_path):
            '''''读取并解析xml文件
               in_path: xml路径
               return: ElementTree'''
            dom = xml.dom.minidom.parse(in_path)
            return dom

        dom = xml.dom.minidom.Document()
        self.link_matrix_make()
        for i in range(20):#对于每个单元
            unitdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml")
            root = unitdom.documentElement
            '''目前写到了这里，下面的目标是把xml解析出来，然后给它分配连接权重，连接权重分配完了还要把连接关系写回到xml里面，最后保存'''
            parameter=root.getElementsByTagName('parameter')[0]

            c_endowment=float(parameter.getAttribute('endowment'))
            remain=self.make_link_strength(i,c_endowment)#分配权重并返回剩下的
            parameter.setAttribute('remain',str(round(remain,5)))
            c_scale=0
            for j in range(20) :
                if self.link_strength_matrix[i][j] != 0.0:#有连接关系
                    c_unit=dom.createElement('cUnit')
                    c_unit.setAttribute('uID','u-'+str(j).zfill(2))
                    c_unit.setAttribute('strength',str(round(self.link_strength_matrix[i][j],5)))
                    parameter.appendChild(c_unit)
                    c_scale+=1
            parameter.setAttribute('scale',str(c_scale))

            try:
                with open("E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml",
                          'w',
                          encoding='UTF-8') as fh:
                    unitdom.writexml(fh)
            except:
                print("error")

    def make_link_strength(self,i,endowment):
        """
        :param i: 想要分配连接关系的成员的下标，此处是成员的ID编号
        :param endowment: 该成员拥有的比较用的连接禀赋
        :return: remain:分配结束后成语的连接禀赋
        """
        remain=endowment
        for j in range(20):
            if int(self.link_matrix[i][j])!=0:
                rand_strength=np.random.rand()*remain
                self.link_strength_matrix[i][j]=rand_strength
                remain-=rand_strength
        return remain


    def link_matrix_make(self):
        for i in range(20):
            rand_scale=np.random.randint(0,20)
            rand_link=list(range(0,20))
            shuffle(rand_link)
            rand_link=rand_link[:rand_scale]
            for j in rand_link:
                if i<j:
                    self.link_matrix[i][j]=self.link_matrix[j][i]=1

if __name__ == '__main__':
    uu=uu_linker()
    uu.link_uu()