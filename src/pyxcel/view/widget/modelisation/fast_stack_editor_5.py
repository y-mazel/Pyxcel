#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fast_stack_editor.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(524, 410)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layer_table = QtWidgets.QTableWidget(Form)
        self.layer_table.setObjectName("layer_table")
        self.layer_table.setColumnCount(6)
        self.layer_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        item.setFont(font)
        self.layer_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.layer_table.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.layer_table)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_button = QtWidgets.QPushButton(self.widget)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.sample_len_edit = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sample_len_edit.sizePolicy().hasHeightForWidth())
        self.sample_len_edit.setSizePolicy(sizePolicy)
        self.sample_len_edit.setObjectName("sample_len_edit")
        self.horizontalLayout.addWidget(self.sample_len_edit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.simulate_button = QtWidgets.QPushButton(self.widget)
        self.simulate_button.setObjectName("simulate_button")
        self.horizontalLayout.addWidget(self.simulate_button)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.layer_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Nom"))
        item = self.layer_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Matériau"))
        item = self.layer_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Epaisseur"))
        item = self.layer_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Densité numérique"))
        item = self.layer_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Densité massique"))
        item = self.layer_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Rugosité"))
        self.save_button.setText(_translate("Form", "Sauver"))
        self.label.setText(_translate("Form", "Taille d\'échantillon :"))
        self.simulate_button.setText(_translate("Form", "Simulation"))

