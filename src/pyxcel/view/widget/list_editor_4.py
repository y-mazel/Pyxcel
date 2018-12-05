#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\list_editor.ui'
#
# Created: Thu Jun 25 08:58:43 2015
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(479, 463)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.list_widget = QtGui.QListWidget(Form)
        self.list_widget.setObjectName(_fromUtf8("list_widget"))
        self.horizontalLayout.addWidget(self.list_widget)
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.add_button = QtGui.QPushButton(self.widget)
        self.add_button.setObjectName(_fromUtf8("add_button"))
        self.verticalLayout.addWidget(self.add_button)
        self.del_button = QtGui.QPushButton(self.widget)
        self.del_button.setObjectName(_fromUtf8("del_button"))
        self.verticalLayout.addWidget(self.del_button)
        self.mod_button = QtGui.QPushButton(self.widget)
        self.mod_button.setObjectName(_fromUtf8("mod_button"))
        self.verticalLayout.addWidget(self.mod_button)
        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.up_button = QtGui.QPushButton(self.widget)
        self.up_button.setObjectName(_fromUtf8("up_button"))
        self.verticalLayout.addWidget(self.up_button)
        self.down_button = QtGui.QPushButton(self.widget)
        self.down_button.setObjectName(_fromUtf8("down_button"))
        self.verticalLayout.addWidget(self.down_button)
        self.validate_button = QtGui.QPushButton(self.widget)
        self.validate_button.setObjectName(_fromUtf8("validate_button"))
        self.verticalLayout.addWidget(self.validate_button)
        self.cancel_button = QtGui.QPushButton(self.widget)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.verticalLayout.addWidget(self.cancel_button)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("List editor")
        self.add_button.setText("Add")
        self.del_button.setText("Delete")
        self.mod_button.setText("Modify")
        self.up_button.setText("Move up")
        self.down_button.setText("Move down")
        self.validate_button.setText("Ok")
        self.cancel_button.setText("Cancel")

