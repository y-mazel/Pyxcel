#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\composite_editor2.ui'
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
        self.workspace_scroll = QtWidgets.QScrollArea(Form)
        self.workspace_scroll.setFrameShadow(QtWidgets.QFrame.Raised)
        self.workspace_scroll.setWidgetResizable(True)
        self.workspace_scroll.setObjectName("workspace_scroll")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 545, 478))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.workspace = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.workspace.setObjectName("workspace")
        self.formLayout = QtWidgets.QFormLayout(self.workspace)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName("formLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(0, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.verticalLayout_3.addWidget(self.workspace)
        self.workspace_scroll.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.workspace_scroll)
        self.validation_widget = QtWidgets.QWidget(Form)
        self.validation_widget.setObjectName("validation_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.validation_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.validate_button = QtWidgets.QPushButton(self.validation_widget)
        self.validate_button.setObjectName("validate_button")
        self.verticalLayout.addWidget(self.validate_button)
        self.cancel_button = QtWidgets.QPushButton(self.validation_widget)
        self.cancel_button.setObjectName("cancel_button")
        self.verticalLayout.addWidget(self.cancel_button)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.validation_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("Composite editor")
        self.validate_button.setText("Ok")
        self.cancel_button.setText("Cancel")

