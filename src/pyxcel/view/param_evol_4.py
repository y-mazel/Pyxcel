#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\param_evol.ui'
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
        Form.resize(503, 650)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.parameter_widget = QtGui.QTableWidget(Form)
        self.parameter_widget.setObjectName(_fromUtf8("parameter_widget"))
        self.parameter_widget.setColumnCount(5)
        self.parameter_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.parameter_widget.setHorizontalHeaderItem(4, item)
        self.verticalLayout.addWidget(self.parameter_widget)
        self.fom_widget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_widget.sizePolicy().hasHeightForWidth())
        self.fom_widget.setSizePolicy(sizePolicy)
        self.fom_widget.setObjectName(_fromUtf8("fom_widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.fom_widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout.addWidget(self.fom_widget)
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(401, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.corrcoef_button = QtGui.QPushButton(self.widget)
        self.corrcoef_button.setObjectName(_fromUtf8("corrcoef_button"))
        self.horizontalLayout.addWidget(self.corrcoef_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
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

