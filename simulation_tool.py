# cE_simulation_tool.py
'''
本文件是写的界面与后台仿真线程
'''
from defination_read import *
from UI.simulation_exe_Form import Ui_Form  # pyUIC自动生成的pyqt5界面
from members.CN_member import *

from PyQt5 import QtCore, QtGui, QtWidgets  # 一些必要的qt包
import sys  # 线程挂起恢复必要的包
import os  # 必要的包


def format_members_id_role(xml_dom: xml.dom.minidom.Document):
    """
    格式化成员的id与角色，本函数仅用于获取仿真成员xml文件中的部分简单信息包含成员id，成员角色，各类成员的数量
    :param xml_dom: xml文件的dom对象
    :return: key为id与role的dict，成员总个数，primitive成员的数量，collective成员的数量，adviser成员的数量，monitor成员的数量
    """
    root = xml_dom.documentElement  # 获取dom对象的根
    # 初始化id_role字典
    id_role_dict = {
        'id': list(),
        'role': list()
    }
    member_info_labels = root.getElementsByTagName('memberInfo')  # 获取memberInfo标签
    primitive_number = len(root.getElementsByTagName('primitiveInfo'))  # 获取primitiveInfo标签
    collective_number = len(root.getElementsByTagName('collectiveInfo'))  # 获取collectiveInfo标签
    adviser_number = len(root.getElementsByTagName('advisorInfo'))  # 获取advisorInfo标签
    monitorMember_number = len(root.getElementsByTagName('monitorMemberInfo'))  # 获取monitorMemberInfo标签
    for one_member_info_label in member_info_labels:
        id_role_dict['id'].append(one_member_info_label.getAttribute('成员ID'))
        id_role_dict['role'].append(one_member_info_label.getAttribute('成员类型'))
    return id_role_dict, len(
        member_info_labels), primitive_number, collective_number, adviser_number, monitorMember_number


global_attribute_dict = dict()  # 全局属性递推方法
round_methods = dict()  # 轮方法

net_p2p = pd.DataFrame()  # 原子型成员网络
net_p2a = pd.DataFrame()  # 原子型——建议者成员网络
net_p2m = pd.DataFrame()  # 原子型——监控者成员网络
net_p2c = pd.DataFrame()  # 原子型——集合型成员网络
net_c2m = pd.DataFrame()  # 集合型——监控者成员网络
net_c2c = pd.DataFrame()  # 集合型——集合型成员网络

primitives = None  # 原子型单元集合
advisers = None  # 建议者单元集合
monitorMembers = None  # 监控者单元集合
collectives = None  # 集合型单元集合


