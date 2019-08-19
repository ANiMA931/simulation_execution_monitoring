from UI.simulation_exe_monitor import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
