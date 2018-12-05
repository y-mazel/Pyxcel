#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\param_evol.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(503, 650)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.parameter_widget = QtWidgets.QTableWidget(Form)
        self.parameter_widget.setObjectName("parameter_widget")
        self.parameter_widget.setColumnCount(5)
        self.parameter_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.parameter_widget)
        self.fom_widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_widget.sizePolicy().hasHeightForWidth())
        self.fom_widget.setSizePolicy(sizePolicy)
        self.fom_widget.setObjectName("fom_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fom_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.fom_widget)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(401, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.corrcoef_button = QtWidgets.QPushButton(self.widget)
        self.corrcoef_button.setObjectName("corrcoef_button")
        self.horizontalLayout.addWidget(self.corrcoef_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Parameters evolution")
        item = self.parameter_widget.horizontalHeaderItem(0)
        item.setText("Parameter")
        item = self.parameter_widget.horizontalHeaderItem(1)
        item.setText("Value")
        item = self.parameter_widget.horizontalHeaderItem(2)
        item.setText("Lower bound")
        item = self.parameter_widget.horizontalHeaderItem(3)
        item.setText("Upper bound")
        item = self.parameter_widget.horizontalHeaderItem(4)
        item.setText("Error")
        self.corrcoef_button.setText("Correlation matrix")

