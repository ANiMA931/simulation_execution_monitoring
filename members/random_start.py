from XmlScript.unit_create import unit_maker
from XmlScript.monitor_create import monitor_maker
from XmlScript.advisor_create import advisor_maker
from XmlScript.create_responsibility import responsibility_creator
from XmlScript.create_preference import preference_creator
from XmlScript.connect_ua import ua_linker
from XmlScript.connect_um import um_linker
from XmlScript.connect_uu import uu_linker
from patterns.pattern import pattern
from tools import *
class random_starter:
    def __init__(self,pattern_dom,um=unit_maker(scale=20),mm=monitor_maker(scale=20),am=advisor_maker(scale=20)):
        self.pattern=pattern(xml_dom=pattern_dom)
        self.um=um
        self.mm=mm
        self.am=am
        for i in range(um.scale):
            self.um.make_unit(i)
        for i in range(am.scale):
            self.am.make_advisor(i)
        for i in range(mm.scale):
            self.mm.make_monitor(i)
    def init_random(self):
        responsibility_creator().create_responsibility()
        preference_creator(self.pattern).creat_preference()
        ua_linker().link_ua()
        um_linker().link_um()
        uu_linker(r'..\units').link_uu()

if __name__ == '__main__':
    pattern_dir=r'..\patterns\pattern1.xml'

    unit_dir=r'..\units'
    advisor_dir=r'..\advisors'
    monitor_dir=r'..\monitors'

    member_dir=r'..\member_xml'

    pattern_dom=read_xml(pattern_dir)
    random_starter(pattern_dom).init_random()

    advisors_name=member_file_name(advisor_dir)
    monitors_name=member_file_name(monitor_dir)
    units_name=member_file_name(unit_dir)

    for name in advisors_name:
        memberdom=read_xml(advisor_dir+'\\\\'+name)
        write_xml(member_dir+'\\\\'+name,memberdom)
    for name in monitors_name:
        memberdom=read_xml(monitor_dir+'\\\\'+name)
        write_xml(member_dir+'\\\\'+name,memberdom)
    for name in units_name:
        memberdom=read_xml(unit_dir+'\\\\'+name)
        write_xml(member_dir+'\\\\'+name,memberdom)


