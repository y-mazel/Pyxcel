#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fast_sim.ui'
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

class Ui_speed_sim(object):
    def setupUi(self, speed_sim):
        speed_sim.setObjectName(_fromUtf8("speed_sim"))
        speed_sim.resize(352, 217)
        self.verticalLayout = QtGui.QVBoxLayout(speed_sim)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(speed_sim)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.instrument_combo = QtGui.QComboBox(self.widget)
        self.instrument_combo.setObjectName(_fromUtf8("instrument_combo"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.instrument_combo)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.model_combo = QtGui.QComboBox(self.widget)
        self.model_combo.setObjectName(_fromUtf8("model_combo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.model_combo)
        self.verticalLayout.addWidget(self.widget)
        self.option_widget = QtGui.QWidget(speed_sim)
        self.option_widget.setObjectName(_fromUtf8("option_widget"))
        self.option_layout = QtGui.QVBoxLayout(self.option_widget)
        self.option_layout.setMargin(0)
        self.option_layout.setSpacing(0)
        self.option_layout.setObjectName(_fromUtf8("option_layout"))
        self.verticalLayout.addWidget(self.option_widget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.widget_2 = QtGui.QWidget(speed_sim)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.simulate_button = QtGui.QPushButton(self.widget_2)
        self.simulate_button.setObjectName(_fromUtf8("simulate_button"))
        self.horizontalLayout.addWidget(self.simulate_button)
        spacerItem1 = QtGui.QSpacerItem(232, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(speed_sim)
        QtCore.QMetaObject.connectSlotsByName(speed_sim)

    def retranslateUi(self, speed_sim):
        speed_sim.setWindowTitle("Fast simulator")
        self.label.setText("Instrument: ")
        self.label_2.setText("Model: ")
        self.simulate_button.setText("Simulate")

