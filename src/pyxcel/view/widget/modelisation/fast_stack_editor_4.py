#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fast_stack_editor.ui'
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
        Form.resize(524, 410)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.layer_table = QtGui.QTableWidget(Form)
        self.layer_table.setObjectName(_fromUtf8("layer_table"))
        self.layer_table.setColumnCount(6)
        self.layer_table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        item.setFont(font)
        self.layer_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.layer_table)
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.save_button = QtGui.QPushButton(self.widget)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.horizontalLayout.addWidget(self.save_button)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.sample_len_edit = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sample_len_edit.sizePolicy().hasHeightForWidth())
        self.sample_len_edit.setSizePolicy(sizePolicy)
        self.sample_len_edit.setObjectName(_fromUtf8("sample_len_edit"))
        self.horizontalLayout.addWidget(self.sample_len_edit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.simulate_button = QtGui.QPushButton(self.widget)
        self.simulate_button.setObjectName(_fromUtf8("simulate_button"))
        self.horizontalLayout.addWidget(self.simulate_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Fast stack editor")
        item = self.layer_table.horizontalHeaderItem(0)
        item.setText("Name")
        item = self.layer_table.horizontalHeaderItem(1)
        item.setText("Material")
        item = self.layer_table.horizontalHeaderItem(2)
        item.setText("Thickness (A)")
        item = self.layer_table.horizontalHeaderItem(3)
        item.setText("Numerical density (A-3)")
        item = self.layer_table.horizontalHeaderItem(4)
        item.setText("Mass density (g.cm-3)")
        item = self.layer_table.horizontalHeaderItem(5)
        item.setText("Roughness (A)")
        self.save_button.setText("Save")
        self.label.setText("Sample size")
        self.simulate_button.setText("Simulation")

