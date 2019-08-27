import numpy as np
from random import shuffle
import xml.dom.minidom

def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    dom=xml.dom.minidom.parse(in_path)
    return dom

positions=np.zeros((24,24),dtype=np.float)

ptndom=read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml")
root=ptndom.documentElement
position=root.getElementsByTagName('position')
behaviors=root.getElementsByTagName('behavior')
for i in range(len(behaviors)):
    before=int(str(behaviors[i].getAttribute('before')).replace('p',''))
    after=int(str(behaviors[i].getAttribute('after')).replace('p',''))
    positions[before][after]=float(behaviors[i].getAttribute('weight'))
print(positions)
def make_preference(positions):
    startList=[0,1,2]
    shuffle(startList)
    start=startList[0]
    p=[start]
    while positions[start].any()!=0:
        temp=list(positions)
        gate=[]
        for i in range(24):
            if temp[start][i]!=0:
                gate.append(i)
        shuffle(gate)
        start=gate[0]
        p.append(start)
    pfrc="p"+str(p[0])
    for i in range(1,len(p)):
        pfrc+=",p"+str(p[i])
    return pfrc
for i in range(20):
    advsrdom=read_xml("E:\\code\\PycharmProjects\\simulation\\advisors\\"+"MyCrowd_advisor" + str(i).zfill(2)+".xml")
    root=advsrdom.documentElement
    preference=root.getElementsByTagName('preference')
    pfrc=make_preference(positions)
    print(pfrc)
    preference[0].setAttribute('value',pfrc)
    try:
        with open("E:\\code\\PycharmProjects\\simulation\\advisors\\"+"MyCrowd_advisor" + str(i).zfill(2)+".xml",'w',encoding='UTF-8') as fh:
            advsrdom.writexml(fh)
    except:
        print("error")
