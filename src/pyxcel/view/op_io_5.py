#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\op_io2.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(442, 633)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.resultat_widget = QtWidgets.QWidget(Form)
        self.resultat_widget.setObjectName("resultat_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.resultat_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.resultat_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.save_button = QtWidgets.QPushButton(self.resultat_widget)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_2.addWidget(self.save_button)
        self.analyse_button = QtWidgets.QPushButton(self.resultat_widget)
        self.analyse_button.setObjectName("analyse_button")
        self.horizontalLayout_2.addWidget(self.analyse_button)
        self.save_and_analyse_button = QtWidgets.QPushButton(self.resultat_widget)
        self.save_and_analyse_button.setObjectName("save_and_analyse_button")
        self.horizontalLayout_2.addWidget(self.save_and_analyse_button)
        self.verticalLayout.addWidget(self.resultat_widget)
        self.input_widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_widget.sizePolicy().hasHeightForWidth())
        self.input_widget.setSizePolicy(sizePolicy)
        self.input_widget.setObjectName("input_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.input_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.input_widget)
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.launch_button = QtWidgets.QPushButton(self.widget)
        self.launch_button.setObjectName("launch_button")
        self.horizontalLayout.addWidget(self.launch_button)
        self.reset_button = QtWidgets.QPushButton(self.widget)
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout.addWidget(self.reset_button)
        spacerItem = QtWidgets.QSpacerItem(413, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.graph_button = QtWidgets.QPushButton(self.widget)
        self.graph_button.setObjectName("graph_button")
        self.horizontalLayout.addWidget(self.graph_button)
        self.parameter_button = QtWidgets.QPushButton(self.widget)
        self.parameter_button.setObjectName("parameter_button")
        self.horizontalLayout.addWidget(self.parameter_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Operation I/O")
        self.label.setText("Result: ")
        self.save_button.setText("Save")
        self.analyse_button.setText("Analyze")
        self.save_and_analyse_button.setText("Save and analyze")
        self.launch_button.setText("Run")
        self.reset_button.setText("Reset")
        self.graph_button.setText("Graph")
        self.parameter_button.setText("Parameters")

