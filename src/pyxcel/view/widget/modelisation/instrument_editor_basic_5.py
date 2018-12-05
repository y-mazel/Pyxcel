#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\instrument_editor_basic.ui'
#
# Created: Wed Aug  5 08:50:52 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.source_box = QtWidgets.QGroupBox(Form)
        self.source_box.setObjectName("source_box")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.source_box)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout.addWidget(self.source_box)
        self.detector_box = QtWidgets.QGroupBox(Form)
        self.detector_box.setObjectName("detector_box")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.detector_box)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout.addWidget(self.detector_box)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Basic instrument editor")
        self.source_box.setTitle("Source")
        self.detector_box.setTitle("Detector")

