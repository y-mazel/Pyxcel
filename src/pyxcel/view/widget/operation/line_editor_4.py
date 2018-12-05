#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\line_editor.ui'
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
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout_2 = QtGui.QFormLayout(self.widget)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setSpacing(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.element_combo = QtGui.QComboBox(self.widget)
        self.element_combo.setObjectName(_fromUtf8("element_combo"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.element_combo)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_2)
        self.line_combo = QtGui.QComboBox(self.widget)
        self.line_combo.setObjectName(_fromUtf8("line_combo"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.line_combo)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.formLayout_2.setItem(5, QtGui.QFormLayout.FieldRole, spacerItem)
        self.horizontalLayout.addWidget(self.widget)
        self.validate_widget = QtGui.QWidget(Form)
        self.validate_widget.setObjectName(_fromUtf8("validate_widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.validate_widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.validate_button = QtGui.QPushButton(self.validate_widget)
        self.validate_button.setObjectName(_fromUtf8("validate_button"))
        self.verticalLayout.addWidget(self.validate_button)
        self.cancel_button = QtGui.QPushButton(self.validate_widget)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.verticalLayout.addWidget(self.cancel_button)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.validate_widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Line editor")
        self.label.setText("Element: ")
        self.label_2.setText("Line: ")
        self.validate_button.setText("Ok")
        self.cancel_button.setText("Cancel")

