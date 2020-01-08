# simulation_exe_tools.py
'''
该文件是总的仿真界面，是整个项目的程序入口
'''
from UI.coEvolution_exe import Ui_MainWindow  # 用pyUIC生成的界面类
from cE_simulation_tool import CE_simulation_Form  # 自己写的某类仿真的界面
from my_tools import *  # 自己写的一些必要的工具
from PyQt5 import QtCore, QtGui, QtWidgets  # pyqt5必要的一些组件
import sys  # 运行界面必要的包


# 主界面类
class main_exe_window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_exe_window, self).__init__()
        self.setupUi(self)
        # 绑定菜单栏action的事件槽函数
        self.action_XML.triggered.connect(self.slot_open_simu_def_XML)

    def slot_open_simu_def_XML(self):
        '''
        读取仿真定义xml文件槽函数
        :return:
        '''
        # 通过fileDialog读取文件的路径与名字
        simu_def_XML_path = QtWidgets.QFileDialog.getOpenFileName(self, '选择仿真定义文件')
        # 获取仿真定义文件中的仿真类型代码
        simulation_code = self.read_simulation_def_meta_model_code(simu_def_XML_path[0], 'simulationExecutionTypeCode')
        # 进行代码比对，由于目前只开发了一种仿真，所以只有一种
        # 此处的下方就是仿真大循环要写的位置。
        
        if simulation_code == 'CE':
            # 读取成功后在预留的布局上添加widget，但首先要移除旧widget
            self.simulation_widget_layout.removeWidget(self.simulation_widget)
            # 初始化新的widget
            self.simulation_widget = CE_simulation_Form()
            # 添加新的widget到布局上
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
            return print('wrong simulation type code.')

    def read_simulation_def_meta_model_code(self, path, nameStr):
        '''
        此处写读取解析xml文件的代码，读取仿真类型代号对应的内容放到simulation_code中
        :param path:文件路径
        :param nameStr: 需要读取的xml文件中的标签名
        :return: 仿真类型代号
        '''
        # 通过路径读取整个xml文件为一个dom
        dom = read_xml(path)
        # 拿到xml文件的根标签
        root = dom.documentElement
        # 拿到对应名称的标签，由于返回类型是list，所以取第一个
        item = root.getElementsByTagName(nameStr)[0]
        # 返回标签的text
        return item.firstChild.data


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = main_exe_window()
    window.show()
    sys.exit(app.exec_())
