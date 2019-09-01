import xml.dom.minidom


def read_xml(in_path):
    '''''读取并解析xml文件
       in_path: xml路径
       return: ElementTree'''
    dom = xml.dom.minidom.parse(in_path)
    return dom


def write_xml(path, dom):
    try:
        with open(path, 'w', encoding='UTF-8') as fh:
            dom.writexml(fh)
    except:
        print("error")


class unit:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.resource = float(membertype.getAttribute('resource'))
        efctr = self.root.getElementsByTagName('effector')[0]
        advsrs = self.root.getElementsByTagName('advisor')
        advisors = []
        for i in advsrs:
            a = {"aID": i.getAttribute('aID'), "strength": float(i.getAttribute('strength'))}
            advisors.append(a)
        self.effector = {"endowment": float(efctr.getAttribute('endowment')),
                         "remain": float(efctr.getAttribute('remain')),
                         "scale": int(efctr.getAttribute('scale')), "advisors": advisors}
        dsdr = self.root.getElementsByTagName('decider')[0]
        self.decider = {"depth": int(dsdr.getAttribute('depth')),
                        "selfConfidence": float(dsdr.getAttribute('selfConfidence')),
                        "strategy": dsdr.getAttribute('strategy')}
        exctr = self.root.getElementsByTagName('executor')[0]
        mntrs = self.root.getElementsByTagName('monitor')
        monitors = []
        for i in mntrs:
            a = {"mID": i.getAttribute('mID')}
            monitors.append(a)
        self.executor = {"mutationRate": float(exctr.getAttribute('mutationRate')),
                         "selfDegeneration": float(exctr.getAttribute('selfDegeneration')),
                         "selfDiscipline": float(exctr.getAttribute('selfDiscipline')),
                         "scale": int(exctr.getAttribute('scale')),
                         "monitors": monitors}
        cprtr = self.root.getElementsByTagName('parameter')[0]
        cunts = self.root.getElementsByTagName('cUnit')
        c_units = []
        for i in cunts:
            a = {"uID": i.getAttribute('uID'), "strength": float(i.getAttribute('strength'))}
            c_units.append(a)
        self.parameter = {"endowment": float(cprtr.getAttribute('endowment')),
                          "remain": float(cprtr.getAttribute('remain')),
                          "scale": int(cprtr.getAttribute('scale')), "c_units": c_units}


class advisor:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.endowment = float(membertype.getAttribute('endowment'))
        pfrc = self.root.getElementsByTagName('preference')[0]
        self.preference = pfrc.getAttribute('value').split(',')
        unitList = self.root.getElementsByTagName('unitList')[0]
        us = self.root.getElementsByTagName('unit')
        units = []
        for i in us:
            a = {"uID": i.getAttribute('uID'), "strength": float(i.getAttribute('strength'))}
            units.append(a)
        self.unitList = {"remain": unitList.getAttribute('remaining'), "scale": int(unitList.getAttribute('scale')),
                         "units": units}


class monitor:
    def __init__(self, xml_dom):
        self.root = xml_dom.documentElement
        membertype = self.root.getElementsByTagName('memberType')[0]
        self.id = membertype.getAttribute('ID')
        self.endowment = float(membertype.getAttribute('endowment'))
        rspsblty = self.root.getElementsByTagName('monitoring')[0]
        self.responsibility = rspsblty.getAttribute('value').split(',')
        unitList = self.root.getElementsByTagName('unitList')[0]
        us = self.root.getElementsByTagName('unit')
        units = []
        for i in us:
            a = {"uID": i.getAttribute('uID'), "strength": float(i.getAttribute('strength'))}
            units.append(a)
        self.unitList = {"remain": float(unitList.getAttribute('remaining')),
                         "scale": int(unitList.getAttribute('scale')),
                         "units": units}


if __name__ == '__main__':
    unit = unit(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\units\\MyCrowd_Unit00.xml"))
    advisor = advisor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\advisors\\MyCrowd_advisor00.xml"))
    monitor = monitor(xml_dom=read_xml("E:\\code\\PycharmProjects\\simulation\\monitors\\MyCrowd_monitor01.xml"))
    input()
