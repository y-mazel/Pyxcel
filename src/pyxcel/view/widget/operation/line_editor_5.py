#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\line_editor.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setSpacing(0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.element_combo = QtWidgets.QComboBox(self.widget)
        self.element_combo.setObjectName("element_combo")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.element_combo)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.line_combo = QtWidgets.QComboBox(self.widget)
        self.line_combo.setObjectName("line_combo")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.line_combo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout_2.setItem(5, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.horizontalLayout.addWidget(self.widget)
        self.validate_widget = QtWidgets.QWidget(Form)
        self.validate_widget.setObjectName("validate_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.validate_widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.validate_button = QtWidgets.QPushButton(self.validate_widget)
        self.validate_button.setObjectName("validate_button")
        self.verticalLayout.addWidget(self.validate_button)
        self.cancel_button = QtWidgets.QPushButton(self.validate_widget)
        self.cancel_button.setObjectName("cancel_button")
        self.verticalLayout.addWidget(self.cancel_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.validate_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Line editor")
        self.label.setText("Input")
        self.label_2.setText("Line: ")
        self.validate_button.setText("Ok")
        self.cancel_button.setText("Cancel")

