# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for exposing simulation evolution.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
import pyxcel.view.widget.visualization.data_view as data_view
import pyxcel.engine.centralizer
import pyxcel.engine.database
import numpy as np
import logging
from pyxcel.view.param_evol import FOMView
from pyxcel.view.mdi_window import MDIWindow
from pyxcel.view.cute import QComboBox, QWidget, QVBoxLayout, QLineEdit
try:
    import pyxcel.view.op_graph_4 as former
except ImportError:
    import pyxcel.view.op_graph_5 as former


class OpGraph(MDIWindow):
    """ widget to observe optimised simulation graphic evolution
    """
    def __init__(self, parent, op_name):
        """ initialization
        """
        MDIWindow.__init__(self, parent, former.Ui_Form())
        self._centralizer = pyxcel.engine.centralizer.Centralizer()

        # create vars
        self._op = self._centralizer.database.get_operation(uni(op_name))[0]
        self._op_name = op_name
        self._simulations = None

        # configure widget
        self._op.evolution_report.connect(self.refresh_graph)

        self._choose_data_combo = self.findChild(QComboBox,
                                                 "choose_data_combo")

        self._fom_line = self.findChild(QLineEdit, "fom_line")

        self.fill_combo()
        self._fom_selector = self.findChild(QComboBox, "fom_selector")
        self._fom_list = []
        for index, fom_name in enumerate(sorted(list(self._centralizer.option.
                                                     fom_dict.keys()))):
            self._fom_selector.addItem(fom_name)
            self._fom_list.append(fom_name)
            try:
                if fom_name == self._op.get_fom(0):
                    self._fom_selector.setCurrentIndex(index)
                    self.change_fom(index)
            except AttributeError:
                if fom_name == "b_normalized":
                    self._fom_selector.setCurrentIndex(index)
                    self.change_fom(index)
        self._fom_selector.currentIndexChanged.connect(self.change_fom)

        data_treatment_widget = self.findChild(QWidget,
                                               "data_treatment_widget")
        data_treatment_widget.hide()

        nb_data_set = self._choose_data_combo.count()
        self._foms = [np.array([]) for _ in range(nb_data_set)]
        self._fom = None
        self._choose_data_combo.currentIndexChanged.connect(self.select_data)
        try:
            self.select_data()
        except:
            self.close()

    @property
    def main_widget(self):
        """ accessing to the main widget
        """
        return self._main_widget

    def change_fom(self, index):
        """ slot for changing FOM
        """
        name = uni(self._fom_selector.currentText())
        self._sim_widget.fom_func = self._centralizer.option.fom_dict[name]()
        fom = format(self._sim_widget.fom, '.3g')
        self._fom_line.setText(fom)

    def show_fom(self, show=True):
        """ slot for fom calculable

        :param show: if it's true it show the fom widget and hide it if not
        :type show: bool
        """
        if show:
            self._fom_line.setText(format(self._sim_widget.fom, '.3g'))

    def fill_combo(self):
        """ fill self._choose_data_combo and load data in memory
        """
        self._choose_data_combo.setEnabled(True)
        for (key, entity_pump) in sorted(self._op.entity_pump.items()):
            if (entity_pump.entity_type ==
                    pyxcel.engine.database.ExperimentalData):
                self._choose_data_combo.addItem(key)

    def select_data(self, index=0):
        """ slot for new data selected
        """
        fom_index = 0
        try:
            fom_index = self._fom_list.index(self._op.get_fom(index))
            self._fom_selector.setCurrentIndex(fom_index)
        except AttributeError:
            pass
        name = uni(self._choose_data_combo.currentText())
        data_name = self._op.entity_pump[name]["el_name"].value
        self.data = self._centralizer.database[data_name]
        try:
            self._fom.foms = self._foms[self._choose_data_combo.currentIndex()]
        except:
            pass
        try:
            temp = self._op.temporary_data
            column = temp.value[name + "_col"]
            self._sim_widget.change_XRF_column(column)
        except:
            pass
        self.add_simulation(name)
        self.change_fom(fom_index)
        logging.info("Selecting data in operation (%s): %s", self._op_name, name)

    def add_simulation(self, name):
        """ add simulation to main widget
        """
        if self._simulations is not None:
            selected_sim = self._simulations[name].value
            if selected_sim.size != 0:
                self._sim_widget.add_simulation(selected_sim)

    def new_widget(self, data):
        """ creating new widget
        """
        if not isinstance(data, pyxcel.engine.database.ExperimentalData):
            try:
                self.select_data()
            except:
                pass
            return None
        self._data = data
        new_widget = QWidget(self)
        new_widget.setLayout(QVBoxLayout())
        pump_name = uni(self._choose_data_combo.currentText())
        dataset = self._op.temporary_data[pump_name + "_dataset"]
        index = self._choose_data_combo.currentIndex()
        self._op.clear_inf[index](dataset)
        instrument_name = data["Instrument_name"].value
        phy_instrument = self._centralizer.database[instrument_name]
        self._instrument = phy_instrument['default_value']
        type_ = self._instrument.abstract_type[:-10]
        self._sim_widget = data_view.ExperimentalDataView(self, dataset, type_)
        self._sim_widget.fom_calculable.connect(self.show_fom)
        new_widget.layout().addWidget(self._sim_widget)
        if self._choose_data_combo.count() > 1:
            self._fom = FOMView(self)
            new_widget.layout().addWidget(self._fom)
        return new_widget

    def refresh_graph(self, report):
        """ refreshing the graph
        """
        self._simulations = report["simulations"]
        self.add_simulation(uni(self._choose_data_combo.currentText()))
        if len(self._op.entity_pump) > 1:
            foms = report["FOMS"].value
            self._foms = [np.append(self._foms[idx], fom)
                          for idx, fom in enumerate(foms)]
            if self._fom is not None:
                self._fom.append_fom(foms[self._choose_data_combo.
                                          currentIndex()])
