from UI.coEvolution_exe import Ui_MainWindow
from cE_simulation_tool import CE_simulation_Form
from tools import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os


class main_exe_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_exe_window, self).__init__()
        self.setupUi(self)
        self.action_XML.triggered.connect(self.slot_open_simu_def_XML)

    def slot_open_simu_def_XML(self):
        simu_def_XML_path = QtWidgets.QFileDialog.getOpenFileName(self, '选择仿真定义文件')
        simulation_code = self.read_simulation_def_meta_model_code(simu_def_XML_path[0], 'simulationExecutionTypeCode')
        if simulation_code == 'CE':
            self.simulation_widget_layout.removeWidget(self.simulation_widget)
            self.simulation_widget=CE_simulation_Form()
            self.simulation_widget_layout.addChildWidget(self.simulation_widget)
            pass
        elif simulation_code == 'b':
            print("11111")
            pass
        elif simulation_code == 'c':
            pass
        elif simulation_code == 'd':
            print("11111")
            pass
        elif simulation_code == 'e':
            pass
        elif simulation_code == 'f':
            print("11111")
            pass
        elif simulation_code == 'g':
            pass
        else:
            print('wrong simulation type code.')

    def read_simulation_def_meta_model_code(self, path, nameStr):
        # 此处写读取解析xml文件的代码，读取仿真类型代号对应的内容放到simulation_code中
        dom = read_xml(path)
        root = dom.documentElement
        item = root.getElementsByTagName(nameStr)[0]
        return item.firstChild.data


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = main_exe_window()
    window.show()
    sys.exit(app.exec_())
