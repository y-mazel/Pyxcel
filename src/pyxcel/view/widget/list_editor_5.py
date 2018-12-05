#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\list_editor.ui'
#
# Created: Thu Jun 25 08:58:52 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(479, 463)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.list_widget = QtWidgets.QListWidget(Form)
        self.list_widget.setObjectName("list_widget")
        self.horizontalLayout.addWidget(self.list_widget)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.add_button = QtWidgets.QPushButton(self.widget)
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.del_button = QtWidgets.QPushButton(self.widget)
        self.del_button.setObjectName("del_button")
        self.verticalLayout.addWidget(self.del_button)
        self.mod_button = QtWidgets.QPushButton(self.widget)
        self.mod_button.setObjectName("mod_button")
        self.verticalLayout.addWidget(self.mod_button)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.up_button = QtWidgets.QPushButton(self.widget)
        self.up_button.setObjectName("up_button")
        self.verticalLayout.addWidget(self.up_button)
        self.down_button = QtWidgets.QPushButton(self.widget)
        self.down_button.setObjectName("down_button")
        self.verticalLayout.addWidget(self.down_button)
        self.validate_button = QtWidgets.QPushButton(self.widget)
        self.validate_button.setObjectName("validate_button")
        self.verticalLayout.addWidget(self.validate_button)
        self.cancel_button = QtWidgets.QPushButton(self.widget)
        self.cancel_button.setObjectName("cancel_button")
        self.verticalLayout.addWidget(self.cancel_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle("List editor")
        self.add_button.setText("Add")
        self.del_button.setText("Delete")
        self.mod_button.setText("Modify")
        self.up_button.setText("Move up")
        self.down_button.setText("Move down")
        self.validate_button.setText("Ok")
        self.cancel_button.setText("Cancel")

