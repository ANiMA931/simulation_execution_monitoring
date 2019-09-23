# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coEvolution_exe.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(903, 635)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 901, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.simulation_widget_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.simulation_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.simulation_widget_layout.setObjectName("simulation_widget_layout")
        self.simulation_widget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.simulation_widget.setObjectName("simulation_widget")
        self.simulation_widget_layout.addWidget(self.simulation_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 903, 23))
        self.menubar.setObjectName("menubar")
        self.menu_XML = QtWidgets.QMenu(self.menubar)
        self.menu_XML.setObjectName("menu_XML")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_XML = QtWidgets.QAction(MainWindow)
        self.action_XML.setObjectName("action_XML")
        self.menu_XML.addAction(self.action_XML)
        self.menubar.addAction(self.menu_XML.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_XML.setTitle(_translate("MainWindow", "仿真XML"))
        self.action_XML.setText(_translate("MainWindow", "选择XML"))

import GraphRes_rc
