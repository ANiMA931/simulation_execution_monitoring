from UI.coEvolution_child import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from simulators import cE_simulator
import ctypes
import win32con
from win32process import SuspendThread, ResumeThread
import sys
import os


class Run_thread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = QtCore.pyqtSignal(float)
    handle = -1

    def __init__(self, generation, simulator):
        super(Run_thread, self).__init__()
        self.generation = generation
        self.simulator = simulator

    def __del__(self):
        self.wait()

    def run(self):
        try:
            # 这个目前我没弄明白这里写法
            self.handle = ctypes.windll.kernel32.OpenThread(win32con.PROCESS_ALL_ACCESS, False,
                                                            int(QtCore.QThread.currentThreadId()))
        except Exception as e:
            print('get thread handle failed', e)
        print('thread id', int(QtCore.QThread.currentThreadId()))

        for i in range(self.generation):
            self.simulator.simulate(i)
            self._signal.emit(i / self.generation * 100)  # 注意这里与_signal = pyqtSignal(str)中的类型相同

        self.simulator.make_simulate_result(self.generation)
        self._signal.emit(100.0)
        self.wait()


class CE_simulation_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self, name='cEsimulation'):
        super(CE_simulation_Form, self).__init__()
        self.setWindowTitle(name)
        self.setupUi(self)
        self.thread = None  # 初始化线程
        # 将事件与槽函数绑定
        self.units_filedialog_btn.clicked.connect(self.slot_btn_set_units_path)
        self.advisor_filedialog_btn.clicked.connect(self.slot_btn_set_advisors_path)
        self.monitor_filedialog_btn.clicked.connect(self.slot_btn_set_monitors_path)
        self.record_filedialog_btn.clicked.connect(self.slot_btn_set_record_path)
        self.run_status = False
        self.simulator = None
        self.start_or_pause_btn.clicked.connect(self.slot_btn_start_simulate)
        self.stop_btn.clicked.connect(self.slot_btn_stop_simulate)
        pass

    def slot_btn_set_units_path(self):
        dir_units_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择原子型成员文件夹", os.getcwd())
        if dir_units_path == "":
            print('取消选择')
            return
        else:
            self.units_dir_path.setText(dir_units_path)

    def slot_btn_set_advisors_path(self):
        dir_advisor_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择建议者成员文件夹", os.getcwd())
        if dir_advisor_path == "":
            print('取消选择')
            return
        else:
            self.advisor_dir_path.setText(dir_advisor_path)

    def slot_btn_set_monitors_path(self):
        dir_monitors_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择监控者成员文件夹", os.getcwd())
        if dir_monitors_path == "":
            print('取消选择')
            return
        else:
            self.monitor_dir_path.setText(dir_monitors_path)

    def slot_btn_set_record_path(self):
        dir_record_path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择仿真记录文件夹", os.getcwd())
        if dir_record_path == "":
            print('取消选择')
            return
        else:
            self.record_dir_path.setText(dir_record_path)

    def slot_btn_start_simulate(self):
        if not self.run_status and self.thread is None:
            self.start_or_pause_btn.setIcon(self.pause_icon)
            self.run_status = True
            try:
                self.simulator = cE_simulator(self.units_dir_path.text(), self.advisor_dir_path.text(),
                                              self.monitor_dir_path.text(), self.record_dir_path.text())
                self.thread = Run_thread(int(self.generation_lineEdit.text()), self.simulator)
                self.thread._signal.connect(self.call_back_bar)
                self.thread.finished.connect(self.thread.deleteLater)
                self.thread.start()
            except:
                print("members' path error.")

        elif not self.run_status and self.thread is not None:  # 恢复线程
            if self.thread.handle == -1:
                return print('handle is wrong')

            ret = ResumeThread(self.thread.handle)
            self.start_or_pause_btn.setIcon(self.pause_icon)
            print('恢复线程', self.thread.handle, ret)
            self.run_status = True
        else:
            if self.thread.handle == -1:
                return print('handle is wrong')

            ret = SuspendThread(self.thread.handle)
            print('挂起线程', self.thread.handle, ret)
            self.start_or_pause_btn.setIcon(self.start_icon)
            self.run_status = False

    def slot_btn_stop_simulate(self):
        if self.thread is None:
            return
        else:
            ret = ctypes.windll.kernel32.TerminateThread(self.thread.handle, 0)
            print('终止线程', self.thread.handle, ret)
            self.thread=None
            del self.simulator
            self.simulator = None
            self.run_status = False
            self.start_or_pause_btn.setIcon(self.start_icon)

    def call_back_bar(self, msg):
        self.exe_progress_bar.setValue(msg)
        if msg == 100.0:
            del self.thread
            del self.simulator
            self.simulator=None
            self.run_status=False
            self.start_or_pause_btn.setIcon(self.start_icon)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = CE_simulation_Form('cE_simulation')
    window.show()
    sys.exit(app.exec_())
