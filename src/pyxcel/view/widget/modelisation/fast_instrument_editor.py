# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
widget to edit instrument before running pipeline.

    :platform: Unix, Windows
    :synopsis: fast instrument editor.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.view.widget.operation.line_editor import LineEditor
from pyxcel.uni import uni
import pyxcel.engine.database
import pyxcel.engine.centralizer
import paf.data
import pyxcel.engine.modeling.entity as entity
from pyxcel.view.widget.composite_editor import clear_layout
from pyxcel.view.widget.operation import line_editor
import pyxcel.view.widget.composite_editor as composite_editor
from pyxcel.view.cute import QWidget, QComboBox, QPushButton, QListWidget
from pyxcel.view.cute import QVBoxLayout, QSpacerItem, QInputDialog
from pyxcel.view.cute import QSizePolicy, QApplication, QAction
from operation.combined import type_inst
try:
    import pyxcel.view.widget.modelisation.fast_instrument_editor_4 as former
except ImportError:
    import pyxcel.view.widget.modelisation.fast_instrument_editor_5 as former
MAKE_DATA = paf.data.make_data

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class FastInstrumentEditor(QWidget):
    """ fast editor for instrument and data
    """
    source_dict = {"XRR": entity.XRaySourceData, "XRF": entity.XRaySourceData}

    detector_dict = {"XRR": entity.XRRDetectorData,
                     "XRF": entity.XRFDetectorData}

    def __init__(self, parent, nb_data=None):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._former = former.Ui_Form()
        self._former.setupUi(self)

        self._type = pyxcel.engine.database.ExperimentalData
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        self._pump_name = []
        self._temporary_data = None
        self._instrument = None
        self._selected_data = None
        self._text = None
        self._xrf_column = []

        self._nb_data = 0

        self._comboBox = self.findChild(QComboBox, "data_combo")

        self._data_list = self.findChild(QListWidget, "data_list")
        self._data_list.currentTextChanged.connect(self.row_selected)
        self._data_list.itemClicked.connect(self.reload)

        self._main_layout = self.findChild(QVBoxLayout, "main_layout")
        self._main_widget = self.findChild(QWidget, "main_widget")
        self._main_widget.setParent(None)

        self._add_button = self.findChild(QPushButton, "add_button")
        self._add_button.clicked.connect(self.add_data)

        self._delete_action = self.findChild(QAction, "delete_data_action")
        self._delete_action.triggered.connect(self.delete_data)
        self._data_list.addAction(self._delete_action)

        self._save_button = self.findChild(QPushButton, "save_button")
        self._save_button.clicked.connect(self.save_instrument)

        self.refresh()

    @property
    def data(self):
        """ accessing to the data
        """
        return self._selected_data

    @property
    def instrument(self):
        """ get selected instrument.
        """
        return self._instrument

    @property
    def pump_name(self):
        """ access to list of all entity pump name
        """
        return self._pump_name

    @property
    def temporary_data(self):
        """ acccessing to temporary data
        """
        return self._temporary_data

    @temporary_data.setter
    def temporary_data(self, value):
        """ modify temporary data
        """
        self._temporary_data = value

    def save_instrument(self):
        """ save selected instrument
        """
        title = "Save instrument"
        meesage = "New instrument name"
        result = QInputDialog.getText(self, title, meesage)
        if result[1]:
            current_row = self._data_list.currentRow()
            data_name = uni(self._data_list.currentItem().text())
            source = self.source_dict["XRR"]
            detector = self.detector_dict["XRR"]
            type_name = "XRR"
            if self._xrf_column[current_row] is not None:
                name_column = uni(self._xrf_column[current_row].value)
                source = self.source_dict["XRF"]
                detector = self.detector_dict["XRF"]
                type_name = "XRF"
            else:
                name_column = None
            instrument = self.get_instrument(data_name, name_column)
            name_instru = uni(result[0])
            self._centralizer.controller.create_instrument(name_instru, source,
                                                           detector, type_name)
            instru = self._centralizer.database.real_value[name_instru]
            instru["default_value"] = paf.data.copy_data(instrument)

    def reload(self):
        """ slot for reclick on list
        """
        if self._text == unicode(self._data_list.currentItem().text()):
            self.row_selected(self._text)

    def clear(self):
        """ clear all composite field
        """
        clear_layout(self._main_layout)

    def row_selected(self, text):
        """ slot for data selection
        """
        if text == "":
            return
        self.clear()
        index = self._data_list.currentRow()
        pump_name = self._pump_name[index]
        self._parent.selected_exp_data = pump_name
        text = uni(text)
        self._text = text
        exp_data = self._centralizer.database[text]
        self._selected_data = exp_data
        view = self._parent.last_selected_view
        if view is not None:
            view.data = exp_data
        current_row = self._data_list.currentRow()
        if self._xrf_column[current_row] is not None:
            name_column = self._xrf_column[current_row].value
        else:
            name_column = None
        self._instrument = self.get_instrument(text, name_column)
        if type_inst(self._instrument) == "XRF":
            line_data = pyxcel.engine.database.CompositeMultiEditor()
            opti = self._parent.data.get_element("optimization_filter")
            line_data.add_element(opti["parameters"][current_row], "line")
            if view is not None:
                basic_simulator = self._centralizer.basic_simulator["XRF"]
                simulator = basic_simulator.get_element("Simulator")
                line = opti["parameters"][current_row]["line"]
                simulator["parameter"]["line"] = line
                line_data.add_connexion("line", simulator["parameter"], "line")
            line_editor = LineEditor(self, line_data["line"])
            self._main_layout.addWidget(line_editor)
            GIXRF_file_header = open(text).readline()
            list_column = GIXRF_file_header.split()
            index_column = list_column.index(name_column)
            if view is not None:
                view.main_widget.change_XRF_column(index_column)

        instrument = pyxcel.engine.database.CompositeMultiEditor()
        instrument.add_element(self._instrument["source"], 'I0')
        if type_inst(self._instrument) == "XRF":
            instrument.add_element(self._instrument["detector"], 'void')
            instrument.add_element(self._instrument["detector"],
                                   'width_parallel_s')
            instrument.add_element(self._instrument["detector"],
                                   'width_parallel_l')
            instrument.add_element(self._instrument["detector"],
                                   'pinhole_height')
            instrument.add_element(self._instrument["detector"], 'dist')
            instrument.add_element(self._instrument["source"], 'beamw')
            instrument.add_element(self._instrument["detector"], 'res')
            for link in self._parent.data.get_link(current_row):
                linked_name = uni(self._data_list.item(link).text())
                linked_cname = self._xrf_column[link].value
                new_instrument = self.get_instrument(linked_name, linked_cname)
                instrument.add_connexion('width_parallel_s',
                                         new_instrument["detector"])
                instrument.add_connexion('width_parallel_l',
                                         new_instrument["detector"])
                instrument.add_connexion('pinhole_height',
                                         new_instrument["detector"])
                instrument.add_connexion('beamw', new_instrument["source"])
                instrument.add_connexion('res', new_instrument["detector"])
                instrument.add_connexion('dist', new_instrument["detector"])
        else:
            instrument.add_element(self._instrument["source"], 'footype')
            instrument.add_element(self._instrument["detector"], 'res')
            instrument.add_element(self._instrument["detector"], 'Ibkg')
        instrument_editor = composite_editor.CompositeEditor(self, instrument,
                                                             True)
        self._main_layout.addWidget(instrument_editor)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum,
                                 QSizePolicy.Expanding)
        self._main_layout.addItem(spacerItem)

    def get_instrument(self, data_name, xrf_column=None):
        """ get instrument object in temporary data from data_name
        """
        exp_data = self._centralizer.database[data_name]
        instrument_name = exp_data["Instrument_name"].value
        if xrf_column is not None:
            instrument_name += "_" + xrf_column
        return self._temporary_data[instrument_name]

    def delete_data(self):
        """ slot for deleting data
        """
        index = self._data_list.currentRow()
        self._data_list.takeItem(index)
        pump_name = self._pump_name[index]
        del self._pump_name[index]
        del self._xrf_column[index]
        self._parent.data.delete_data(pump_name)

    def reload_data(self, name, entity_pump_name):
        """ reload a data
        """
        self._data_list.addItem(name)
        self._pump_name.append(entity_pump_name)
        exp_data = self._centralizer.database[name]
        instrument_name = exp_data["Instrument_name"].value
        phy_instrument = self._centralizer.database[instrument_name]
        instrument = phy_instrument['default_value']
        if instrument.abstract_type == "XRFInstrument":
            GIXRF_file_header = open(name).readline()
            list_column = GIXRF_file_header.split()
            new_column = self._temporary_data[entity_pump_name + "_col"].value
            self._xrf_column.append(MAKE_DATA(list_column[new_column]))
        else:
            self._xrf_column.append(None)
        self._nb_data += 1

    def add_data(self):
        """ slot for add data button
        """
        name = uni(self._comboBox.currentText())
        self._data_list.addItem(name)
        entity_pump_name = self._parent.data.add_data(name)
        self._pump_name.append(entity_pump_name)
        exp_data = self._centralizer.database[name]
        instrument_name = exp_data["Instrument_name"].value
        phy_instrument = self._centralizer.database[instrument_name]
        self._instrument = phy_instrument['default_value']
        if self._instrument.abstract_type == "XRFInstrument":
            title = "Data column"
            mesage = "Column: "
            GIXRF_file_header = open(name).readline()
            list_column = GIXRF_file_header.split()
            column = QInputDialog.getItem(self, title, mesage, list_column,
                                          current=0, editable=False)
            if column[1]:
                self._xrf_column.append(MAKE_DATA(uni(column[0])))
                new_column = MAKE_DATA(list_column.index(uni(column[0])))
                self._temporary_data[entity_pump_name + "_col"] = new_column
                self._temporary_data[entity_pump_name +
                                     "_col_name"] = MAKE_DATA(uni(column[0]))
                instrument_name += "_" + uni(column[0])
        else:
            self._xrf_column.append(None)
        entity_pump = self._parent.data.get_element(entity_pump_name)
        entity_pump["el_name"] = name
        self._temporary_data[instrument_name] = self._instrument
        self._nb_data += 1
        self._parent.data.load_dataset(entity_pump_name)

    def refresh(self):
        """ refresh the view
        """
        self._comboBox.clear()
        for element_name in self._centralizer.database.keys():
            if isinstance(self._centralizer.database[uni(element_name)],
                          self._type):
                self._comboBox.addItem(element_name)
