# cE_simulation_tool.py
'''
本文件是写的界面与后台仿真线程，目前尚不可用
'''
from UI.coEvolution_child import Ui_Form  # pyUIC自动生成的pyqt5界面
from PyQt5 import QtCore, QtGui, QtWidgets  # 一些必要的qt包
from simulators import cE_simulator  # 自己写的众进化仿真类
import ctypes  # 线程挂起恢复必要的包
import win32con  # 线程挂起恢复必要的包
from win32process import SuspendThread, ResumeThread  # 线程挂起恢复必要的包
import sys  # 线程挂起恢复必要的包
import os  # 必要的包


# 线程类，用于执行仿真计算
class Run_thread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = QtCore.pyqtSignal(float)  # 刷新界面进度条需要用到的信号
    handle = -1  # 线程挂起标志位

    def __init__(self, generation, simulator):  # 迭代数与仿真器对象
        super(Run_thread, self).__init__()
        self.generation = generation
        self.simulator = simulator

    def __del__(self):  # 设置线程停止
        self.wait()

    def run(self):  # 线程运行函数
        try:
            # 设置线程标志位
            self.handle = ctypes.windll.kernel32.OpenThread(win32con.PROCESS_ALL_ACCESS, False,
                                                            int(QtCore.QThread.currentThreadId()))
        except Exception as e:
            print('get thread handle failed', e)
        print('thread id', int(QtCore.QThread.currentThreadId()))

        # 依照仿真迭代数循环执行仿真类中的仿真方法。
        for i in range(self.generation):
            self.simulator.simulate(i)  # 仿真类中的仿真函数
            self._signal.emit(i / self.generation * 100)  # 设置信号，内容为仿真完成的百分比

        self.simulator.make_simulate_result(self.generation)  # 循环结束后生成记录
        self._signal.emit(100.0)
        self.wait()  # 仿真结束设置线程状态


# 界面类，用于显示界面
class CE_simulation_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(CE_simulation_Form, self).__init__()
        self.setupUi(self)
        self.thread = None  # 初始化线程
        # 将事件与槽函数绑定
        self.units_filedialog_btn.clicked.connect(self.slot_btn_set_units_path)
        self.record_filedialog_btn.clicked.connect(self.slot_btn_set_record_path)
        sp_btn_icon=QtGui.QIcon(r'E:\code\PycharmProjects\simulation\UI\播放按钮.ico')
        stop_btn_icon=QtGui.QIcon(r'E:\code\PycharmProjects\simulation\UI\停止.ico')
        self.start_or_pause_btn.setIcon(sp_btn_icon)
        self.stop_btn.setIcon(stop_btn_icon)
        # 仿真运行状态初始化
        self.run_status = False
        # 仿真器初始化
        self.simulator = None
        # 绑定仿真槽函数
        self.start_or_pause_btn.clicked.connect(self.slot_btn_start_simulate)
        # 绑定停止仿真槽函数
        self.stop_btn.clicked.connect(self.slot_btn_stop_simulate)
        pass

    def slot_btn_set_units_path(self):
        '''
        读取units的路径的槽函数
        :return:
        '''
        dir_units_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择原子型成员文件夹", os.getcwd())
        if dir_units_path == "":
            print('取消选择')
            return
        else:
            self.units_dir_path.setText(dir_units_path)

    def slot_btn_set_advisors_path(self):
        '''
        读取建议者的槽函数
        :return:
        '''
        dir_advisor_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择建议者成员文件夹", os.getcwd())
        if dir_advisor_path == "":
            print('取消选择')
            return
        else:
            self.advisor_dir_path.setText(dir_advisor_path)

    def slot_btn_set_monitors_path(self):
        '''
        读取监控者的槽函数
        :return:
        '''
        dir_monitors_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择监控者成员文件夹", os.getcwd())
        if dir_monitors_path == "":
            print('取消选择')
            return
        else:
            self.monitor_dir_path.setText(dir_monitors_path)

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
            self.record_dir_path.setText(dir_record_path)

    def slot_btn_start_simulate(self):
        '''
        开始或暂停仿真的槽函数
        :return: no return
        '''
        # 该判断条件是界面尚未初始化线程且仿真状态为False即未运行。
        if not self.run_status and self.thread is None:
            # 更改button上的图标
            self.start_or_pause_btn.setIcon(self.pause_icon)
            # 更改仿真状态为运行
            self.run_status = True
            # 由于路径中的成员有可能会出错，所以要try
            try:
                # 初始化仿真器，仿真器需要传入三种成员的路径与仿真结果记录的路径，目前已经改为一个路径
                self.simulator = cE_simulator(self.units_dir_path.text(), self.advisor_dir_path.text(),
                                              self.monitor_dir_path.text(), self.record_dir_path.text())
                # 初始化线程，需要传入仿真迭代数与仿真器对象
                self.thread = Run_thread(int(self.generation_lineEdit.text()), self.simulator)
                # 绑定线程的信号函数
                self.thread._signal.connect(self.call_back_bar)
                # 绑定线程的结束函数（其实这个函数是所查到的资料中包含的，未知上述理解是否正确）
                self.thread.finished.connect(self.thread.deleteLater)
                # 进程开始
                self.thread.start()
            except:
                print("members' path error.")
        # 该判断条件是仿真状态为未运行（False）但已初始化了线程（即暂停仿真状态）
        elif not self.run_status and self.thread is not None:  # 恢复线程
            # 判断异常
            if self.thread.handle == -1:
                return print('handle is wrong')
            # 继续线程
            ret = ResumeThread(self.thread.handle)
            ##重设按键图标
            self.start_or_pause_btn.setIcon(self.pause_icon)
            # 输出查看结果
            print('恢复线程', self.thread.handle, ret)
            # 重设仿真标志位
            self.run_status = True
        # 最后的判断是仿真状态为运行（True）的时候
        else:
            if self.thread.handle == -1:
                return print('handle is wrong')
            # 挂起线程
            ret = SuspendThread(self.thread.handle)
            print('挂起线程', self.thread.handle, ret)
            # 重设图标
            self.start_or_pause_btn.setIcon(self.start_icon)
            # 更改仿真状态
            self.run_status = False

    def slot_btn_stop_simulate(self):
        '''
        停止仿真槽函数
        :return: no return
        '''
        # 线程未初始化时直接返回
        if self.thread is None:
            return
        # 线程已初始化后
        else:
            # 终止线程
            del self.simulator
            ret = ctypes.windll.kernel32.TerminateThread(self.thread.handle, 0)
            print('终止线程', self.thread.handle, ret)
            self.thread = None
            self.simulator = None
            self.run_status = False
            self.start_or_pause_btn.setIcon(self.start_icon)

    def call_back_bar(self, msg):
        '''
        信号函数，用于显示界面上的进度条
        :param msg: 线程类的run()函数中的emit()函数的参数
        :return:
        '''
        # 设置新值
        self.exe_progress_bar.setValue(msg)
        # 若仿真已经到达100%
        if msg == 100.0:
            #将仿真器与线程移除，重设运行状态为False
            del self.simulator
            del self.thread
            self.simulator = None
            self.run_status = False
            self.start_or_pause_btn.setIcon(self.start_icon)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CE_simulation_Form()
    window.setWindowTitle('simulation execution')
    window.show()
    sys.exit(app.exec_())
