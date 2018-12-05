# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for analysis a result.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import re

import pyxcel.engine.centralizer
from pyxcel.uni import uni
from pyxcel.view.analysis_window import AddDataWindow
from pyxcel.view.analysis_window import choose_presentation_widget
from pyxcel.view.cute import QDateTime
from pyxcel.view.cute import QLineEdit, QApplication, QVBoxLayout, Qt
from pyxcel.view.cute import QPushButton, QComboBox, QFileDialog, QWidget
from pyxcel.view.cute import QTableWidgetItem, QTableWidget, QLabel
from pyxcel.view.mdi_window import MDIWindow
from pyxcel.view.param_evol import FOMView
from pyxcel.view.widget.composite_editor import clear_layout

try:
    import pyxcel.view.full_analysis_window_4 as former
    QT_VERSION = 4
except ImportError:
    import pyxcel.view.full_analysis_window_5 as former

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class FullAnalysisWindow(MDIWindow):
    """ window for analysis
    """
    def __init__(self, parent, data=None):
        """ initialization
        """
#         self._centralizer = mpyxcelCentralizer()
#         former = self._centralizer.option.ui_dir + "analysis_window.ui"
        MDIWindow.__init__(self, parent, former.Ui_Form())
        self._centralizer = pyxcel.engine.centralizer.Centralizer()

        self._final_keys = ["Simulator_XSW", "optimization_filter_end_data"]

        # configuration
        self._categories_dict = {uni("donnée final"): self.get_final}

        # find data widget
        self._data_widget = self.findChild(QWidget, "data_widget")
        self._data_layout = self.findChild(QVBoxLayout, "data_layout")

        # configuring widget
        self._choose_data_combo = self.findChild(QComboBox,
                                                 "choose_data_combo")

        self._category_combo = self.findChild(QComboBox, "category_combo")

        self._save_data_button = self.findChild(QPushButton,
                                                "save_data_button")
        self._save_data_button.clicked.connect(self.save_data)

        self._copy_data_button = self.findChild(QPushButton,
                                                "copy_data_button")
        self._copy_data_button.clicked.connect(self.copy_data)

        self._copy_select_button = self.findChild(QPushButton,
                                                  "copy_select_button")
        self._copy_select_button.hide()

        self._fom_widget = self.findChild(QWidget, "fom_widget")
        self._fom_line = self.findChild(QLineEdit, "fom_line")
        self._fom_widget.hide()

        self._add_result_button = self.findChild(QWidget, "add_result_button")
        self._add_result_button.clicked.connect(self.select_data_to_add)

        self._tab = self.findChild(QTableWidget, "parameter_widget_2")

        self._parameter_selector = self.findChild(QComboBox,
                                                  "parameter_selector")

        # configure fom selectors
        self._fom_selector = self.findChild(QComboBox, "fom_selector")
        for index, fom_name in enumerate(sorted(list(self._centralizer.option.
                                                     fom_dict.keys()))):
            self._fom_selector.addItem(fom_name)
            if fom_name == "b_normalized":
                self._fom_selector.setCurrentIndex(index)
        self._fom_selector.currentIndexChanged.connect(self.change_fom)

        #: fom evolution wiever
        self._fom = FOMView(self)
        parameter_widget = self.findChild(QWidget, "parameter_widget")
        parameter_widget.layout().addWidget(self._fom)

        self._to_unconnect = False
        self._data = None
        if data is not None:
            self.data = data

        # create variable for adding data
        self._add_widget = None

    @property
    def data_widget(self):
        """ accessing to main widget
        """
        return self._data_widget

    @property
    def data(self):
        """ rewrite data from MDI Widget
        """
        return self._data(self)

    @data.setter
    def data(self, value):
        """ new data setter
        """
        self._data = value
        self.load_info()
        best_history_key = "optimization_filter_best_history"
        if best_history_key in list(value["data"].keys()):
            self._parameter_selector.setCurrentIndex(0)
            best_history = value["data"][best_history_key].value
            self._fom.foms = best_history[0][:, -1]
        best_table_key = "optimization_filter_best_sim_table"
        if best_table_key in list(value["data"].keys()):
            self.show_parameter(value["data"][best_table_key].value[0])
        self._category_combo.clear()
        self._category_combo.addItems(list(self._categories_dict.keys()))
        self.choose_category()
        self._choose_data_combo.currentIndexChanged.connect(self.choose_final)

    def load_info(self):
        """ load information on selected result
        """
        date_format = "dddd d MMMM yyyy hh:mm:ss"
        start_label = self.findChild(QLabel, "start_label")
        end_label = self.findChild(QLabel, "end_label")
        foms_label = self.findChild(QLabel, "foms_label")
        start_time = QDateTime()
        start_time_t = int(self._data["start"].value*1000)
        start_time.setMSecsSinceEpoch(start_time_t)
        star_text = start_time.toString(date_format)
        start_label.setText(star_text)
        end_time = QDateTime()
        end_time.setMSecsSinceEpoch(int(self._data["end"].value*1000))
        end_text = end_time.toString(date_format)
        end_label.setText(end_text)
        try:
            foms = ""
            for fom_name in self._data.foms:
                foms += fom_name + ", "
            foms_label.setText(foms[:-2])
        except:
            pass

    def show_parameter(self, tab):
        """ refresh parameter with new report
        """       
        self._tab.setRowCount(0)
        tab_lines = tab.split("\n")[1:]
        for tab_line in tab_lines:
            cells_text = tab_line.split()
            del cells_text[2]
            line_count = self._tab.rowCount()
            self._tab.setRowCount(line_count+1)
            for index in range(5):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled)
                item.setText('{text:{formating}}'.format(text = cells_text[index] if (index == 0) else float(cells_text[index]), formating = 's' if (index == 0) else '.3g'))
                self._tab.setItem(line_count, index, item)

    def choose_category(self):
        """ slot for select a category in category combo
        """
        name = uni(self._category_combo.currentText())
        self._current_cat_data = self._categories_dict[name]()
        list_data = list(self._current_cat_data.keys())
        self._choose_data_combo.clear()
        self._choose_data_combo.addItems(list_data)
        self.choose_final()

    def get_final(self):
        """ get list of final data name
        """
        final_dict = {}
        for key in self._final_keys:
            if key in self._data["data"].keys():
                break
        for idx, data in enumerate(self._data["data"][key]):
            final_dict["resultat "+str(idx)] = data
        return final_dict

    def choose_final(self):
        """ choose final data from the list
        """
        #name = str(uni(self._choose_data_combo.currentText()))
        name = str(uni(self._choose_data_combo.currentText()))
        self.load_dataset(self._current_cat_data[name])

    def select_data_to_add(self):
        """ choose a data in database to add to the graphe
        """
        self._add_widget = AddDataWindow(self)
        self._add_widget.show()
        self._add_widget.selecte_data_slot()

    def add_data(self, dataset, new_axes, legend):
        """ add data to graph slot
        """
        type_ = self._add_widget.data_type
        self._data_widget.add_data(dataset, new_axes, type_, legend)
        self._add_widget = None

    def change_fom(self, index):
        """ slot for changing FOM
        """
        name = uni(self._fom_selector.currentText())
        self._data_widget.fom_func = self._centralizer.option.fom_dict[name]()
        fom = str(self._data_widget.fom)
        self._fom_line.setText(fom)

    def show_fom(self, show=True):
        """ slot for fom calculable

# infinity
        :param show: if it's true it show the fom widget and hide it if not
        :type show: bool
        """
        if show:
            self._fom_widget.show()
            fom = str(self._data_widget.fom)
            self._fom_line.setText(fom)
        else:
            self._fom_widget.hide()

    def save_data(self):
        """ save data in a file
        """
        file_name = QFileDialog.getSaveFileName(self, "Open")
        try:
            is_ok = file_name[1]
            if isinstance(is_ok, str):
                is_ok = file_name[0] != ""
                file_name = file_name[0]
        except IndexError:
            is_ok = False
        if is_ok:
            self._data_widget.save_to_file(file_name)

    def add_selected_copier(self, copier):
        """ add slot for copy select button.
        """
        self._copy_select_button.show()
        self._copy_select_button.clicked.connect(copier)
        self._to_unconnect = True

    def copy_data(self):
        """ copy actual showing data
        """
        self._data_widget.copy_to_clipboard()

    def load_dataset(self, data):
        """ creating new widget
        """
        clear_layout(self._data_layout)
        self._copy_select_button.hide()
        if self._to_unconnect:
            self._copy_select_button.clicked.disconnect()
            self._to_unconnect = False
        presentation_widget = choose_presentation_widget(data)
        if presentation_widget is None:
            return
        widget = presentation_widget(self, data)
        widget.fom_calculable.connect(self.show_fom)
        if widget is not None:
            widget.setContentsMargins(0, 0, 0, 0)
            self._data_widget = widget
            self._data_layout.addWidget(self._data_widget)

    def add_simulation(self, data):
        """ add a new simulation in the widget.
        """
        if data.abstract_type == "data_XRR":
            simulation = data["XRR"].value
            self._data_widget.add_simulation(simulation)
        elif data.abstract_type == "data_XRF":
            simulation = data["XRF"].value
            self._data_widget.add_simulation(simulation)
