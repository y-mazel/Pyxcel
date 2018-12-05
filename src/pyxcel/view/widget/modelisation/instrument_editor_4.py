#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\instrument_editor.ui'
#
# Created: Thu Apr 30 08:05:46 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(642, 536)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.default_value_widget = QtGui.QWidget(Form)
        self.default_value_widget.setObjectName(_fromUtf8("default_value_widget"))
        self.default_value_widget_2 = QtGui.QHBoxLayout(self.default_value_widget)
        self.default_value_widget_2.setMargin(0)
        self.default_value_widget_2.setObjectName(_fromUtf8("default_value_widget_2"))
        self.label = QtGui.QLabel(self.default_value_widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.default_value_widget_2.addWidget(self.label)
        self.default_value_edit = QtGui.QLineEdit(self.default_value_widget)
        self.default_value_edit.setObjectName(_fromUtf8("default_value_edit"))
        self.default_value_widget_2.addWidget(self.default_value_edit)
        self.default_value_ed_button = QtGui.QPushButton(self.default_value_widget)
        self.default_value_ed_button.setObjectName(_fromUtf8("default_value_ed_button"))
        self.default_value_widget_2.addWidget(self.default_value_ed_button)
        self.verticalLayout.addWidget(self.default_value_widget)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget_2 = QtGui.QWidget(self.groupBox)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.new_calibration_button = QtGui.QPushButton(self.widget_2)
        self.new_calibration_button.setObjectName(_fromUtf8("new_calibration_button"))
        self.horizontalLayout_2.addWidget(self.new_calibration_button)
        spacerItem = QtGui.QSpacerItem(502, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.calibration_table = QtGui.QTableWidget(self.groupBox)
        self.calibration_table.setObjectName(_fromUtf8("calibration_table"))
        self.calibration_table.setColumnCount(2)
        self.calibration_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.calibration_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.calibration_table.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.calibration_table)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.calibration_value_widget = QtGui.QWidget(self.groupBox_2)
        self.calibration_value_widget.setObjectName(_fromUtf8("calibration_value_widget"))
        self.calibration_value_widget_2 = QtGui.QHBoxLayout(self.calibration_value_widget)
        self.calibration_value_widget_2.setMargin(0)
        self.calibration_value_widget_2.setObjectName(_fromUtf8("calibration_value_widget_2"))
        self.label_2 = QtGui.QLabel(self.calibration_value_widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.calibration_value_widget_2.addWidget(self.label_2)
        self.calibration_value_edit = QtGui.QLineEdit(self.calibration_value_widget)
        self.calibration_value_edit.setObjectName(_fromUtf8("calibration_value_edit"))
        self.calibration_value_widget_2.addWidget(self.calibration_value_edit)
        self.calibration_value_ed_button = QtGui.QPushButton(self.calibration_value_widget)
        self.calibration_value_ed_button.setObjectName(_fromUtf8("calibration_value_ed_button"))
        self.calibration_value_widget_2.addWidget(self.calibration_value_ed_button)
        self.verticalLayout_3.addWidget(self.calibration_value_widget)
        self.widget_3 = QtGui.QWidget(self.groupBox_2)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.new_sample = QtGui.QPushButton(self.widget_3)
        self.new_sample.setObjectName(_fromUtf8("new_sample"))
        self.horizontalLayout_3.addWidget(self.new_sample)
        self.choose_sample = QtGui.QPushButton(self.widget_3)
        self.choose_sample.setObjectName(_fromUtf8("choose_sample"))
        self.horizontalLayout_3.addWidget(self.choose_sample)
        spacerItem1 = QtGui.QSpacerItem(385, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.sample_table = QtGui.QTableWidget(self.groupBox_2)
        self.sample_table.setObjectName(_fromUtf8("sample_table"))
        self.sample_table.setColumnCount(0)
        self.sample_table.setRowCount(0)
        self.verticalLayout_3.addWidget(self.sample_table)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Instrument editor")
        self.label.setText("Init values: ")
        self.default_value_ed_button.setText("Edit")
        self.groupBox.setTitle("Calibration: ")
        self.new_calibration_button.setText("New")
        item = self.calibration_table.horizontalHeaderItem(0)
        item.setText("Name: ")
        item = self.calibration_table.horizontalHeaderItem(1)
        item.setText("Date: ")
        self.groupBox_2.setTitle("Details: ")
        self.label_2.setText("Value")
        self.calibration_value_ed_button.setText("Edit")
        self.new_sample.setText("New sample")
        self.choose_sample.setText("Select sample")

