# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for exposing simulation evolution.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import os.path
import pyxcel.view.widget.visualization.data_view as data_view
import pyxcel.engine.centralizer
from pyxcel.uni import uni
from pyxcel.view.widget.composite_editor import clear_layout, CompositeEditor
from pyxcel.view.mdi_window import MDIWindow
from pyxcel.view.cute import QSize, QWidget, QLineEdit, QComboBox, QPushButton
from pyxcel.view.cute import uic
try:
    import pyxcel.view.op_graph_4 as former
except ImportError:
    import pyxcel.view.op_graph_5 as former


class OpGraph(MDIWindow):
    """ widget to observe optimised simulation graphic evolution
    """
    def __init__(self, parent):
        """ initialization
        """
        MDIWindow.__init__(self, parent, former.Ui_Form())
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        self._pump_name = None

        # configurate widget
        self._fom_widget = self.findChild(QWidget, "fom_widget")
        self._fom_line = self.findChild(QLineEdit, "fom_line")
        self._fom_widget.hide()

        self._fom_selector = self.findChild(QComboBox, "fom_selector")
        for index, fom_name in enumerate(sorted(list(self._centralizer.option.
                                                     fom_dict.keys()))):
            self._fom_selector.addItem(fom_name)
            if fom_name == "b_normalized":
                self._fom_selector.setCurrentIndex(index)
        self._fom_selector.currentIndexChanged.connect(self.change_fom)

        data_treatment_button = self.findChild(QPushButton,
                                               "data_treatment_button")
        data_treatment_button.clicked.connect(self.open_data_treatement)

        #: data treatment window
        self._data_treatment = None

    def open_data_treatement(self):
        """ open data treatment windows
        """
        # define slot for data treatment windows
        def change_operation(index):
            """ change current operation
            """
            window = self._data_treatment
            config_widget = window.findChild(QWidget, "config_widget")
            operation_combo = window.findChild(QComboBox, "operation_combo")
            name = uni(operation_combo.currentText())
            op_generator = self._centralizer.option.data_treatment[name]
            self._op_treatment = op_generator(self._pump_name + "_dataset")
            op_treatment = self._op_treatment
            op_treatment.temporary_data = self._parent.data.temporary_data
            clear_layout(config_widget.layout())
            essential_editor = CompositeEditor(self, self._op_treatment.
                                               essential)
            config_widget.layout().addWidget(essential_editor)

        def validate_slot():
            """ slot for validating
            """
            self._op_treatment.reinit()
            self._op_treatment.start()
            self._data_treatment.close()

        self._data_treatment = QWidget()

        # load ui for data treatement
        data_treatement_ui = os.path.join(self._centralizer.option.ui_dir,
                                          "data_treatment.ui")
        uic.loadUi(data_treatement_ui, self._data_treatment)

        # configure UI
        operation_combo = self._data_treatment.operation_combo
        operation_combo.addItems(self._centralizer.option.data_treatment.keys()
                                 )
        operation_combo.currentIndexChanged.connect(change_operation)
        self._data_treatment.validate_button.clicked.connect(validate_slot)
        change_operation(0)

        # show window
        self._data_treatment.show()

    def change_fom(self, index=0):
        """ slot for changing FOM
        """
        name = uni(self._fom_selector.currentText())
        self._main_widget.fom_func = self._centralizer.option.fom_dict[name]()
        fom = format(self._main_widget.fom, '.3g')
        self._fom_line.setText(fom)

    def show_fom(self, show=True):
        """ slot for fom calculable

        :param show: if it's true it show the fom widget and hide it if not
        :type show: bool
        """
        if show:
            self._fom_widget.show()
            fom = format(self._main_widget.fom, '.3g')
            self._fom_line.setText(fom)
            self.change_fom()
        else:
            self._fom_widget.hide()

    def sizeHint(self, *args, **kwargs):
        """ rewrite size hint for give default size for window
        """
        return QSize(500, 400)

    def new_widget(self, data):
        """ creating new widget
        """
        self._data = data
        instrument_name = data["Instrument_name"].value # TODO : data[] does not contain instrument info, look elsewhere
        phy_instrument = self._centralizer.database[instrument_name]
        self._instrument = phy_instrument['default_value']
        type_ = self._instrument.abstract_type[:-10]
        temporary_data = self._parent.data.temporary_data
        self._pump_name = self._parent.selected_exp_data
        data_set = temporary_data[self._pump_name + "_dataset"]
        new_widget = data_view.ExperimentalDataView(self, data_set, type_)
        new_widget.fom_calculable.connect(self.show_fom)
        return new_widget

    @property
    def main_widget(self):
        return self._main_widget
