from XmlScript.unit_create import unit_maker
from XmlScript.monitor_create import monitor_maker
from XmlScript.advisor_create import advisor_maker
from XmlScript.create_responsibility import responsibility_creator
from XmlScript.create_preference import preference_creator
from XmlScript.connect_ua import ua_linker
from XmlScript.connect_um import um_linker
from XmlScript.connect_uu import uu_linker
class random_starter:
    def __init__(self,um=unit_maker(scale=20),mm=monitor_maker(scale=20),am=advisor_maker(scale=20)):
        self.um=um
        self.mm=mm
        self.am=am
        for i in range(20):
            self.um.make_unit(i)
            self.am.make_advisor(i)
            self.mm.make_monitor(i)
    def init_random(self):
        responsibility_creator().create_responsibility()
        preference_creator().creat_preference()
        ua_linker().link_ua()
        um_linker().link_um()
        uu_linker().link_uu()

if __name__ == '__main__':
    random_starter().init_random()

