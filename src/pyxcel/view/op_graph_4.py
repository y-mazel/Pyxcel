#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\op_graph.ui'
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
        Form.resize(587, 515)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.selecting_widget = QtGui.QWidget(Form)
        self.selecting_widget.setObjectName(_fromUtf8("selecting_widget"))
        self.selecting_layout = QtGui.QHBoxLayout(self.selecting_widget)
        self.selecting_layout.setMargin(0)
        self.selecting_layout.setSpacing(0)
        self.selecting_layout.setObjectName(_fromUtf8("selecting_layout"))
        self.data_label = QtGui.QLabel(self.selecting_widget)
        self.data_label.setEnabled(False)
        self.data_label.setObjectName(_fromUtf8("data_label"))
        self.selecting_layout.addWidget(self.data_label)
        self.choose_data_combo = QtGui.QComboBox(self.selecting_widget)
        self.choose_data_combo.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_data_combo.sizePolicy().hasHeightForWidth())
        self.choose_data_combo.setSizePolicy(sizePolicy)
        self.choose_data_combo.setObjectName(_fromUtf8("choose_data_combo"))
        self.selecting_layout.addWidget(self.choose_data_combo)
        self.verticalLayout.addWidget(self.selecting_widget)
        self.fom_widget = QtGui.QWidget(Form)
        self.fom_widget.setObjectName(_fromUtf8("fom_widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.fom_widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.fom_selector = QtGui.QComboBox(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_selector.sizePolicy().hasHeightForWidth())
        self.fom_selector.setSizePolicy(sizePolicy)
        self.fom_selector.setObjectName(_fromUtf8("fom_selector"))
        self.horizontalLayout.addWidget(self.fom_selector)
        self.fom_label = QtGui.QLabel(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_label.sizePolicy().hasHeightForWidth())
        self.fom_label.setSizePolicy(sizePolicy)
        self.fom_label.setObjectName(_fromUtf8("fom_label"))
        self.horizontalLayout.addWidget(self.fom_label)
        self.fom_line = QtGui.QLineEdit(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_line.sizePolicy().hasHeightForWidth())
        self.fom_line.setSizePolicy(sizePolicy)
        self.fom_line.setObjectName(_fromUtf8("fom_line"))
        self.horizontalLayout.addWidget(self.fom_line)
        self.verticalLayout.addWidget(self.fom_widget)
        self.data_treatment_widget = QtGui.QWidget(Form)
        self.data_treatment_widget.setObjectName(_fromUtf8("data_treatment_widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.data_treatment_widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.data_treatment_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.data_treatment_button = QtGui.QPushButton(self.data_treatment_widget)
        self.data_treatment_button.setObjectName(_fromUtf8("data_treatment_button"))
        self.horizontalLayout_2.addWidget(self.data_treatment_button)
        self.verticalLayout.addWidget(self.data_treatment_widget)
        self.widget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.main_layout = QtGui.QVBoxLayout(self.widget)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(_fromUtf8("main_layout"))
        self.main_widget = QtGui.QWidget(self.widget)
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.main_layout.addWidget(self.main_widget)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Operation graph")
        self.data_label.setText("Data to visualize: ")
        self.label.setText("FOM formula: ")
        self.fom_label.setText("FOM: ")
        self.label_2.setText("Data processing: ")
        self.data_treatment_button.setText("Select operation: ")

