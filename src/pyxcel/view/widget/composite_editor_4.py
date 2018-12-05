#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\composite_editor2.ui'
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
        Form.resize(640, 480)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.workspace_scroll = QtGui.QScrollArea(Form)
        self.workspace_scroll.setFrameShadow(QtGui.QFrame.Raised)
        self.workspace_scroll.setWidgetResizable(True)
        self.workspace_scroll.setObjectName(_fromUtf8("workspace_scroll"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 545, 478))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.workspace = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.workspace.setObjectName(_fromUtf8("workspace"))
        self.formLayout = QtGui.QFormLayout(self.workspace)
        self.formLayout.setMargin(0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtGui.QFormLayout.FieldRole, spacerItem)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout.setItem(0, QtGui.QFormLayout.FieldRole, spacerItem1)
        self.verticalLayout_3.addWidget(self.workspace)
        self.workspace_scroll.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.workspace_scroll)
        self.validation_widget = QtGui.QWidget(Form)
        self.validation_widget.setObjectName(_fromUtf8("validation_widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.validation_widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.validate_button = QtGui.QPushButton(self.validation_widget)
        self.validate_button.setObjectName(_fromUtf8("validate_button"))
        self.verticalLayout.addWidget(self.validate_button)
        self.cancel_button = QtGui.QPushButton(self.validation_widget)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.verticalLayout.addWidget(self.cancel_button)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout.addWidget(self.validation_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Composite editor")
        self.validate_button.setText("Ok")
        self.cancel_button.setText("Cancel")

