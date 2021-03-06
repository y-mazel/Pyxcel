#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\analysis_window.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_analysis_windows(object):
    def setupUi(self, analysis_windows):
        analysis_windows.setObjectName("analysis_windows")
        analysis_windows.resize(586, 685)
        self.verticalLayout = QtWidgets.QVBoxLayout(analysis_windows)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(analysis_windows)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.choose_data_combo = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_data_combo.sizePolicy().hasHeightForWidth())
        self.choose_data_combo.setSizePolicy(sizePolicy)
        self.choose_data_combo.setObjectName("choose_data_combo")
        self.horizontalLayout.addWidget(self.choose_data_combo)
        self.add_sim_button = QtWidgets.QPushButton(self.widget)
        self.add_sim_button.setObjectName("add_sim_button")
        self.horizontalLayout.addWidget(self.add_sim_button)
        self.add_data_button = QtWidgets.QPushButton(self.widget)
        self.add_data_button.setObjectName("add_data_button")
        self.horizontalLayout.addWidget(self.add_data_button)
        self.clear_button = QtWidgets.QPushButton(self.widget)
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout.addWidget(self.clear_button)
        self.verticalLayout.addWidget(self.widget)
        self.export_widget = QtWidgets.QWidget(analysis_windows)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_widget.sizePolicy().hasHeightForWidth())
        self.export_widget.setSizePolicy(sizePolicy)
        self.export_widget.setObjectName("export_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.export_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.export_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.copy_select_button = QtWidgets.QPushButton(self.export_widget)
        self.copy_select_button.setObjectName("copy_select_button")
        self.horizontalLayout_2.addWidget(self.copy_select_button)
        self.copy_data_button = QtWidgets.QPushButton(self.export_widget)
        self.copy_data_button.setObjectName("copy_data_button")
        self.horizontalLayout_2.addWidget(self.copy_data_button)
        self.save_data_button = QtWidgets.QPushButton(self.export_widget)
        self.save_data_button.setObjectName("save_data_button")
        self.horizontalLayout_2.addWidget(self.save_data_button)
        self.verticalLayout.addWidget(self.export_widget)
        self.fom_widget = QtWidgets.QWidget(analysis_windows)
        self.fom_widget.setObjectName("fom_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.fom_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.fom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.fom_selector = QtWidgets.QComboBox(self.fom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_selector.sizePolicy().hasHeightForWidth())
        self.fom_selector.setSizePolicy(sizePolicy)
        self.fom_selector.setObjectName("fom_selector")
        self.horizontalLayout_4.addWidget(self.fom_selector)
        self.fom_label = QtWidgets.QLabel(self.fom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_label.sizePolicy().hasHeightForWidth())
        self.fom_label.setSizePolicy(sizePolicy)
        self.fom_label.setObjectName("fom_label")
        self.horizontalLayout_4.addWidget(self.fom_label)
        self.fom_line = QtWidgets.QLineEdit(self.fom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_line.sizePolicy().hasHeightForWidth())
        self.fom_line.setSizePolicy(sizePolicy)
        self.fom_line.setObjectName("fom_line")
        self.horizontalLayout_4.addWidget(self.fom_line)
        self.verticalLayout.addWidget(self.fom_widget)
        self.widget_2 = QtWidgets.QWidget(analysis_windows)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName("widget_2")
        self.main_layout = QtWidgets.QVBoxLayout(self.widget_2)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.main_widget = QtWidgets.QWidget(self.widget_2)
        self.main_widget.setObjectName("main_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.main_layout.addWidget(self.main_widget)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(analysis_windows)
        QtCore.QMetaObject.connectSlotsByName(analysis_windows)

    def retranslateUi(self, analysis_windows):
        _translate = QtCore.QCoreApplication.translate
        analysis_windows.setWindowTitle("Analysis window")
        self.label.setText("Data to visualize: ")
        self.add_sim_button.setText("Add a simulation")
        self.add_data_button.setText("Add data")
        self.clear_button.setText("Clean")
        self.label_2.setText("Export")
        self.copy_select_button.setText("Copy selection")
        self.copy_data_button.setText("Copy")
        self.save_data_button.setText("Save")
        self.label_4.setText("FOM formula: ")
        self.fom_label.setText("FOM: ")

