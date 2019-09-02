import numpy as np
from random import shuffle
from tools import *


class preference_creator:
    def __init__(self):
        pass

    def creat_preference(self):
        positions = np.zeros((25, 25), dtype=np.float)

        ptndom = read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml")
        root = ptndom.documentElement
        behaviors = root.getElementsByTagName('behavior')
        for i in range(len(behaviors)):
            before = int(str(behaviors[i].getAttribute('before')).replace('p', ''))
            after = int(str(behaviors[i].getAttribute('after')).replace('p', ''))
            positions[before][after] = float(behaviors[i].getAttribute('weight'))

        def make_preference(positions):
            startList = [0, 1, 2]
            shuffle(startList)
            start = startList[0]
            p = [start]
            while positions[start].any() != 0:
                temp = list(positions)
                gate = []
                for i in range(24):
                    if temp[start][i] != 0:
                        gate.append(i)
                shuffle(gate)
                start = gate[0]
                p.append(start)
            pfrc = "p" + str(p[0])
            for i in range(1, len(p)):
                pfrc += ",p" + str(p[i])
            return pfrc

        for i in range(20):
            advsrdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\advisors\\" + "MyCrowd_advisor" + str(i).zfill(2) + ".xml")
            root = advsrdom.documentElement
            preference = root.getElementsByTagName('preference')
            pfrc = make_preference(positions)
            preference[0].setAttribute('value', pfrc)
            write_xml("E:\\code\\PycharmProjects\\simulation\\advisors\\" + "MyCrowd_advisor" + str(i).zfill(
                2) + ".xml", advsrdom)


if __name__ == '__main__':
    preference_creator().creat_preference()
