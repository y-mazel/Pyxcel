#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\op_io2.ui'
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
        Form.resize(442, 633)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.resultat_widget = QtGui.QWidget(Form)
        self.resultat_widget.setObjectName(_fromUtf8("resultat_widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.resultat_widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.resultat_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.save_button = QtGui.QPushButton(self.resultat_widget)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.horizontalLayout_2.addWidget(self.save_button)
        self.analyse_button = QtGui.QPushButton(self.resultat_widget)
        self.analyse_button.setObjectName(_fromUtf8("analyse_button"))
        self.horizontalLayout_2.addWidget(self.analyse_button)
        self.save_and_analyse_button = QtGui.QPushButton(self.resultat_widget)
        self.save_and_analyse_button.setObjectName(_fromUtf8("save_and_analyse_button"))
        self.horizontalLayout_2.addWidget(self.save_and_analyse_button)
        self.verticalLayout.addWidget(self.resultat_widget)
        self.input_widget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_widget.sizePolicy().hasHeightForWidth())
        self.input_widget.setSizePolicy(sizePolicy)
        self.input_widget.setObjectName(_fromUtf8("input_widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.input_widget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout.addWidget(self.input_widget)
        self.widget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.launch_button = QtGui.QPushButton(self.widget)
        self.launch_button.setObjectName(_fromUtf8("launch_button"))
        self.horizontalLayout.addWidget(self.launch_button)
        self.reset_button = QtGui.QPushButton(self.widget)
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.horizontalLayout.addWidget(self.reset_button)
        spacerItem = QtGui.QSpacerItem(413, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.graph_button = QtGui.QPushButton(self.widget)
        self.graph_button.setObjectName(_fromUtf8("graph_button"))
        self.horizontalLayout.addWidget(self.graph_button)
        self.parameter_button = QtGui.QPushButton(self.widget)
        self.parameter_button.setObjectName(_fromUtf8("parameter_button"))
        self.horizontalLayout.addWidget(self.parameter_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Operation I/O")
        self.label.setText("Result: ")
        self.save_button.setText("Save")
        self.analyse_button.setText("Analyze")
        self.save_and_analyse_button.setText("Save and analyze")
        self.launch_button.setText("Run")
        self.reset_button.setText("Reset")
        self.graph_button.setText("Graph")
        self.parameter_button.setText("Parameters")