class uf_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(uf_Form, self).__init__()
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.start_btn_icon = QtGui.QIcon(r'.\UI\播放按钮.ico')
        self.pause_btn_icon = QtGui.QIcon(r'.\UI\暂停.ico')
        stop_btn_icon = QtGui.QIcon(r'.\UI\停止.ico')
        self.start_or_pause_btn.setIcon(self.start_btn_icon)
        self.stop_btn.setIcon(stop_btn_icon)
        self.modify_dateEdit.setDate(QtCore.QDate.currentDate())
        self.members_filedialog_btn.clicked.connect(self.slot_btn_set_members_path)
        self.def_xml_filedialog_btn.clicked.connect(self.slot_btn_set_definition_path)
        self.record_filedialog_btn.clicked.connect(self.slot_btn_set_record_path)

    def slot_btn_set_definition_path(self):
        '''
        读取仿真定义文件路径
        :return:
        '''
        try:
            xml_definition_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择仿真定义xml文件", "./",
                                                                        "XML Files (*.xml);;All Files (*)")
            self.def_xml_path_edit.setText(xml_definition_path[0])
            definition_dom = read_xml(xml_definition_path[0])
            # 注册全局函数成员递推函数
            global global_attribute_dict, round_methods
            global_attribute_dict = register_global_attribute_method(definition_dom)
            round_methods = register_round_method(definition_dom)
            self.service_msg_log_text.append('Read definition from: ')
            self.service_msg_log_text.append(xml_definition_path[0])
        except:
            QtWidgets.QMessageBox.critical(self, "错误", "仿真定义文件错误")
            self.def_xml_path_edit.clear()
            self.service_msg_log_text.append('definition file error. ')
            raise

    def slot_btn_set_members_path(self):
        '''
        读取所有成员的路径的槽函数
        :return:
        '''
        try:
            xml_members_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择仿真成员xml文件", "./",
                                                                     "XML Files (*.xml);;All Files (*)")
            self.members_xml_path_edit.setText(xml_members_path[0])
            # 根据这个路径来读取成员
            member_dom = read_xml(xml_members_path[0])
            # 服务信息更新显示
            self.service_msg_log_text.append('Read member from: ')
            self.service_msg_log_text.append(xml_members_path[0])
            # 解析成员
            global net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c
            net_p2p, net_p2a, net_p2m, net_p2c, net_c2m, net_c2c = net_work_read(member_dom)
            global primitives, advisers, monitorMembers, collectives
            primitives, advisers, monitorMembers, collectives = member_read(member_dom)
            id_role_dict, member_number, p_number, c_number, a_number, m_number = format_members_id_role(member_dom)
            self.reset_member_tableWidget(member_number, id_role_dict)
            self.primitive_num_edit.setText(str(p_number))
            self.adviser_num_edit.setText(str(a_number))
            self.monitor_num_edit.setText(str(m_number))
            self.collective_num_edit.setText(str(c_number))
            self.service_msg_log_text.append("Primitive:{}|Adviser:{}|Monitor:{}|Collective:{}".format(
                p_number, a_number, m_number, c_number
            ))
        except:
            QtWidgets.QMessageBox.critical(self, "错误", "成员生成文件错误")
            self.members_xml_path_edit.clear()
            self.service_msg_log_text.append('member XML file error. ')
            raise

    def reset_member_tableWidget(self, length, id_role_dict):
        self.member_tableWidget.setRowCount(length)
        item = self.member_tableWidget.horizontalHeaderItem(0)
        item.setText(QtCore.QCoreApplication.translate("Form", "Member"))
        item = self.member_tableWidget.horizontalHeaderItem(1)
        item.setText(QtCore.QCoreApplication.translate("Form", "Role"))
        self.member_tableWidget.setHorizontalHeaderItem(1, item)
        temp_arrow = 0
        for id, role in zip(id_role_dict['id'], id_role_dict['role']):
            id_item, role_item = QtWidgets.QTableWidgetItem(), QtWidgets.QTableWidgetItem()
            id_item.setText(QtCore.QCoreApplication.translate("Form", id))
            role_item.setText(QtCore.QCoreApplication.translate("Form", role))
            self.member_tableWidget.setItem(temp_arrow, 0, id_item)
            self.member_tableWidget.setItem(temp_arrow, 1, role_item)
            temp_arrow += 1

    def slot_btn_set_record_path(self):
        '''
        设置仿真结果路径保存的槽函数
        :return:
        '''
        dir_record_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择仿真记录文件夹", os.getcwd())
        if dir_record_path == "":
            print('取消选择')
            return
        else:
            self.record_dir_path_edit.setText(dir_record_path)
            self.service_msg_log_text.append('Set record dictionary to: ')
            self.service_msg_log_text.append(dir_record_path)

    def start_check(self):
        if self.members_xml_path_edit.text() is "" or \
                self.def_xml_path_edit.text() is "" or \
                self.record_dir_path_edit.text() is "" or \
                self.version_edit.text() is "" or\
                self.generation_Edit.text() is "" or\
                self.step_size_Edit.text() is "":
            return False
        else:
            return True


if __name__ == '__main__':
    all_change_time = 2
    for chance_time in range(all_change_time):
        extend_path = input('请输入外部函数文件所在路径：')
        sys.path.append(extend_path)
        try:
            from aa__ import *

            print('外部函数包引用成功')
            break
        except:
            print('外部函数文件路径有误，您还有{}次机会'.format(all_change_time - chance_time - 1))
            if chance_time < all_change_time - 1:
                continue
            else:
                input('错误次数已达上限，请按回车键退出')
                exit(0)
    print(globals()['globalAttribute1'])
    print(globals()['A1']('new init', 1, 3))

    app = QtWidgets.QApplication(sys.argv)
    window = uf_Form()
    window.setWindowTitle('众智网络仿真执行工具软件')
    window.show()

    sys.exit(app.exec_())
