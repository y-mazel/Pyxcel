#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\fast_instrument_editor.ui'
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
        Form.resize(652, 346)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(Form)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.data_combo = QtGui.QComboBox(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_combo.sizePolicy().hasHeightForWidth())
        self.data_combo.setSizePolicy(sizePolicy)
        self.data_combo.setObjectName(_fromUtf8("data_combo"))
        self.horizontalLayout.addWidget(self.data_combo)
        self.add_button = QtGui.QPushButton(self.widget_2)
        self.add_button.setObjectName(_fromUtf8("add_button"))
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.editor_layout = QtGui.QHBoxLayout(self.widget)
        self.editor_layout.setMargin(0)
        self.editor_layout.setSpacing(0)
        self.editor_layout.setObjectName(_fromUtf8("editor_layout"))
        self.data_list = QtGui.QListWidget(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_list.sizePolicy().hasHeightForWidth())
        self.data_list.setSizePolicy(sizePolicy)
        self.data_list.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.data_list.setObjectName(_fromUtf8("data_list"))
        self.editor_layout.addWidget(self.data_list)
        self.widget_3 = QtGui.QWidget(self.widget)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.form_widget = QtGui.QWidget(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.form_widget.sizePolicy().hasHeightForWidth())
        self.form_widget.setSizePolicy(sizePolicy)
        self.form_widget.setObjectName(_fromUtf8("form_widget"))
        self.main_layout = QtGui.QVBoxLayout(self.form_widget)
        self.main_layout.setContentsMargins(5, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName(_fromUtf8("main_layout"))
        self.main_widget = QtGui.QWidget(self.form_widget)
        self.main_widget.setObjectName(_fromUtf8("main_widget"))
        self.main_layout.addWidget(self.main_widget)
        self.verticalLayout_2.addWidget(self.form_widget)
        self.widget_4 = QtGui.QWidget(self.widget_3)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(149, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.save_button = QtGui.QPushButton(self.widget_4)
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.horizontalLayout_2.addWidget(self.save_button)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.editor_layout.addWidget(self.widget_3)
        self.verticalLayout.addWidget(self.widget)
        self.delete_data_action = QtGui.QAction(Form)
        self.delete_data_action.setObjectName(_fromUtf8("delete_data_action"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Fast instrument editor")
        self.label.setText("Data file : ")
        self.add_button.setText("Add")
        self.save_button.setText("Save")
        self.delete_data_action.setText("Delete")

