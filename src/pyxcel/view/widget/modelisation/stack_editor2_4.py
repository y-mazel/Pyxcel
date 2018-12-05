#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\stack_editor2.ui'
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
        Form.resize(667, 493)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget_5 = QtGui.QWidget(Form)
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.add_layer_button = QtGui.QPushButton(self.widget_5)
        self.add_layer_button.setObjectName(_fromUtf8("add_layer_button"))
        self.horizontalLayout_5.addWidget(self.add_layer_button)
        self.label = QtGui.QLabel(self.widget_5)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_5.addWidget(self.label)
        self.repetition_spin = QtGui.QSpinBox(self.widget_5)
        self.repetition_spin.setMinimum(1)
        self.repetition_spin.setMaximum(999)
        self.repetition_spin.setObjectName(_fromUtf8("repetition_spin"))
        self.horizontalLayout_5.addWidget(self.repetition_spin)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.delete_layer_button = QtGui.QPushButton(self.widget_5)
        self.delete_layer_button.setObjectName(_fromUtf8("delete_layer_button"))
        self.horizontalLayout_5.addWidget(self.delete_layer_button)
        self.verticalLayout_2.addWidget(self.widget_5)
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.layer_table = QtGui.QTableWidget(self.widget_2)
        self.layer_table.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.layer_table.setStyleSheet(_fromUtf8(""))
        self.layer_table.setObjectName(_fromUtf8("layer_table"))
        self.layer_table.setColumnCount(8)
        self.layer_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        item.setFont(font)
        self.layer_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(7, item)
        self.horizontalLayout_4.addWidget(self.layer_table)
        self.widget_6 = QtGui.QWidget(self.widget_2)
        self.widget_6.setObjectName(_fromUtf8("widget_6"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.up_button = QtGui.QPushButton(self.widget_6)
        self.up_button.setObjectName(_fromUtf8("up_button"))
        self.verticalLayout.addWidget(self.up_button)
        self.down_button = QtGui.QPushButton(self.widget_6)
        self.down_button.setObjectName(_fromUtf8("down_button"))
        self.verticalLayout.addWidget(self.down_button)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.simulate_button = QtGui.QPushButton(self.widget_6)
        self.simulate_button.setObjectName(_fromUtf8("simulate_button"))
        self.verticalLayout.addWidget(self.simulate_button)
        self.horizontalLayout_4.addWidget(self.widget_6)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.create_sigmai_action = QtGui.QAction(Form)
        self.create_sigmai_action.setObjectName(_fromUtf8("create_sigmai_action"))
        self.delete_layer_action = QtGui.QAction(Form)
        self.delete_layer_action.setObjectName(_fromUtf8("delete_layer_action"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Stack editor 2")
        self.add_layer_button.setText("Add")
        self.label.setText("Repetition")
        self.delete_layer_button.setText("Delete")
        item = self.layer_table.horizontalHeaderItem(0)
        item.setText("Name")
        item = self.layer_table.horizontalHeaderItem(1)
        item.setText("Material")
        item = self.layer_table.horizontalHeaderItem(2)
        item.setText("Thickness (A)")
        item = self.layer_table.horizontalHeaderItem(3)
        item.setText("Numerical density (A-3)")
        item = self.layer_table.horizontalHeaderItem(4)
        item.setText("Mass density (g.cm-3)")
        item = self.layer_table.horizontalHeaderItem(5)
        item.setText("Roughness (A)")
        item = self.layer_table.horizontalHeaderItem(6)
        item.setText("Repetition")
        item = self.layer_table.horizontalHeaderItem(7)
        item.setText("Profile")
        self.up_button.setText("Move up")
        self.down_button.setText("Move down")
        self.simulate_button.setText("Simulate")
        self.create_sigmai_action.setText("Create intermixing layer")
        self.delete_layer_action.setText("Delete layer")
        self.delete_layer_action.setToolTip("Delete layer")

