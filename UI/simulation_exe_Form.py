# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulation_exe_Form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(918, 571)
        self.setting_frame = QtWidgets.QFrame(Form)
        self.setting_frame.setEnabled(True)
        self.setting_frame.setGeometry(QtCore.QRect(10, 0, 901, 561))
        self.setting_frame.setToolTipDuration(2)
        self.setting_frame.setStyleSheet("")
        self.setting_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setting_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setting_frame.setObjectName("setting_frame")
        self.simulation_message_label = QtWidgets.QLabel(self.setting_frame)
        self.simulation_message_label.setGeometry(QtCore.QRect(20, 10, 121, 16))
        self.simulation_message_label.setObjectName("simulation_message_label")
        self.layoutWidget_2 = QtWidgets.QWidget(self.setting_frame)
        self.layoutWidget_2.setGeometry(QtCore.QRect(20, 260, 861, 25))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.start_or_pause_btn = QtWidgets.QPushButton(self.layoutWidget_2)
        self.start_or_pause_btn.setStyleSheet("image: url(:/icon/播放按钮.ico);")
        self.start_or_pause_btn.setText("")
        self.start_or_pause_btn.setObjectName("start_or_pause_btn")
        self.horizontalLayout_4.addWidget(self.start_or_pause_btn)
        self.stop_btn = QtWidgets.QPushButton(self.layoutWidget_2)
        self.stop_btn.setStyleSheet("image: url(:/icon/停止.ico);")
        self.stop_btn.setText("")
        self.stop_btn.setObjectName("stop_btn")
        self.horizontalLayout_4.addWidget(self.stop_btn)
        self.progress_label = QtWidgets.QLabel(self.layoutWidget_2)
        self.progress_label.setObjectName("progress_label")
        self.horizontalLayout_4.addWidget(self.progress_label)
        self.exe_progress_bar = QtWidgets.QProgressBar(self.layoutWidget_2)
        self.exe_progress_bar.setProperty("value", 0)
        self.exe_progress_bar.setObjectName("exe_progress_bar")
        self.horizontalLayout_4.addWidget(self.exe_progress_bar)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.setting_frame)
        self.tableWidget_3.setGeometry(QtCore.QRect(20, 30, 341, 221))
        self.tableWidget_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(11)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(6, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(7, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(8, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(9, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(9, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(10, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(10, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(10, 2, item)
        self.layoutWidget_3 = QtWidgets.QWidget(self.setting_frame)
        self.layoutWidget_3.setGeometry(QtCore.QRect(20, 290, 861, 251))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget_3)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_53 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_53.setObjectName("label_53")
        self.gridLayout_6.addWidget(self.label_53, 0, 0, 1, 1)
        self.label_54 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_54.setObjectName("label_54")
        self.gridLayout_6.addWidget(self.label_54, 0, 1, 1, 1)
        self.label_55 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_55.setObjectName("label_55")
        self.gridLayout_6.addWidget(self.label_55, 0, 2, 1, 1)
        self.log_text = QtWidgets.QTextEdit(self.layoutWidget_3)
        self.log_text.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.log_text.setObjectName("log_text")
        self.gridLayout_6.addWidget(self.log_text, 1, 0, 1, 1)
        self.log_text_2 = QtWidgets.QTextEdit(self.layoutWidget_3)
        self.log_text_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.log_text_2.setObjectName("log_text_2")
        self.gridLayout_6.addWidget(self.log_text_2, 1, 1, 1, 1)
        self.log_text_3 = QtWidgets.QTextEdit(self.layoutWidget_3)
        self.log_text_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.log_text_3.setObjectName("log_text_3")
        self.gridLayout_6.addWidget(self.log_text_3, 1, 2, 1, 1)
        self.layoutWidget_4 = QtWidgets.QWidget(self.setting_frame)
        self.layoutWidget_4.setGeometry(QtCore.QRect(370, 230, 509, 22))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_56 = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_56.setObjectName("label_56")
        self.horizontalLayout_6.addWidget(self.label_56)
        self.se_ID_edit_2 = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.se_ID_edit_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.se_ID_edit_2.setText("")
        self.se_ID_edit_2.setObjectName("se_ID_edit_2")
        self.horizontalLayout_6.addWidget(self.se_ID_edit_2)
        self.label_57 = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_57.setObjectName("label_57")
        self.horizontalLayout_6.addWidget(self.label_57)
        self.se_ID_edit_3 = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.se_ID_edit_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.se_ID_edit_3.setText("")
        self.se_ID_edit_3.setObjectName("se_ID_edit_3")
        self.horizontalLayout_6.addWidget(self.se_ID_edit_3)
        self.label_58 = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_58.setObjectName("label_58")
        self.horizontalLayout_6.addWidget(self.label_58)
        self.se_ID_edit_4 = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.se_ID_edit_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.se_ID_edit_4.setText("")
        self.se_ID_edit_4.setObjectName("se_ID_edit_4")
        self.horizontalLayout_6.addWidget(self.se_ID_edit_4)
        self.layoutWidget_5 = QtWidgets.QWidget(self.setting_frame)
        self.layoutWidget_5.setGeometry(QtCore.QRect(371, 120, 511, 100))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget_5)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.se_ID_label = QtWidgets.QLabel(self.layoutWidget_5)
        self.se_ID_label.setObjectName("se_ID_label")
        self.gridLayout_2.addWidget(self.se_ID_label, 0, 0, 1, 1)
        self.se_ID_edit = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.se_ID_edit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.se_ID_edit.setText("")
        self.se_ID_edit.setObjectName("se_ID_edit")
        self.gridLayout_2.addWidget(self.se_ID_edit, 0, 1, 1, 1)
        self.result_handle_label = QtWidgets.QLabel(self.layoutWidget_5)
        self.result_handle_label.setObjectName("result_handle_label")
        self.gridLayout_2.addWidget(self.result_handle_label, 0, 2, 1, 1)
        self.result_handle_combobox = QtWidgets.QComboBox(self.layoutWidget_5)
        self.result_handle_combobox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.result_handle_combobox.setObjectName("result_handle_combobox")
        self.result_handle_combobox.addItem("")
        self.result_handle_combobox.addItem("")
        self.gridLayout_2.addWidget(self.result_handle_combobox, 0, 3, 1, 1)
        self.se_ID_label_2 = QtWidgets.QLabel(self.layoutWidget_5)
        self.se_ID_label_2.setObjectName("se_ID_label_2")
        self.gridLayout_2.addWidget(self.se_ID_label_2, 1, 0, 1, 1)
        self.se_ID_edit_5 = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.se_ID_edit_5.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.se_ID_edit_5.setText("")
        self.se_ID_edit_5.setObjectName("se_ID_edit_5")
        self.gridLayout_2.addWidget(self.se_ID_edit_5, 1, 1, 1, 1)
        self.se_ID_label_3 = QtWidgets.QLabel(self.layoutWidget_5)
        self.se_ID_label_3.setObjectName("se_ID_label_3")
        self.gridLayout_2.addWidget(self.se_ID_label_3, 1, 2, 1, 1)
        self.se_ID_edit_6 = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.se_ID_edit_6.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.se_ID_edit_6.setText("")
        self.se_ID_edit_6.setObjectName("se_ID_edit_6")
        self.gridLayout_2.addWidget(self.se_ID_edit_6, 1, 3, 1, 1)
        self.version_label = QtWidgets.QLabel(self.layoutWidget_5)
        self.version_label.setObjectName("version_label")
        self.gridLayout_2.addWidget(self.version_label, 2, 0, 1, 1)
        self.version_edit = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.version_edit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.version_edit.setText("")
        self.version_edit.setObjectName("version_edit")
        self.gridLayout_2.addWidget(self.version_edit, 2, 1, 1, 1)
        self.generation_label = QtWidgets.QLabel(self.layoutWidget_5)
        self.generation_label.setObjectName("generation_label")
        self.gridLayout_2.addWidget(self.generation_label, 2, 2, 1, 1)
        self.generation_lineEdit = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.generation_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.generation_lineEdit.setText("")
        self.generation_lineEdit.setObjectName("generation_lineEdit")
        self.gridLayout_2.addWidget(self.generation_lineEdit, 2, 3, 1, 1)
        self.modify_date_label = QtWidgets.QLabel(self.layoutWidget_5)
        self.modify_date_label.setObjectName("modify_date_label")
        self.gridLayout_2.addWidget(self.modify_date_label, 3, 0, 1, 1)
        self.modify_dateEdit = QtWidgets.QDateEdit(self.layoutWidget_5)
        self.modify_dateEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.modify_dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2019, 11, 5), QtCore.QTime(0, 0, 0)))
        self.modify_dateEdit.setObjectName("modify_dateEdit")
        self.gridLayout_2.addWidget(self.modify_dateEdit, 3, 1, 1, 1)
        self.step_size_label = QtWidgets.QLabel(self.layoutWidget_5)
        self.step_size_label.setObjectName("step_size_label")
        self.gridLayout_2.addWidget(self.step_size_label, 3, 2, 1, 1)
        self.step_size_lineEdit = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.step_size_lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.step_size_lineEdit.setText("")
        self.step_size_lineEdit.setObjectName("step_size_lineEdit")
        self.gridLayout_2.addWidget(self.step_size_lineEdit, 3, 3, 1, 1)
        self.layoutWidget_6 = QtWidgets.QWidget(self.setting_frame)
        self.layoutWidget_6.setGeometry(QtCore.QRect(370, 32, 511, 83))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget_6)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.units_dir_label = QtWidgets.QLabel(self.layoutWidget_6)
        self.units_dir_label.setObjectName("units_dir_label")
        self.gridLayout.addWidget(self.units_dir_label, 0, 0, 1, 1)
        self.units_dir_path = QtWidgets.QLineEdit(self.layoutWidget_6)
        self.units_dir_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.units_dir_path.setText("")
        self.units_dir_path.setObjectName("units_dir_path")
        self.gridLayout.addWidget(self.units_dir_path, 0, 1, 1, 1)
        self.units_filedialog_btn = QtWidgets.QPushButton(self.layoutWidget_6)
        self.units_filedialog_btn.setObjectName("units_filedialog_btn")
        self.gridLayout.addWidget(self.units_filedialog_btn, 0, 2, 1, 1)
        self.simu_meta_dir_label = QtWidgets.QLabel(self.layoutWidget_6)
        self.simu_meta_dir_label.setObjectName("simu_meta_dir_label")
        self.gridLayout.addWidget(self.simu_meta_dir_label, 1, 0, 1, 1)
        self.simu_meta_dir_path = QtWidgets.QLineEdit(self.layoutWidget_6)
        self.simu_meta_dir_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.simu_meta_dir_path.setText("")
        self.simu_meta_dir_path.setObjectName("simu_meta_dir_path")
        self.gridLayout.addWidget(self.simu_meta_dir_path, 1, 1, 1, 1)
        self.simu_meta_filedialog_btn = QtWidgets.QPushButton(self.layoutWidget_6)
        self.simu_meta_filedialog_btn.setObjectName("simu_meta_filedialog_btn")
        self.gridLayout.addWidget(self.simu_meta_filedialog_btn, 1, 2, 1, 1)
        self.record_dir_label = QtWidgets.QLabel(self.layoutWidget_6)
        self.record_dir_label.setObjectName("record_dir_label")
        self.gridLayout.addWidget(self.record_dir_label, 2, 0, 1, 1)
        self.record_dir_path = QtWidgets.QLineEdit(self.layoutWidget_6)
        self.record_dir_path.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.record_dir_path.setText("")
        self.record_dir_path.setObjectName("record_dir_path")
        self.gridLayout.addWidget(self.record_dir_path, 2, 1, 1, 1)
        self.record_filedialog_btn = QtWidgets.QPushButton(self.layoutWidget_6)
        self.record_filedialog_btn.setObjectName("record_filedialog_btn")
        self.gridLayout.addWidget(self.record_filedialog_btn, 2, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.simulation_message_label.setText(_translate("Form", "Simulation message："))
        self.start_or_pause_btn.setToolTip(_translate("Form", "<html><head/><body><p>开始</p></body></html>"))
        self.start_or_pause_btn.setWhatsThis(_translate("Form", "<html><head/><body><p>继续</p></body></html>"))
        self.stop_btn.setToolTip(_translate("Form", "<html><head/><body><p>终止</p></body></html>"))
        self.stop_btn.setWhatsThis(_translate("Form", "<html><head/><body><p>终止</p></body></html>"))
        self.progress_label.setText(_translate("Form", "Progress:"))
        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_3.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget_3.verticalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.tableWidget_3.verticalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.tableWidget_3.verticalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        item = self.tableWidget_3.verticalHeaderItem(5)
        item.setText(_translate("Form", "6"))
        item = self.tableWidget_3.verticalHeaderItem(6)
        item.setText(_translate("Form", "7"))
        item = self.tableWidget_3.verticalHeaderItem(7)
        item.setText(_translate("Form", "8"))
        item = self.tableWidget_3.verticalHeaderItem(8)
        item.setText(_translate("Form", "9"))
        item = self.tableWidget_3.verticalHeaderItem(9)
        item.setText(_translate("Form", "10"))
        item = self.tableWidget_3.verticalHeaderItem(10)
        item.setText(_translate("Form", "11"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Member"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Role"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Status"))
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        self.tableWidget_3.setSortingEnabled(__sortingEnabled)
        self.label_53.setText(_translate("Form", "mutual message:"))
        self.label_54.setText(_translate("Form", "Warning message:"))
        self.label_55.setText(_translate("Form", "service message:"))
        self.log_text.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.log_text_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.log_text_3.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_56.setText(_translate("Form", "Units："))
        self.label_57.setText(_translate("Form", "Advisors："))
        self.label_58.setText(_translate("Form", "Monitors："))
        self.se_ID_label.setText(_translate("Form", "Execute ID："))
        self.result_handle_label.setText(_translate("Form", "Inherit setting："))
        self.result_handle_combobox.setItemText(0, _translate("Form", "inherit"))
        self.result_handle_combobox.setItemText(1, _translate("Form", "don\'t inherit"))
        self.se_ID_label_2.setText(_translate("Form", "Meta Member ID："))
        self.se_ID_label_3.setText(_translate("Form", "definition ID："))
        self.version_label.setText(_translate("Form", "Version："))
        self.generation_label.setText(_translate("Form", "Generation："))
        self.modify_date_label.setText(_translate("Form", "Modify date："))
        self.modify_dateEdit.setDisplayFormat(_translate("Form", "yyyy.MM.dd"))
        self.step_size_label.setText(_translate("Form", "Record step size："))
        self.units_dir_label.setText(_translate("Form", "Member path："))
        self.units_filedialog_btn.setText(_translate("Form", "Browser..."))
        self.simu_meta_dir_label.setText(_translate("Form", "Simulation Meta path："))
        self.simu_meta_filedialog_btn.setText(_translate("Form", "Browser..."))
        self.record_dir_label.setText(_translate("Form", "Record path："))
        self.record_filedialog_btn.setText(_translate("Form", "Setting..."))

import UI.GraphRes_rc
