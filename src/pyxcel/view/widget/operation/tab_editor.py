# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit parameter to fit.

    :platform: Unix, Windows
    :synopsis: edit parameter to fit.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import logging
import pyxcel.engine.centralizer
import paf.data
from pyxcel.engine.modeling.entity import LayerProfileData
from pyxcel.uni import uni
from pyxcel.view.cute import QDialog, QComboBox, QPushButton, QTableWidget
from pyxcel.view.cute import QTableWidgetItem, QFileDialog, QMessageBox
from pyxcel.view.cute import Qt, QApplication
from pyxcel.controller import type_inst
try:
    import pyxcel.view.widget.operation.tab_editor_4 as former
except ImportError:
    import pyxcel.view.widget.operation.tab_editor_5 as former
MAKE_DATA = paf.data.make_data

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig)


class TabEditor(QDialog):
    """ class to create a form for show the execution of a pipeline.
    """
    def __init__(self, parent, data):
        """ initialization
        """
        # draw form
        QDialog.__init__(self, parent)
        self._parent = parent
        self._data = data
        self._former = former.Ui_Form()
        self._former.setupUi(self)

        # configure widget
        self._element_combo = self.findChild(QComboBox, "element_combo")
        self._element_combo.lineEdit().textChanged.connect(self.select_element)
        self._element_combo.lineEdit().setReadOnly(True)

        self._parameter_combo = self.findChild(QComboBox, "parameter_combo")

        self._add_button = self.findChild(QPushButton, "add_button")
        self._add_button.clicked.connect(self.add_param_slot)

        self._load_button = self.findChild(QPushButton, "load_button")
        self._load_button.clicked.connect(self.load)

        self._delete_button = self.findChild(QPushButton, "delete_button")
        self._delete_button.clicked.connect(self.delete_param)

        self._parameter_tab = self.findChild(QTableWidget, "parameter_tab")
        self._parameter_tab.cellClicked.connect(self.select_cell)

        self._validate_button = self.findChild(QPushButton, "validate_button")
        self._validate_button.clicked.connect(self.validate)

        self._cancel_button = self.findChild(QPushButton, "cancel_button")
        self._cancel_button.clicked.connect(self.cancel)

        self._save_button = self.findChild(QPushButton, "save_button")
        self._save_button.clicked.connect(self.save)

        #: list of all parameter in tab (element, parameter, value)
        self._parameter_list = []

        #: element parameter map
        self._element_parameter = {}
        #: based value of parameter
        self._parameter_value = {}

        #: create access to temporary value
        self._temporary_data = None

        # initialize private data
        self._centralizer = pyxcel.engine.centralizer.Centralizer()

        # initialize option
        self.create_element_list()
        self.load_string(self._data["text"].value)

    def select_cell(self, row):
        """ slot for selecting cell
        """
        self._parameter_tab.selectRow(row)

    def cancel(self):
        """ cancel action
        """
        self._parent.go_back()

    def validate(self):
        """ validate
        """
        self.generate_data()
        self._parent.go_back()

    def save(self):
        """ save data in file
        """
        file_name = QFileDialog.getSaveFileName(self, "Save")
        try:
            is_ok = file_name[1]
            if isinstance(is_ok, str):
                is_ok = file_name[0] != ""
                file_name = file_name[0]
        except IndexError:
            is_ok = False
        if is_ok:
            self.generate_data()
            with open(file_name, "w") as tab_file:
                tab_file.write(self._data.value["text"])

    def load(self):
        """ load data from file
        """
        file_name = QFileDialog.getOpenFileName(self, "Load")
        try:
            is_ok = file_name[1]
            if isinstance(is_ok, str):
                is_ok = file_name[0] != ""
                file_name = file_name[0]
        except IndexError:
            is_ok = False
        if is_ok:
            with open(file_name, "r") as tab_file:
                try:
                    self.load_string(tab_file.read())
                    logging.info("Open tab file %s", file_name)
                except:
                    message = "Incompatible data file"
                    title = "Format error"
                    QMessageBox.about(self, title, message)
                    logging.error("Tried to open not well formed tab file")

    def load_string(self, tab_str):
        """ load data from string
        """
        tab = tab_str.split("\n")[1:]
        for line in tab:
            line_element = line.split()
            if len(line_element) == 0:
                break
            element_name = line_element[0].split(".")[0]
            param_name = line_element[0].split(".")[1][3:]
            param_name_low = param_name[0].lower() + param_name[1:]
            if param_name != "I0" and param_name != "Ibkg":
                param_name = param_name_low
            base_value = line_element[1]
            min_ = line_element[3]
            max_ = line_element[4]
            groupe = line_element[-1]
            if groupe == "None" or groupe == "2e-01,)":
                groupe = None
            self.add_param(element_name, param_name, base_value, min_, max_,
                           groupe)

    def generate_data(self):
        """ generate data from the tab
        """
        text = "#Parameter    Value    Fit    Min    Max    Error \n"
        for index in range(self._parameter_tab.rowCount()):
            tab = [0, 2, 1, 3, 4, 5, 6]
            for i in tab:
                new_text = uni(self._parameter_tab.item(index, i).text())
                if i != 6:
                    new_text += "\t"
                else:
                    if new_text == "":
                        new_text = "None"
                text += new_text
            text += "\n"
        self._data["text"] = text
        self._data.emit_modify()

    def delete_param(self):
        """ delete selected parameter
        """
        index = self._parameter_tab.currentRow()
        self._parameter_tab.removeRow(index)

        # recreate element list
        (element_name, param_name, base_value) = self._parameter_list[index]
        self._parameter_value[element_name].append(base_value)
        self._element_parameter[element_name].append(param_name)

        # refresh param list
        if self._element_combo.currentText() == element_name:
            self.select_element(element_name)

        # delete parameter
        del self._parameter_list[index]

    def add_param_slot(self):
        """ slot for add selected parameter to tab.
        """
        element_name = uni(self._element_combo.currentText())
        # create name of parameter
        param_list = self._element_parameter[element_name]
        if len(param_list) >= 1:
            param_name = param_list[self._parameter_combo.currentIndex()]
            self.add_param(element_name, param_name)

    def add_param(self, element_name, param_name, base_value=None, min_=None,
                  max_=None, groupe=None):
        """ add parameter to tab.
        """
        # start by upper case character
        param_name_up = param_name[0].upper() + param_name[1:]
        genx_name = element_name + '.set' + param_name_up

        # extract base value
        try:
            param_index = (self._element_parameter[element_name].
                           index(param_name))
        except:
            return
        if base_value is None:
            base_value = self._parameter_value[element_name][param_index]

        # save element
        self._parameter_list.append((element_name, param_name, base_value))

        # delete element from tab
        del self._parameter_value[element_name][param_index]
        del self._element_parameter[element_name][param_index]

        # refresh param list
        self.select_element(element_name)

        # add line in tab
        index = self._parameter_tab.rowCount()
        self._parameter_tab.setRowCount(index+1)
        item = QTableWidgetItem()
        item.setText(genx_name)
        item.setFlags(Qt.ItemIsEnabled)
        self._parameter_tab.setItem(index, 0, item)
        item = QTableWidgetItem()
        item.setText("True")
        self._parameter_tab.setItem(index, 1, item)
        item = QTableWidgetItem()
        item.setText(uni(base_value))
        self._parameter_tab.setItem(index, 2, item)
        item = QTableWidgetItem()
        if min_ is None:
            min_ = base_value-base_value*.25
        item.setText(uni(min_))
        self._parameter_tab.setItem(index, 3, item)
        item = QTableWidgetItem()
        if max_ is None:
            max_ = base_value+base_value*.25
        item.setText(uni(max_))
        self._parameter_tab.setItem(index, 4, item)
        item = QTableWidgetItem()
        item.setText(uni("0"))
        self._parameter_tab.setItem(index, 5, item)
        item = QTableWidgetItem()
        if groupe is None:
            item.setText(uni(""))
        else:
            item.setText(uni(groupe))
        self._parameter_tab.setItem(index, 6, item)

    def select_element(self, name):
        """ select an element
        """
        name = uni(name)
        self._parameter_combo.clear()
        try:
            self._parameter_combo.addItems(self._element_parameter[name])
        except KeyError:
            pass

    def add_sample_element(self, sample):
        """ add a new sample element
        """
        def generate_value(layer):
            """ generate value for a layer
            """
            parameter = ["d", "sigmar"]
            tab = [layer["d"].value, layer["sigmar"].value]
            if isinstance(layer, LayerProfileData):
                parameter[0] = "profile_d"
                parameter[1] = "profile_sigmar"
                for idx, profile in enumerate(layer["materials"]["computers"]):
                    for kwarg, value in profile["kwargs"].items():
                        parameter.append("profile_" + str(idx) + "_" + kwarg)
                        tab.append(value.value)
                for kwarg, value in layer["densities"].items():
                    if kwarg == "type":
                        continue
                    parameter.append("profile_dens_" + kwarg)
                    tab.append(value.value)
            else:
                tab.append(layer["numerical_density"].value)
                parameter.append("numerical_density")
                tab.append(layer["mass_density"].value)
                parameter.append("mass_density")
            return tab, parameter
        sub_name = sample['substrate']["name"].value
        self._element_combo.addItem(sub_name)
        self._element_parameter[sub_name] = ["numerical_density",
                                             "mass_density", "sigmar"]
        self._parameter_value[sub_name] = [sample['substrate']
                                           ["numerical_density"].value,
                                           sample['substrate']
                                           ["mass_density"].value,
                                           sample['substrate']["sigmar"].value]
        for layer in sample.real_value['layers']:
            if layer['material'].value.count("_") > 0:
                self.add_stochio_element(layer)
            lay_name = layer["name"].value
            self._element_combo.addItem(lay_name)
            value, parameter = generate_value(layer)
            self._parameter_value[lay_name] = value
            self._element_parameter[lay_name] = parameter
        self.select_element(sub_name)

    def add_inst_element(self, inst, inst_name=None):
        """ add new instrument
        """
        source = inst["source"]
        detector = inst["detector"]
        parameter = ["I0"]
        parameter_value = [source['I0'].value]
        if type_inst(inst) == "XRF":
            parameter.extend(["dist", "pinhole_height", "width_parallel_l",
                              "width_parallel_s", "res"])
            parameter_value.extend([detector['dist'].value,
                                    detector["pinhole_height"].value,
                                    detector["width_parallel_l"].value,
                                    detector["width_parallel_s"].value,
                                    detector["res"].value])
        elif type_inst(inst) == "XRR":
            parameter.extend(["res", "Ibkg"])
            parameter_value.extend([detector['res'].value,
                                    detector["Ibkg"].value])
        if inst_name is None:
            inst_name = inst["name"].value
        self._element_parameter[inst_name] = parameter
        self._parameter_value[inst_name] = parameter_value
        self._element_combo.addItem(inst_name)

    def add_stochio_element(self, layer):
        """ add element for stochio

        :param layer: layer containing stochio
        """
        stochio = layer.stochio
        parameter = ["stochio" + uni(index)
                     for index in range(len(stochio))]
        element_name = "stochio_" + layer["name"].value
        self._element_combo.addItem(element_name)
        self._parameter_value[element_name] = stochio
        self._element_parameter[element_name] = parameter

    def create_element_list(self):
        """ create a list of element
        """
        field_list = self._parent.input_field
        first_field = field_list[list(field_list.keys())[0]]
        self._temporary_data = first_field.entity_pump["temporary_data"]
        for _, field in field_list.items():
            el_name = field.selected_value
            if el_name is None:
                continue
            element = self._temporary_data[el_name]
            self.add_sample_element(element)
        data_field = self._parent.data_field
        for pump_name in data_field.pump_name:
            data_name = (self._parent.data.get_element(pump_name)["el_name"].
                         value)
            exp_data = self._centralizer.database[data_name]
            instrument_name = exp_data["Instrument_name"].value
            try:
                column_name = pump_name + "_col_name"
                column_name = self._temporary_data[column_name].value
                instrument_name += '_' + column_name
                instrument = self._temporary_data[instrument_name]
                self.add_inst_element(instrument, instrument_name)
            except:
                instrument = self._temporary_data[instrument_name]
                self.add_inst_element(instrument)
