#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\op_launcher_empty.ui'
#
# Created: Tue May 05 15:55:55 2015
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

class Ui_op_launcher(object):
    def setupUi(self, op_launcher):
        op_launcher.setObjectName(_fromUtf8("op_launcher"))
        op_launcher.resize(640, 480)
        self.verticalLayout = QtGui.QVBoxLayout(op_launcher)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.option_tab = QtGui.QTabWidget(op_launcher)
        self.option_tab.setObjectName(_fromUtf8("option_tab"))
        self.input_tab = QtGui.QWidget()
        self.input_tab.setObjectName(_fromUtf8("input_tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.input_tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.input_filed = QtGui.QWidget(self.input_tab)
        self.input_filed.setObjectName(_fromUtf8("input_filed"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.input_filed)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.input_filed)
        self.option_tab.addTab(self.input_tab, _fromUtf8(""))
        self.parameter_tab = QtGui.QWidget()
        self.parameter_tab.setObjectName(_fromUtf8("parameter_tab"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.parameter_tab)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.button_list = QtGui.QWidget(self.parameter_tab)
        self.button_list.setObjectName(_fromUtf8("button_list"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.button_list)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_6.addWidget(self.button_list)
        self.data_parameter = QtGui.QWidget(self.parameter_tab)
        self.data_parameter.setObjectName(_fromUtf8("data_parameter"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.data_parameter)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_6.addWidget(self.data_parameter)
        self.option_tab.addTab(self.parameter_tab, _fromUtf8(""))
        self.output_tab = QtGui.QWidget()
        self.output_tab.setObjectName(_fromUtf8("output_tab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.output_tab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.option_tab.addTab(self.output_tab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.option_tab)
        self.commande_op_widget = QtGui.QWidget(op_launcher)
        self.commande_op_widget.setObjectName(_fromUtf8("commande_op_widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.commande_op_widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.start_op_push_button = QtGui.QPushButton(self.commande_op_widget)
        self.start_op_push_button.setObjectName(_fromUtf8("start_op_push_button"))
        self.horizontalLayout_2.addWidget(self.start_op_push_button)
        spacerItem1 = QtGui.QSpacerItem(619, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.commande_op_widget)

        self.retranslateUi(op_launcher)
        self.option_tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(op_launcher)

    def retranslateUi(self, op_launcher):
        op_launcher.setWindowTitle("Operation launcher")
        self.option_tab.setTabText(self.option_tab.indexOf(self.input_tab), "Input")
        self.option_tab.setTabText(self.option_tab.indexOf(self.parameter_tab), "Parameter")
        self.option_tab.setTabText(self.option_tab.indexOf(self.output_tab), "Output")
        self.start_op_push_button.setText("Start")

