#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\modeling_window_simple.ui'
#
# Created: Fri Jun  5 15:32:59 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_modeling_window(object):
    def setupUi(self, modeling_window):
        modeling_window.setObjectName("modeling_window")
        modeling_window.resize(585, 458)
        self.main_layout = QtWidgets.QVBoxLayout(modeling_window)
        self.main_layout.setObjectName("main_layout")
        self.main_widget = QtWidgets.QWidget(modeling_window)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 375, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.main_layout.addWidget(self.main_widget)

        self.retranslateUi(modeling_window)
        QtCore.QMetaObject.connectSlotsByName(modeling_window)

    def retranslateUi(self, modeling_window):
        _translate = QtCore.QCoreApplication.translate
        modeling_window.setWindowTitle("Modeling window")

