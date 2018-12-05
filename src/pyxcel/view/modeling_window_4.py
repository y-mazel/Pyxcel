#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\modeling_window_simple.ui'
#
# Created: Fri Jun 05 15:32:49 2015
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

class Ui_modeling_window(object):
    def setupUi(self, modeling_window):
        modeling_window.setObjectName(_fromUtf8("modeling_window"))
        modeling_window.resize(585, 458)
        self.main_layout = QtGui.QVBoxLayout(modeling_window)
        self.main_layout.setObjectName(_fromUtf8("main_layout"))
        self.main_widget = QtGui.QWidget(modeling_window)
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(20, 375, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.main_layout.addWidget(self.main_widget)

        self.retranslateUi(modeling_window)
        QtCore.QMetaObject.connectSlotsByName(modeling_window)

    def retranslateUi(self, modeling_window):
        modeling_window.setWindowTitle("Modeling window")

