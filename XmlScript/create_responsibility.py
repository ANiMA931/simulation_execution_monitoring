import numpy as np
from random import shuffle
from tools import *


class responsibility_creator:
    def __init__(self):
        pass

    def create_responsibility(self):
        ptndom = read_xml("E:\\code\\PycharmProjects\\simulation\\patterns\\pattern1.xml")
        responsible_upper = 20
        root = ptndom.documentElement
        behaviors = root.getElementsByTagName('behavior')
        b = []
        for i in range(len(behaviors)):
            b.append((behaviors[i].getAttribute('before'), behaviors[i].getAttribute('after')))
        for i in range(20):
            mntrdom = read_xml(
                "E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(i).zfill(2) + ".xml")
            root = mntrdom.documentElement
            monitoring = root.getElementsByTagName('monitoring')[0]
            shuffle(b)
            responsible_count = np.random.randint(0, responsible_upper)
            v = str(b[0])
            for j in range(1, responsible_count):
                v += "|" + str(b[j])
            monitoring.setAttribute('value', v)
            write_xml("E:\\code\\PycharmProjects\\simulation\\monitors\\" + "MyCrowd_monitor" + str(i).zfill(
                2) + ".xml", mntrdom)


if __name__ == '__main__':
    responsibility_creator().create_responsibility()
