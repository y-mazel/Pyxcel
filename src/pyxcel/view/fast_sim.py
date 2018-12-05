# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to launch a fast simulation.

    :platform: Unix, Windows
    :synopsis: fast simulation windows.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
import pyxcel.engine.centralizer
import pyxcel.engine.database
import pyxcel.engine.modeling.entity
import paf.data
import pyxcel.view.widget.composite_editor as composite_editor
from pyxcel.view.widget.operation.line_editor import LineEditor
from pyxcel.view.cute import QWidget, QComboBox, QPushButton, QVBoxLayout
try:
    import pyxcel.view.fast_sim_4 as former
except ImportError:
    import pyxcel.view.fast_sim_5 as former


class FastSim(QWidget):
    """ widget to lunch a fast simulation.
    """
    def __init__(self, callback=None, custom_array=None):
        """ initialization
        """
        QWidget.__init__(self)
        self._former = former.Ui_speed_sim()
        self._former.setupUi(self)
        self._c = pyxcel.engine.centralizer.Centralizer()

        # set widget
        self._instrument_combo = self.findChild(QComboBox, "instrument_combo")
        self._instrument_combo.currentIndexChanged.connect(self.
                                                           select_instrument)
        self._model_combo = self.findChild(QComboBox, "model_combo")
        self._option_layout = self.findChild(QVBoxLayout, "option_layout")
        self._option_widget = self.findChild(QWidget, "option_widget")

        self._simulate_button = self.findChild(QPushButton, "simulate_button")
        self._simulate_button.clicked.connect(self.simulate)

        # variable
        self._instrument = ""
        self._instrument_type = pyxcel.engine.database.PhysicalInstrument
        self._model_type = pyxcel.engine.modeling.entity.StackData
        self._callback = callback
        self._custom_array = custom_array
        value = {"scan_start": .1, "scan_stop": 1., "points": 100}
        self._linspace_param = paf.data.CompositeData(value)

        # construction
        self._fill_combobox()

    def _fill_combobox(self):
        """ fill all combobox by reading database.
        """
        db = self._c.database
        for element_name in db.keys():
            if isinstance(db[uni(element_name)], self._instrument_type):
                self._instrument_combo.addItem(element_name)
            elif isinstance(db[uni(element_name)], self._model_type):
                self._model_combo.addItem(element_name)

    @property
    def instrument(self):
        """ property for access to the instrument
        """
        return self._instrument

    @instrument.setter
    def instrument(self, instrument):
        """ fix the instrument.
        """
        self._instrument_combo.setCurrentIndex(self._instrument_combo.
                                               findText(instrument))
        self._instrument_combo.setEnabled(False)

    def select_instrument(self, instrument):
        """ select instrument
        """
        index = self._instrument_combo.findText(str(instrument))
        if index == -1:
            index = self._instrument_combo.currentIndex()
        else:
            self._instrument_combo.setCurrentIndex(index)
        self._instrument = uni(self._instrument_combo.currentText())
        type_ = self._c.database.get_type(self._instrument)
        composite_editor.clear_layout(self._option_layout)
        if type_ == "XRF":
            basic_simulator = self._c.basic_simulator["XRF"]
            simulator = basic_simulator.get_element("Simulator")
            line = simulator["parameter"]["line"]
            line_editor = LineEditor(self._option_widget, line)
            self._option_layout.addWidget(line_editor)
        if self._custom_array is None:
            param_editor = composite_editor.CompositeEditor(self, self.
                                                            _linspace_param)
            self._option_layout.addWidget(param_editor)

    @property
    def model(self):
        """ accessing to the model
        """
        return uni(self._instrument_combo.currentText())

    @model.setter
    def model(self, model):
        """ fix the model
        """
        self._model_combo.setCurrentIndex(self._model_combo.
                                          findText(str(model)))
        self._model_combo.setEnabled(False)

    def simulate(self):
        """ execute simulation
        """
        instrument_name = uni(self._instrument_combo.currentText())
        type_ = self._c.database.get_type(instrument_name)
        basic_simulator = self._c.basic_simulator[type_]
        if self._callback is not None:
            port_recorder = basic_simulator.recordable['Simulator_main']
            port_recorder.disconnect()
            port_recorder.connect_to_signal(self._callback)
        simulator = basic_simulator.get_element("Simulator")
        if self._custom_array is None:
            simulator["custom_array"] = False
            simulator["scan_start"] = self._linspace_param["scan_start"]
            simulator["scan_stop"] = self._linspace_param["scan_stop"]
            simulator["points"] = self._linspace_param["points"]
        else:
            simulator["custom_array"] = True
            simulator["simulator"]["theta_array"] = self._custom_array
        inst = self._c.database[instrument_name]['default_value']
        temporary_data = (basic_simulator.get_element("instrument")
                          ["temporary_data"])
        temporary_data[instrument_name] = inst
        basic_simulator.get_element("instrument")["el_name"] = instrument_name
        model_name = uni(self._model_combo.itemText(self._model_combo.
                                                    currentIndex()))
        basic_simulator.get_element("stack")["el_name"] = model_name
        basic_simulator.reinit()
        basic_simulator.start()
        self.close()
