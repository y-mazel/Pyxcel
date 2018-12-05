#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\stack_editor2.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(667, 493)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_5 = QtWidgets.QWidget(Form)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.add_layer_button = QtWidgets.QPushButton(self.widget_5)
        self.add_layer_button.setObjectName("add_layer_button")
        self.horizontalLayout_5.addWidget(self.add_layer_button)
        self.label = QtWidgets.QLabel(self.widget_5)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.repetition_spin = QtWidgets.QSpinBox(self.widget_5)
        self.repetition_spin.setMinimum(1)
        self.repetition_spin.setMaximum(999)
        self.repetition_spin.setObjectName("repetition_spin")
        self.horizontalLayout_5.addWidget(self.repetition_spin)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.delete_layer_button = QtWidgets.QPushButton(self.widget_5)
        self.delete_layer_button.setObjectName("delete_layer_button")
        self.horizontalLayout_5.addWidget(self.delete_layer_button)
        self.verticalLayout_2.addWidget(self.widget_5)
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.layer_table = QtWidgets.QTableWidget(self.widget_2)
        self.layer_table.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.layer_table.setStyleSheet("")
        self.layer_table.setObjectName("layer_table")
        self.layer_table.setColumnCount(8)
        self.layer_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        item.setFont(font)
        self.layer_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(7, item)
        self.horizontalLayout_4.addWidget(self.layer_table)
        self.widget_6 = QtWidgets.QWidget(self.widget_2)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.up_button = QtWidgets.QPushButton(self.widget_6)
        self.up_button.setObjectName("up_button")
        self.verticalLayout.addWidget(self.up_button)
        self.down_button = QtWidgets.QPushButton(self.widget_6)
        self.down_button.setObjectName("down_button")
        self.verticalLayout.addWidget(self.down_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.simulate_button = QtWidgets.QPushButton(self.widget_6)
        self.simulate_button.setObjectName("simulate_button")
        self.verticalLayout.addWidget(self.simulate_button)
        self.horizontalLayout_4.addWidget(self.widget_6)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.create_sigmai_action = QtWidgets.QAction(Form)
        self.create_sigmai_action.setObjectName("create_sigmai_action")
        self.delete_layer_action = QtWidgets.QAction(Form)
        self.delete_layer_action.setObjectName("delete_layer_action")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Stack editor 2")
        self.add_layer_button.setText("Add")
        self.label.setText("Repetition")
        self.delete_layer_button.setText("Delete")
        item = self.layer_table.horizontalHeaderItem(0)
        item.setText("Name")
        item = self.layer_table.horizontalHeaderItem(1)
        item.setText("Material")
        item = self.layer_table.horizontalHeaderItem(2)
        item.setText("Thickness")
        item = self.layer_table.horizontalHeaderItem(3)
        item.setText("Numerical density")
        item = self.layer_table.horizontalHeaderItem(4)
        item.setText("Mass density")
        item = self.layer_table.horizontalHeaderItem(5)
        item.setText("Rougness")
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
