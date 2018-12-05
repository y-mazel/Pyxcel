# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for configuring IO and launch a new operation.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
from pyxcel.view.mdi_window import MDIWindow
import pyxcel.view.op_graph
import pyxcel.view.widget.modelisation.fast_stack_editor as fast_stack_editor
import pyxcel.engine.modeling.entity as entity
import pyxcel.engine.centralizer
import pyxcel.view.op_parameter_lite as op_parameter_lite
import pyxcel.view.widget.modelisation.fast_instrument_editor as fast_inst_ed
from pyxcel.view.cute import QWidget, QHBoxLayout, QLabel, QSpacerItem
from pyxcel.view.cute import QComboBox, QPushButton, QErrorMessage
from pyxcel.view.cute import QMdiArea, QSizePolicy, QInputDialog, QApplication
try:
    import pyxcel.view.op_io_4 as former
except ImportError:
    import pyxcel.view.op_io_5 as former

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig=None):
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
        self._data_editor = None
        self.create_structure()

    @property
    def data_editor(self):
        """ link to the widget for editing data
        """
        return self._data_editor

    @data_editor.setter
    def data_editor(self, value):
        self._data_editor = value
        self.refresh()

    def refresh(self):
        """ refresh the view
        """
        self._comboBox.clear()
        for element_name in self._c.database.keys():
            if isinstance(self._c.database[uni(element_name)], self._type):
                self._comboBox.addItem(element_name)
        if self._entity_pump.validate:
            index = self._comboBox.findText(self._entity_pump.entity_name)
            self._comboBox.setCurrentIndex(index)
            self._comboBox.setEnabled(False)
            if self.data_editor is not None:
                self.data_editor.set_data(self._entity_pump.data)

    @property
    def entity_pump(self):
        """ accessing to entity pump
        """
        return self._entity_pump

    def create_structure(self):
        """ create the view
        """
        label = QLabel()
        label.setObjectName(self._name + '_label')
        label.setText(self._name)
        self._layout.addWidget(label)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self._comboBox = QComboBox(self)
        sizePolicy.setHeightForWidth(self._comboBox.sizePolicy().
                                     hasHeightForWidth())
        self._comboBox.setSizePolicy(sizePolicy)
        self._comboBox.setObjectName("comboBox")
        self._layout.addWidget(self._comboBox)
        self._button = QPushButton("valider", self)
        self._button.clicked.connect(self.validator)
        self._layout.addWidget(self._button)
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
            if self._entity_pump.data is None:
                self._entity_pump.data = self._selected_value
            self.refresh()
        self._validate = value

    @property
    def selected_value(self):
        """ return the selected value if the field is validate
        """
        if self._validate:
            return self._selected_value
        else:
            return None


