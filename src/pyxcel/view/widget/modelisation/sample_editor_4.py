#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\sample_editor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        Form.resize(640, 480)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.model_box = QtGui.QGroupBox(Form)
        self.model_box.setObjectName(_fromUtf8("model_box"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.model_box)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.widget_2 = QtGui.QWidget(self.model_box)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.add_model_button = QtGui.QPushButton(self.widget_2)
        self.add_model_button.setObjectName(_fromUtf8("add_model_button"))
        self.horizontalLayout_2.addWidget(self.add_model_button)
        self.copy_button = QtGui.QPushButton(self.widget_2)
        self.copy_button.setObjectName(_fromUtf8("copy_button"))
        self.horizontalLayout_2.addWidget(self.copy_button)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addWidget(self.widget_2)
        self.model_table = QtGui.QTableWidget(self.model_box)
        self.model_table.setObjectName(_fromUtf8("model_table"))
        self.model_table.setColumnCount(4)
        self.model_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.model_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.model_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.model_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.model_table.setHorizontalHeaderItem(3, item)
        self.verticalLayout_3.addWidget(self.model_table)
        self.verticalLayout.addWidget(self.model_box)
        self.data_box = QtGui.QGroupBox(Form)
        self.data_box.setObjectName(_fromUtf8("data_box"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.data_box)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QtGui.QWidget(self.data_box)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.add_exp_data_button = QtGui.QPushButton(self.widget)
        self.add_exp_data_button.setObjectName(_fromUtf8("add_exp_data_button"))
        self.horizontalLayout.addWidget(self.add_exp_data_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.widget)
        self.exp_data_table = QtGui.QTableWidget(self.data_box)
        self.exp_data_table.setObjectName(_fromUtf8("exp_data_table"))
        self.exp_data_table.setColumnCount(3)
        self.exp_data_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.exp_data_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.exp_data_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.exp_data_table.setHorizontalHeaderItem(2, item)
        self.verticalLayout_2.addWidget(self.exp_data_table)
        self.verticalLayout.addWidget(self.data_box)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Sample editor")
        self.model_box.setTitle("Model")
        self.add_model_button.setText("Add")
        self.copy_button.setText("Duplicate")
        item = self.model_table.horizontalHeaderItem(0)
        item.setText("Name")
        item = self.model_table.horizontalHeaderItem(1)
        item.setText("Atmosphere")
        item = self.model_table.horizontalHeaderItem(2)
        item.setText("Substrate")
        item = self.model_table.horizontalHeaderItem(3)
        item.setText("Layers")
        self.data_box.setTitle("Experimental data")
        self.add_exp_data_button.setText("Add")
        item = self.exp_data_table.horizontalHeaderItem(0)
        item.setText("Name")
        item = self.exp_data_table.horizontalHeaderItem(1)
        item.setText("Instrument")
        item = self.exp_data_table.horizontalHeaderItem(2)
        item.setText("2 theta scale")

