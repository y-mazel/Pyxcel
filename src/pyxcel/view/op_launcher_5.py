#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\op_launcher_empty.ui'
#
# Created: Tue May  5 15:56:03 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_op_launcher(object):
    def setupUi(self, op_launcher):
        op_launcher.setObjectName("op_launcher")
        op_launcher.resize(640, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(op_launcher)
        self.verticalLayout.setObjectName("verticalLayout")
        self.option_tab = QtWidgets.QTabWidget(op_launcher)
        self.option_tab.setObjectName("option_tab")
        self.input_tab = QtWidgets.QWidget()
        self.input_tab.setObjectName("input_tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.input_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.input_filed = QtWidgets.QWidget(self.input_tab)
        self.input_filed.setObjectName("input_filed")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.input_filed)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.input_filed)
        self.option_tab.addTab(self.input_tab, "")
        self.parameter_tab = QtWidgets.QWidget()
        self.parameter_tab.setObjectName("parameter_tab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.parameter_tab)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.button_list = QtWidgets.QWidget(self.parameter_tab)
        self.button_list.setObjectName("button_list")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.button_list)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6.addWidget(self.button_list)
        self.data_parameter = QtWidgets.QWidget(self.parameter_tab)
        self.data_parameter.setObjectName("data_parameter")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.data_parameter)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6.addWidget(self.data_parameter)
        self.option_tab.addTab(self.parameter_tab, "")
        self.output_tab = QtWidgets.QWidget()
        self.output_tab.setObjectName("output_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.output_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.option_tab.addTab(self.output_tab, "")
        self.verticalLayout.addWidget(self.option_tab)
        self.commande_op_widget = QtWidgets.QWidget(op_launcher)
        self.commande_op_widget.setObjectName("commande_op_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.commande_op_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.start_op_push_button = QtWidgets.QPushButton(self.commande_op_widget)
        self.start_op_push_button.setObjectName("start_op_push_button")
        self.horizontalLayout_2.addWidget(self.start_op_push_button)
        spacerItem1 = QtWidgets.QSpacerItem(619, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.commande_op_widget)

        self.retranslateUi(op_launcher)
        self.option_tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(op_launcher)

    def retranslateUi(self, op_launcher):
        _translate = QtCore.QCoreApplication.translate
        op_launcher.setWindowTitle("Operation launcher")
        self.option_tab.setTabText(self.option_tab.indexOf(self.input_tab), "Input")
        self.option_tab.setTabText(self.option_tab.indexOf(self.parameter_tab), "Parameter")
        self.option_tab.setTabText(self.option_tab.indexOf(self.output_tab), "Output")
        self.start_op_push_button.setText("Start")