class OperationIO(MDIWindow):
    """ widget to configure IO and launch operation
    """

    def __init__(self, parent):
        """ initialization

        :param parent: parent widget
        :type parent: QWidget
        :param controller: controller to modify model
        """
        MDIWindow.__init__(self, parent, former.Ui_Form())
        self._parent = parent
        self._input_field = {}
        #: operation name
        self._name = ""
        self._c = pyxcel.engine.centralizer.Centralizer()
        self._error_msg = QErrorMessage()
        self._last_selected_view = None
        self._active_stack = None
        self._active_stack_editor = None
        self._exp_data_select = None

        self._input_widget = self.findChild(QWidget, "input_widget")

        launch_button = self.findChild(QPushButton, "launch_button")
        launch_button.clicked.connect(self.launch)

        parameter_button = self.findChild(QPushButton, "parameter_button")
        parameter_button.clicked.connect(self.open_parameter)

        graph_button = self.findChild(QPushButton, "graph_button")
        graph_button.clicked.connect(self.open_new_graph)

        reset_button = self.findChild(QPushButton, "reset_button")
        reset_button.clicked.connect(self.reset_op)

        save_button = self.findChild(QPushButton, "save_button")
        save_button.clicked.connect(self.save_result)

        self._resultat_widget = self.findChild(QWidget, "resultat_widget")
        self._resultat_widget.hide()

    @property
    def selected_exp_data(self):
        """ return selected experimental dataset
        """
        return self._exp_data_select

    @selected_exp_data.setter
    def selected_exp_data(self, value):
        """ setter for selected experimental dataset
        """
        self._exp_data_select = value

    @property
    def active_stack_editor(self):
        """ return the active stack editor
        """
        return self._active_stack_editor

    @active_stack_editor.setter
    def active_stack_editor(self, value):
        """ seting for active stack editor
        """
        self._active_stack_editor = value

    @property
    def active_stack(self):
        """ accessing to the active stack
        """
        return self._active_stack

    @active_stack.setter
    def active_stack(self, value):
        """ setting the active stack
        """
        self._active_stack = value

    @property
    def last_selected_view(self):
        """ accessing to the last selected view
        """
        return self._last_selected_view

    @last_selected_view.setter
    def last_selected_view(self, new_view):
        """ stter for last_selected_view
        """
        self._last_selected_view = new_view

    @staticmethod
    def clear_element(layout):
        """ clear all element on a layout.
        """
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget() is not None:
                layout.itemAt(i).widget().setParent(None)
            else:
                layout.removeItem(layout.itemAt(i))

    @property
    def data(self):
        """ property to access to the data
        """
        return self._data

    @data.setter
    def data(self, name):
        """ setter for data property
        """
        self._data_field = None
        self._input_field = {}
        if name is None:
            self.clear()
        try:
            data = self._c.database.get_operation(uni(name))[0]
            if data.result is None:
                self._resultat_widget.hide()
            else:
                self._resultat_widget.show()
            self._name = name
            self._data = data
            self.clear()
            if data.nb_data_max != 0:
                self.create_fast_inst()
            for key in sorted(list(data.entity_pump.keys())):
                element = data.entity_pump[key]
                self.add_entity_choice_field(key, element)
            self._c.database.connect_to_signal(self.refresh)
            spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                     QSizePolicy.Expanding)
            self._input_widget.layout().addItem(spacerItem)
        except KeyError:
            pass

    @property
    def data_field(self):
        """ property to access to data field
        """
        return self._data_field

    @property
    def input_field(self):
        """ property to access to the list of input field
        """
        return self._input_field

    def save_result(self):
        """ slot for saving result
        """
        message = "Name"
        title = "Save result"
        result = QInputDialog.getText(self, title, message)
        if result[1]:
            self._data.result.name = uni(result[0])
            self._c.controller.add_result(self._data.result, self._name)

    def reset_op(self):
        """ reset operation
        """
        try:
            for (_, element) in self._data.entity_pump.items():
                data_name = element["el_name"].value
                saved = self._data.temporary_data[data_name + "_save"]
                self._data.temporary_data[data_name] = saved
            old_tab = self._data.temporary_data["old_tab"]
            self._data.temporary_data["new_tab"] = old_tab
        except:
            pass

    def add_to_current_workspace(self, widget):
        """ add widget to the current workspace.
        """
        parent = self._parent
        parent.op_workspace[parent.current_op].append(widget)

    def simulate(self):
        """ slot for adding simulation
        """
        if self.last_selected_view is not None:
            instrument = self.data_field.instrument
            if instrument is None:
                return
            stack = self._active_stack
            if stack is None:
                return
            sim_op = self._c.basic_simulator[self.last_selected_view.
                                             main_widget.type]
            temporary_data = self._data.temporary_data
            port_recorder = sim_op.recordable['Simulator_main']
            simulator = sim_op.get_element("Simulator")
            simulator["custom_array"] = True
            theta_array = self.last_selected_view.main_widget.theta_array
            simulator["simulator"]["theta_array"] = theta_array
            port_recorder.disconnect()
            port_recorder.connect_to_signal(self.add_simulation)
            instrument_name = self.data_field.data["Instrument_name"].value
            temporary_data[instrument_name] = instrument
            sim_op.get_element("instrument")["el_name"] = instrument_name
            sim_op.get_element("instrument")["temporary_data"] = temporary_data
            model_name = self.active_stack_editor.stack_name
            sim_op.get_element("stack")["el_name"] = model_name
            sim_op.get_element("stack")["temporary_data"] = temporary_data
            sim_op.temporary_data = temporary_data
            sim_op.reinit()
            sim_op.start()
            self._sim_op = sim_op

    def add_simulation(self, data):
        """ add a new simulation in the widget.
        """
        type_ = data.abstract_type[5:]
        sim_op = self._c.basic_simulator[type_]
        temporary_data = pyxcel.engine.pipeline.TemporaryData()
        sim_op.get_element("instrument")["temporary_data"] = temporary_data
        sim_op.get_element("stack")["temporary_data"] = temporary_data
        sim_op.temporary_data = temporary_data
        simulation = data[type_].value
        self.last_selected_view.main_widget.add_simulation(simulation)

    def open_new_graph(self):
        """ create and open a new graph view
        """
        self.create_graph_view()
        self.last_selected_view.show()

    def create_graph_view(self):
        """ slot for creating a new graph windows
        """
        mdiarea = self._parent.findChild(QMdiArea, "operation_mdiarea")
        self._last_selected_view = pyxcel.view.op_graph.OpGraph(self)
        mdiarea.addSubWindow(self._last_selected_view)
        self.add_to_current_workspace(self._last_selected_view)

    def clear(self):
        """ clear all element
        """
        self.clear_element(self._input_widget.layout())
        self.clear_history()

    def create_fast_inst(self):
        """ creat a fast instrument editor
        """
        if self._data_field is None:
            self._data_field = fast_inst_ed.FastInstrumentEditor(self)
            self._input_widget.layout().addWidget(self._data_field)
            self._data_field.temporary_data = self._data.temporary_data

    def add_entity_choice_field(self, name, element):
        """ add new entity choice field
        """
        if element.entity_type == pyxcel.engine.database.ExperimentalData:
            data_name = element["el_name"].value
            self._data_field.reload_data(data_name, name)
        else:
            self._input_field[name] = EntityChoiceField(self, name, element)
            self._input_widget.layout().addWidget(self.input_field[name])
            if element.entity_type == entity.StackData:
                fast_editor = fast_stack_editor.FastStackEditor(self, self.
                                                                _input_field
                                                                [name])
                self._input_widget.layout().addWidget(fast_editor)
                self._input_field[name].data_editor = fast_editor
                if element.validate:
                    self._input_field[name].validator()

    def launch(self):
        """ launch the current operation
        """
        if self._data_field is not None:
            try:
                self._data_field.validate = True
            except AttributeError:
                message = uni("More data required")
                self._error_msg.showMessage(message)
                return
        for (_, field) in list(self._input_field.items()):
            field.validate = True
        self._c.controller.launch(self._name)
        self.data = None

    def open_parameter(self):
        """ open parameter windows
        """
        mdiarea = self._parent.findChild(QMdiArea, "operation_mdiarea")
        new_form = op_parameter_lite.OperationParameterLite(self, self._data)
        mdiarea.addSubWindow(new_form)
        new_form.show()
        self.add_to_current_workspace(new_form)
