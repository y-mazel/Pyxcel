#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\analysis_window.ui'
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

class Ui_analysis_windows(object):
    def setupUi(self, analysis_windows):
        analysis_windows.setObjectName(_fromUtf8("analysis_windows"))
        analysis_windows.resize(586, 685)
        self.verticalLayout = QtGui.QVBoxLayout(analysis_windows)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(analysis_windows)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.choose_data_combo = QtGui.QComboBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_data_combo.sizePolicy().hasHeightForWidth())
        self.choose_data_combo.setSizePolicy(sizePolicy)
        self.choose_data_combo.setObjectName(_fromUtf8("choose_data_combo"))
        self.horizontalLayout.addWidget(self.choose_data_combo)
        self.add_sim_button = QtGui.QPushButton(self.widget)
        self.add_sim_button.setObjectName(_fromUtf8("add_sim_button"))
        self.horizontalLayout.addWidget(self.add_sim_button)
        self.add_data_button = QtGui.QPushButton(self.widget)
        self.add_data_button.setObjectName(_fromUtf8("add_data_button"))
        self.horizontalLayout.addWidget(self.add_data_button)
        self.clear_button = QtGui.QPushButton(self.widget)
        self.clear_button.setObjectName(_fromUtf8("clear_button"))
        self.horizontalLayout.addWidget(self.clear_button)
        self.verticalLayout.addWidget(self.widget)
        self.export_widget = QtGui.QWidget(analysis_windows)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.export_widget.sizePolicy().hasHeightForWidth())
        self.export_widget.setSizePolicy(sizePolicy)
        self.export_widget.setObjectName(_fromUtf8("export_widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.export_widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.export_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.copy_select_button = QtGui.QPushButton(self.export_widget)
        self.copy_select_button.setObjectName(_fromUtf8("copy_select_button"))
        self.horizontalLayout_2.addWidget(self.copy_select_button)
        self.copy_data_button = QtGui.QPushButton(self.export_widget)
        self.copy_data_button.setObjectName(_fromUtf8("copy_data_button"))
        self.horizontalLayout_2.addWidget(self.copy_data_button)
        self.save_data_button = QtGui.QPushButton(self.export_widget)
        self.save_data_button.setObjectName(_fromUtf8("save_data_button"))
        self.horizontalLayout_2.addWidget(self.save_data_button)
        self.verticalLayout.addWidget(self.export_widget)
        self.fom_widget = QtGui.QWidget(analysis_windows)
        self.fom_widget.setObjectName(_fromUtf8("fom_widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.fom_widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.fom_selector = QtGui.QComboBox(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_selector.sizePolicy().hasHeightForWidth())
        self.fom_selector.setSizePolicy(sizePolicy)
        self.fom_selector.setObjectName(_fromUtf8("fom_selector"))
        self.horizontalLayout_4.addWidget(self.fom_selector)
        self.fom_label = QtGui.QLabel(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_label.sizePolicy().hasHeightForWidth())
        self.fom_label.setSizePolicy(sizePolicy)
        self.fom_label.setObjectName(_fromUtf8("fom_label"))
        self.horizontalLayout_4.addWidget(self.fom_label)
        self.fom_line = QtGui.QLineEdit(self.fom_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fom_line.sizePolicy().hasHeightForWidth())
        self.fom_line.setSizePolicy(sizePolicy)
        self.fom_line.setObjectName(_fromUtf8("fom_line"))
        self.horizontalLayout_4.addWidget(self.fom_line)
        self.verticalLayout.addWidget(self.fom_widget)
        self.widget_2 = QtGui.QWidget(analysis_windows)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.main_layout = QtGui.QVBoxLayout(self.widget_2)
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(_fromUtf8("main_layout"))
        self.main_widget = QtGui.QWidget(self.widget_2)
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.main_widget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.main_layout.addWidget(self.main_widget)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(analysis_windows)
        QtCore.QMetaObject.connectSlotsByName(analysis_windows)

    def retranslateUi(self, analysis_windows):
        analysis_windows.setWindowTitle("Analysis window")
        self.label.setText("Data to visualize: ")
        self.add_sim_button.setText("Add a simulation")
        self.add_data_button.setText("Add data")
        self.clear_button.setText("Clean")
        self.label_2.setText("Export")
        self.copy_select_button.setText("Copy selection")
        self.copy_data_button.setText("Copy to clipboard")
        self.save_data_button.setText("Export to file")
        self.label_4.setText("FOM formula: ")
        self.fom_label.setText("FOM")

