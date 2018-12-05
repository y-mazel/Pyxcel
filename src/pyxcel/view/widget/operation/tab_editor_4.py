#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\tab_editor.ui'
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
        self.widget_3 = QtGui.QWidget(Form)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.widget_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.element_combo = QtGui.QComboBox(self.widget_3)
        self.element_combo.setEditable(True)
        self.element_combo.setObjectName(_fromUtf8("element_combo"))
        self.horizontalLayout_2.addWidget(self.element_combo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.widget_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.parameter_combo = QtGui.QComboBox(self.widget_3)
        self.parameter_combo.setEditable(False)
        self.parameter_combo.setObjectName(_fromUtf8("parameter_combo"))
        self.horizontalLayout_2.addWidget(self.parameter_combo)
        self.add_button = QtGui.QPushButton(self.widget_3)
        self.add_button.setObjectName(_fromUtf8("add_button"))
        self.horizontalLayout_2.addWidget(self.add_button)
        self.delete_button = QtGui.QPushButton(self.widget_3)
        self.delete_button.setObjectName(_fromUtf8("delete_button"))
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.verticalLayout.addWidget(self.widget_3)
        self.parameter_tab = QtGui.QTableWidget(Form)
        self.parameter_tab.setObjectName(_fromUtf8("parameter_tab"))
        self.parameter_tab.setColumnCount(7)
        self.parameter_tab.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_tab.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.parameter_tab)
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.save_button = QtGui.QPushButton(self.widget)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.horizontalLayout.addWidget(self.save_button)
        self.load_button = QtGui.QPushButton(self.widget)
        self.load_button.setObjectName(_fromUtf8("load_button"))
        self.horizontalLayout.addWidget(self.load_button)
        spacerItem1 = QtGui.QSpacerItem(439, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancel_button = QtGui.QPushButton(self.widget)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout.addWidget(self.cancel_button)
        self.validate_button = QtGui.QPushButton(self.widget)
        self.validate_button.setObjectName(_fromUtf8("validate_button"))
        self.horizontalLayout.addWidget(self.validate_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Parameter editor")
        self.label.setText("Element: ")
        self.label_2.setText("Parameter: ")
        self.add_button.setText("Add")
        self.delete_button.setText("Delete")
        item = self.parameter_tab.horizontalHeaderItem(0)
        item.setText("Parameter")
        item = self.parameter_tab.horizontalHeaderItem(1)
        item.setText("Refine")
        item = self.parameter_tab.horizontalHeaderItem(2)
        item.setText("Value: ")
        item = self.parameter_tab.horizontalHeaderItem(3)
        item.setText("Min")
        item = self.parameter_tab.horizontalHeaderItem(4)
        item.setText("Max")
        item = self.parameter_tab.horizontalHeaderItem(5)
        item.setText("Error")
        item = self.parameter_tab.horizontalHeaderItem(6)
        item.setText("Group")
        self.save_button.setText("Save")
        self.load_button.setText("Load")
        self.cancel_button.setText("Cancel")
        self.validate_button.setText("Ok")

