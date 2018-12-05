#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\instrument_editor_basic.ui'
#
# Created: Wed Aug 05 08:51:02 2015
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
        Form.resize(640, 480)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.source_box = QtGui.QGroupBox(Form)
        self.source_box.setObjectName(_fromUtf8("source_box"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.source_box)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout.addWidget(self.source_box)
        self.detector_box = QtGui.QGroupBox(Form)
        self.detector_box.setObjectName(_fromUtf8("detector_box"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.detector_box)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.verticalLayout.addWidget(self.detector_box)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.source_box.setTitle(_translate("Form", "source:", None))
        self.detector_box.setTitle(_translate("Form", "detector:", None))

