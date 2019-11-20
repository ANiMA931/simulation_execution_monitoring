#connect_uu,py
'''
本文件用于随机连接两个unit，属于前期工具，现已无用
'''
import numpy as np
import pandas as pd
from random import shuffle
import xml.dom.minidom
from my_tools import *
"""与同类相连，该用什么办法呢？
相连的方法是对称的
先把谁会和谁相连写清楚"""
class uu_linker:
    def __init__(self,unit_path):
        self.units_dir=unit_path
        self.units_name=member_file_name(unit_path)
        self.units_id=[]
        for i in self.units_name:
            unitdom=read_xml(self.units_dir+'\\\\'+i)
            root=unitdom.documentElement
            member_type=root.getElementsByTagName('memberType')[0]
            u_id=member_type.getAttribute('ID')
            self.units_id.append(u_id)
        link_matrix=np.zeros((len(self.units_name),len(self.units_name)),dtype=np.int)
        self.link_matrix=pd.DataFrame(link_matrix)
        self.link_matrix.columns=self.units_id
        self.link_matrix.index = self.units_id
        link_strength_matrix=np.zeros((len(self.units_name),len(self.units_name)),dtype=np.float)
        self.link_strength_matrix=pd.DataFrame(link_strength_matrix)
        self.link_strength_matrix.columns=self.units_id
        self.link_strength_matrix.index = self.units_id


    def link_uu(self):
        dom = xml.dom.minidom.Document()
        self.link_matrix_make()

        for i in self.units_name:#对于每个单元
            unitdom = read_xml(self.units_dir+'\\\\'+i)
            '''unitdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\units\\" + "MyCrowd_Unit" + str(i).zfill(2) + ".xml")'''
            root = unitdom.documentElement
            member_type = root.getElementsByTagName('memberType')[0]
            u_id = member_type.getAttribute('ID')
            parameter=root.getElementsByTagName('parameter')[0]
            c_endowment=float(parameter.getAttribute('endowment'))
            remain=self.make_link_strength(u_id,c_endowment)#分配权重并返回剩下的
            parameter.setAttribute('remain',str(round(remain,5)))
            c_scale=0
            for j in self.units_id:
                if self.link_strength_matrix[u_id][j] != 0.0:#有连接关系
                    c_unit=dom.createElement('cUnit')
                    c_unit.setAttribute('uID',str(j))
                    c_unit.setAttribute('strength',str(round(self.link_strength_matrix[u_id][j],5)))
                    parameter.appendChild(c_unit)
                    c_scale+=1
            parameter.setAttribute('scale',str(c_scale))

            write_xml(self.units_dir+'\\\\'+i,unitdom)

    def make_link_strength(self,i,endowment):
        """
        :param i: 想要分配连接关系的成员的下标，此处是成员的ID编号
        :param endowment: 该成员拥有的比较用的连接禀赋
        :return: remain:分配结束后成员的连接禀赋
        """
        remain=endowment
        for j in self.units_id:
            if int(self.link_matrix[i][j])!=0:
                rand_strength=np.random.rand()*remain
                self.link_strength_matrix[i][j]=rand_strength
                remain-=rand_strength
        return remain


    def link_matrix_make(self):
        for i in self.units_id:
            rand_scale=np.random.randint(0,len(self.units_id))
            rand_link=self.units_id.copy()
            shuffle(rand_link)
            rand_link=rand_link[:rand_scale]
            for j in rand_link:
                if self.units_id.index(i)<self.units_id.index(j):
                    self.link_matrix[i][j]=self.link_matrix[j][i]=1

if __name__ == '__main__':
    unit_dir=r'..\units'
    uu=uu_linker(unit_dir)
    uu.link_uu()