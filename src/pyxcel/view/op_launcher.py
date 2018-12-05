# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for launch a new operation.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
from pyxcel.view.mdi_window import MDIWindow
import pyxcel.engine.pipeline
import pyxcel.engine.modeling.pumps
import paf.data
import pyxcel.view.widget.composite_editor as composite_editor
import pyxcel.view.widget.list_editor as list_editor
import pyxcel.engine.centralizer
import pyxcel.view.widget.operation.tab_editor as tab_editor
import pyxcel.view.widget.operation.line_editor as line_editor
from pyxcel.view.cute import QWidget, QHBoxLayout, QLabel, QSpacerItem
from pyxcel.view.cute import QSizePolicy, QComboBox, QPushButton, QCheckBox
from pyxcel.view.cute import QApplication
try:
    import pyxcel.view.op_launcher_4 as former
except ImportError:
    import pyxcel.view.op_launcher_5 as former
MAKE_DATA = paf.data.make_data

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class EntityChoiceField(QWidget):
    """ Special filed to link entity in database and entity pump
    """
    def __init__(self, parent, name, entity_pump):
        """ initialization

        :param parent: parent Widget
        :type parent: QWidget
        :param name: name of field
        :type name: str
        :param entity_pump: entity pump to link
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._c = pyxcel.engine.centralizer.Centralizer()
        self._name = name
        self._entity_pump = entity_pump
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._type = self._entity_pump.entity_type
        self._validate = False
        self.create_structure()

    def refresh(self):
        """ refresh the view
        """
        self._comboBox.clear()
        for element_name in self._c.database.keys():
            if isinstance(self._c.database[uni(element_name)], self._type):
                self._comboBox.addItem(element_name)

    def create_structure(self):
        """ create the view
        """
        label = QLabel()
        label.setObjectName(self._name + '_label')
        label.setText(self._name)
        self._layout.addWidget(label)
        self._comboBox = QComboBox(self)
        self._comboBox.setObjectName("comboBox")
        self._layout.addWidget(self._comboBox)
        self._button = QPushButton("Ok", self)
        self._button.clicked.connect(self.validator)
        self._layout.addWidget(self._button)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        self._layout.addItem(spacerItem)
        self.refresh()

    @property
    def current_text(self):
        """ return the chosen value

        :return: current value
        :rtype: str
        """
        return self._comboBox.currentText()

    def validator(self):
        """ slot for clicking on validate button
        """
        self.validate = True

    @property
    def validate(self):
        """ property to access to the validation status of field
        """
        return self._validate

    @validate.setter
    def validate(self, value):
        """ assign the current value to the pump
        """
        if value:
            self._selected_value = uni(self._comboBox.currentText())
            self._entity_pump["el_name"] = self._selected_value
            self._entity_pump.data = self._c.database[self._selected_value]
        self._validate = value
        self._parent.data.validate(self._name)

    @property
    def selected_value(self):
        """ return the selected value if the field is validate
        """
        if self._validate:
            return self._selected_value
        else:
            return None


class OperationLauncher(MDIWindow):
    """ widget to configure and launch operation
    """

    #: list of widget for some abstract type
    abstract_type = {"tab_data": tab_editor.TabEditor,
                     "line": line_editor.LineEditor}

    #: list of widget for some type
    type_widget = {dict: composite_editor.CompositeEditor,
                   list: list_editor.ListEditor}

    def __init__(self, parent):
        """ initialization

        :param parent: parent widget
        :type parent: QWidget
        :param controller: controller to modify model
        """
        MDIWindow.__init__(self, parent, former.Ui_op_launcher())
        self._input_field = {}
        self._name = ""
        self._checkBox = {}
        self._c = pyxcel.engine.centralizer.Centralizer()

        self._input_tab = self.findChild(QWidget, "input_tab")
        self._parameter_tab = self.findChild(QWidget, "parameter_tab")
        self._output_tab = self.findChild(QWidget, "output_tab")

        self._parametre_button_list = self.findChild(QWidget, "button_list")
        self._data_parameter = self.findChild(QWidget, "data_parameter")

        button_start = self.findChild(QPushButton, "start_op_push_button")
        button_start.clicked.connect(self.launch)

    @staticmethod
    def clear_element(layout):
        """ clear all element on a layout.
        """
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget() is not None:
                layout.itemAt(i).widget().setParent(None)
            else:
                layout.removeItem(layout.itemAt(i))

    def open_parameter_editor(self, name):
        """ open the named parameterizable with editor

        :param name: name of the parameterizable to edit
        :type name: str
        """
        self.clear_element(self._data_parameter.layout())
        data_composite = self._data.modifiable[name].to_composite_data()
        self._editor = composite_editor.CompositeEditor(self, data_composite)
        self._data_parameter.layout().addWidget(self._editor)

    def create_parametre(self):
        """ create list of button to access at filter parameter.
        """
        def create_editor_slot(name):
            """ create slot for editing value
            """
            def f():
                """ slot for editing value
                """
                self.clear_history()
                self.open_parameter_editor(name)
            return f
        for modifiable in list(self._data.modifiable.keys()):
            new_pushButton = QPushButton(self._parametre_button_list)
            new_pushButton.setText(modifiable)
            self._parametre_button_list.layout().addWidget(new_pushButton)
            new_pushButton.clicked.connect(create_editor_slot(modifiable))
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                  QSizePolicy.Expanding)
        self._parametre_button_list.layout().addItem(spacer_item)
        spacer_item = QSpacerItem(40, 40, QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self._data_parameter.layout().addItem(spacer_item)

    def refresh(self):
        """ refresh the list of input field. *use at every modification in
        database*
        """
        for (_, field) in self._input_field.items():
            field.refresh()

    def clear(self):
        """ clear all tabs
        """
        self.clear_element(self._input_tab.layout())
        self.clear_element(self._parametre_button_list.layout())
        self.clear_element(self._data_parameter.layout())
        self.clear_element(self._output_tab.layout())
        self.clear_history()

    def record(self, name):
        """ create auto record slot.
        """
        op_name = self._name

        def auto_record(data):
            """ new auto record lot
            """
            entity_list = {}
            for (field_name, field) in self._input_field.items():
                entity_list[field_name] = field.selected_value
            self._c.controller.add_result(data, op_name, entity_list, name)
        return auto_record

    def create_auto_connector(self, name, plug_sink):
        """ create a chooser for recording.
        """
        def connector(value):
            """ choose for recording
            """
            if value == 2:
                plug_sink.connect_to_signal(self.record(name))
            else:
                plug_sink.disconnect()
        return connector

    def create_check_recordable(self):
        """ create a check box for every recordable element
        """
        try:
            recordable = self._data.recordable
            for (name, value) in recordable.items():
                checkbox = QCheckBox(self._output_tab)
                self._checkBox[name] = checkbox
                checkbox.setObjectName(name + "_label")
                checkbox.setText(name)
                checkbox.stateChanged.connect(self.create_auto_connector(name,
                                                                         value)
                                              )
                value.disconnect()
                self._output_tab.layout().addWidget(checkbox)
            spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                     QSizePolicy.Expanding)
            self._output_tab.layout().addItem(spacerItem)
        except:
            pass

    def go_back(self):
        """ redefine go back function for parameter part.
        """
        self._editor.setParent(None)
        if len(self._history) > 0:
            self._editor = self._history.pop()
        self._data_parameter.layout().addWidget(self._editor)

    @property
    def data(self):
        """ property to access to the data
        """
        return self._data

    @data.setter
    def data(self, name):
        """ setter for data property
        """
        try:
            data = self._c.database.get_operation(uni(name))[0]
            self._name = name
        except KeyError:
            data = name
        if isinstance(data, pyxcel.engine.pipeline.Pipeline):
            self._data = data
            self.clear()
            for (key, element) in data.elements.items():
                if isinstance(element,
                              pyxcel.engine.modeling.pumps.EntityPump):
                    self._input_field[key] = EntityChoiceField(self, key,
                                                               element)
                    self._input_tab.layout().addWidget(self._input_field[key])
            self._c.database.connect_to_signal(self.refresh)
            spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                     QSizePolicy.Expanding)
            self._input_tab.layout().addItem(spacerItem)
            self.create_parametre()
            self.create_check_recordable()
        else:
            self._editor.setParent(None)
            self._history.append(self._editor)
            self.clear_element(self._data_parameter.layout())
            if data.abstract_type in list(self.abstract_type.keys()):
                widget_type = self.abstract_type[data.abstract_type]
            elif isinstance(data, paf.data.SimpleData):
                widget_type = composite_editor.CompositeEditor
            else:
                widget_type = self.type_widget[data.data_type]
            self._editor = widget_type(self, data)
            self._data_parameter.layout().addWidget(self._editor)

    def launch(self):
        """ lunch the current operation
        """
        for (_, field) in list(self._input_field.items()):
            field.validate = True
        self._c.controller.launch(self._name)

    @property
    def input_field(self):
        """ property to access to the list of input field
        """
        return self._input_field
