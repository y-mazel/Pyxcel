#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fast_sim.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_speed_sim(object):
    def setupUi(self, speed_sim):
        speed_sim.setObjectName("speed_sim")
        speed_sim.resize(352, 217)
        self.verticalLayout = QtWidgets.QVBoxLayout(speed_sim)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(speed_sim)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.instrument_combo = QtWidgets.QComboBox(self.widget)
        self.instrument_combo.setObjectName("instrument_combo")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.instrument_combo)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.model_combo = QtWidgets.QComboBox(self.widget)
        self.model_combo.setObjectName("model_combo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.model_combo)
        self.verticalLayout.addWidget(self.widget)
        self.option_widget = QtWidgets.QWidget(speed_sim)
        self.option_widget.setObjectName("option_widget")
        self.option_layout = QtWidgets.QVBoxLayout(self.option_widget)
        self.option_layout.setContentsMargins(0, 0, 0, 0)
        self.option_layout.setSpacing(0)
        self.option_layout.setObjectName("option_layout")
        self.verticalLayout.addWidget(self.option_widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.widget_2 = QtWidgets.QWidget(speed_sim)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.simulate_button = QtWidgets.QPushButton(self.widget_2)
        self.simulate_button.setObjectName("simulate_button")
        self.horizontalLayout.addWidget(self.simulate_button)
        spacerItem1 = QtWidgets.QSpacerItem(232, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(speed_sim)
        QtCore.QMetaObject.connectSlotsByName(speed_sim)

    def retranslateUi(self, speed_sim):
        _translate = QtCore.QCoreApplication.translate
        speed_sim.setWindowTitle("Fast simulator")
        self.label.setText("Instrument: ")
        self.label_2.setText("Model: ")
        self.simulate_button.setText("Simulate")

