# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit a sample for modeling a sample.

    :platform: Unix, Windows
    :synopsis: sample editor.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
import pyxcel.engine.centralizer
import pyxcel.engine.database
from pyxcel.view.cute import QWidget, QInputDialog, QPushButton, QMessageBox
from pyxcel.view.cute import QApplication, QFileDialog, QTableWidget
from pyxcel.view.cute import QTableWidgetItem, QGroupBox, QComboBox
from pyxcel.view.cute import Qt
from pyxcel.engine.database import CompositeDataObservable
try:
    import pyxcel.view.widget.modelisation.sample_editor_4 as former
except ImportError:
    import pyxcel.view.widget.modelisation.sample_editor_5 as former

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class SampleEditor(QWidget):
    """ for editing sample
    """
    def __init__(self, parent, data):
        """ initialization
        """
        QWidget.__init__(self, parent)

        #: option and database centralizer
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        self._parent = parent
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        self._data = CompositeDataObservable(data)

        # adapt presentation
        self._model_box = self.findChild(QGroupBox, 'model_box')
        self._data_box = self.findChild(QGroupBox, 'data_box')
        abstract = data.abstract_type
        if abstract == 'data':
            self._model_box.hide()
        elif abstract == 'model':
            self._data_box.hide()

        # connect button for adding new model
        add_model_button = self.findChild(QPushButton, "add_model_button")
        add_model_button.clicked.connect(self.create_model)

        # connect button for adding new model
        copy_button = self.findChild(QPushButton, "copy_button")
        copy_button.clicked.connect(self.copy_model)

        # connect button for new experimental data
        add_exp_data_button = self.findChild(QPushButton,
                                             "add_exp_data_button")
        add_exp_data_button.clicked.connect(self.add_experimental_data)

        #: model table
        self._model_table = self.findChild(QTableWidget, "model_table")

        #: list of select instrument combo
        self._inst_combo = []

        # connect notification for data refreshing
        self._data.connect_to_signal(self.refresh)
        self.refresh()

    def recreate_header(self):
        """ recreate header for QtableWidget
        """
        model_table = self.findChild(QTableWidget, "model_table")
        model_table.clear()
        model_table.setRowCount(0)
        item = QTableWidgetItem()
        model_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        model_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        model_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        model_table.setHorizontalHeaderItem(3, item)
        self._former.retranslateUi(self)
        exp_data_table = self.findChild(QTableWidget, "exp_data_table")
        exp_data_table.clear()
        exp_data_table.setRowCount(0)
        item = QTableWidgetItem()
        exp_data_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        exp_data_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        exp_data_table.setHorizontalHeaderItem(2, item)
        self._former.retranslateUi(self)

    def create_inst_slot(self, data, index):
        """ create a slot for change instrument in combobox
        """
        def change_inst(selected):
            """ new slot for change instrument in combobox
            """
            value = uni(self._inst_combo[index].currentText())
            data["Instrument_name"] = value
        return change_inst

    def create_theta_slot(self, data):
        """ create slot for theta scale
        """
        def change_theta(selected):
            """ new slot for theta scale
            """
            if selected == 0:
                data["2_Theta"] = True
            else:
                data["2_Theta"] = False
        return change_theta

    def append_exp_data(self, data):
        """ append experimental data to data table
        """
        exp_data_table = self.findChild(QTableWidget, "exp_data_table")
        index = exp_data_table.rowCount()
        exp_data_table.setRowCount(index+1)
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setText(data["file_name"].value)
        exp_data_table.setItem(index, 0, item)
        inst_combo = QComboBox(self)
        element_list = []
        for element_name in self._centralizer.database.keys():
            if isinstance(self._centralizer.database[uni(element_name)],
                          pyxcel.engine.database.PhysicalInstrument):
                element_list.append(element_name)
        inst_combo.addItems(element_list)
        inst_combo.setCurrentIndex(element_list.index(data["Instrument_name"].
                                                      value))
        self._inst_combo.append(inst_combo)
        inst_combo.currentIndexChanged.connect(self.create_inst_slot(data,
                                                                     index))
        exp_data_table.setCellWidget(index, 1, inst_combo)
        theta_combo = QComboBox(self)
        theta_combo.addItem("Yes")
        theta_combo.addItem("No")
        if not data["2_Theta"].value:
            theta_combo.setCurrentIndex(1)
        theta_combo.currentIndexChanged.connect(self.create_theta_slot(data))
        exp_data_table.setCellWidget(index, 2, theta_combo)

    def append_model(self, model):
        """ append model to model table
        """
        model_table = self.findChild(QTableWidget, "model_table")
        index = model_table.rowCount()
        model_table.setRowCount(index+1)
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setText(model["name"].value)
        model_table.setItem(index, 0, item)
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setText(model["ambient"]["name"].value)
        model_table.setItem(index, 1, item)
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setText(model["substrate"]["name"].value)
        model_table.setItem(index, 2, item)
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setText(uni([lay["name"] for lay in model["layers"]]))
        model_table.setItem(index, 3, item)

    def create_model(self):
        """ create new model
        """
        title = "New model"
        meesage = "New model name"
        result = QInputDialog.getText(self, title, meesage)
        if result[1]:
            self._centralizer.controller.create_model(self._data["name"].value,
                                                      result[0])

    def copy_model(self):
        """ copy selected model
        """
        title = "Model copy"
        meesage = "New model name"
        result = QInputDialog.getText(self, title, meesage)
        if result[1]:
            line_num = self._model_table.currentRow()
            source_name = self._model_table.item(line_num, 0).text()
            title = "Model copy"
            mesage = "New model name"
            list_sample = [name for name in self._centralizer.database.keys()
                           if isinstance(self._centralizer.database[name],
                                         pyxcel.engine.database.PhysicalSample)
                           ]
            sample = QInputDialog.getItem(self, title, mesage, list_sample,
                                          current=0, editable=False)
            if sample[1]:
                self._centralizer.controller.copy_model(source_name,
                                                        uni(sample[0]),
                                                        uni(result[0]))

    def refresh(self):
        """ refresh widget
        """
        database = self._centralizer.database
        self.recreate_header()
        for model in self._data["models"]:
            self.append_model(database[model])
        for data in self._data["data"]:
            self.append_exp_data(database[data])

    def add_experimental_data(self):
        """ add new experimental data
        """
        database = self._centralizer.database
        if len(database['tree']["children"][0]["children"]) <= 0:
            message = "Create an instrument first before adding experimental data"
            title = "No instrument"
            self._m = QMessageBox.warning(self, title, message)
            return
        else:
            instrument_list = [element["name"].value for element in
                               database['tree']["children"][0]["children"]]
            choose_instrument_title = "Intrument selection"
            instrument_name = QInputDialog.getItem(self,
                                                   choose_instrument_title,
                                                   "Instrument",
                                                   instrument_list)
            try:
                is_ok = instrument_name[1]
                if isinstance(is_ok, str):
                    is_ok = instrument_name[0] != ""
                    instrument_name = instrument_name[0]
            except IndexError:
                is_ok = False
            if is_ok:
                exp_data_txt = "Data file"
                file_name = QFileDialog.getOpenFileName(self, exp_data_txt)
                try:
                    is_ok = file_name[1]
                    if isinstance(is_ok, str):
                        is_ok = file_name[0] != ""
                        file_name = file_name[0]
                except IndexError:
                    is_ok = False
                if is_ok:
                    controller = self._centralizer.controller
                    controller.add_exp_data(file_name, instrument_name[0],
                                            self._data["name"].value)
                    self._data.emit_modify()
