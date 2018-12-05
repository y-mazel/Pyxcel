# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for moding.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import os.path
import numpy as np
import pyxcel.view.widget.visualization.data_view as data_view
import pyxcel.view.fast_sim
import pyxcel.engine.centralizer
import pyxcel.engine.optimization.fom
from pyxcel.view.widget.composite_editor import clear_layout
from pyxcel.view.mdi_window import MDIWindow
from pyxcel.view.cute import QPushButton, QComboBox, QFileDialog, QWidget
from pyxcel.view.cute import QLineEdit, QApplication, uic
from pyxcel.uni import uni
try:
    import pyxcel.view.analysis_window_4 as former
    QT_VERSION = 4
except ImportError:
    import pyxcel.view.analysis_window_5 as former

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


def choose_presentation_widget(data):
    """ choose the widget to present data
    """
    abstract_data_dict = {"data_XRR": data_view.DataXRR,
                          "data_XRF": data_view.DataXRF,
                          "data_XSW": data_view.DataXSW,
                          "opti_XRR": data_view.DataXRROpt,
                          "opti_XRF": data_view.DataXRFOpt,
                          "experimental_data": data_view.ExperimentalDataView}
    choose = None
    try:
        if data["data"].abstract_type in abstract_data_dict.keys():
            choose = abstract_data_dict[data["data"].abstract_type]
    except KeyError:
        if data.abstract_type in abstract_data_dict.keys():
            choose = abstract_data_dict[data.abstract_type]
    return choose


class AddDataWindow(QWidget):
    """ window for adding data on the graph
    """
    def __init__(self, parent):
        """ initialization
        """
        # create and form window
        QWidget.__init__(self)
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        former = os.path.join(self._centralizer.option.ui_dir, "add_data.ui")
        uic.loadUi(former, self)
        self._parent = parent

        # configuring window
        self.select_combo.addItems(self.get_data_list())
        self.select_combo.currentIndexChanged.connect(self.selecte_data_slot)

        self.legend_edit.setText("new data")

        self.original_data_check.stateChanged.connect(self.show_dataset)

        self.xrf_column_combo.currentIndexChanged.connect(self.selecct_column)

        self.validat_button.clicked.connect(self.validate_slot)

        self.mult_x_edit.textChanged.connect(self.modify_data)

        self.offset_x_edit.textChanged.connect(self.modify_data)

        self.mult_y_edit.textChanged.connect(self.modify_data)

        self.offset_y_edit.textChanged.connect(self.modify_data)

        # declare field
        self._data_to_add_type = None
        self._dataset_to_add = None
        self._dataset_no_mod = None

    @property
    def dataset_to_add(self):
        """ accessing to dataset to add
        """
        return self._dataset_to_add

    @dataset_to_add.setter
    def dataset_to_add(self, value):
        """ setting dataset to add and dataset without modif
        """
        self._dataset_to_add = value
        self._dataset_no_mod = value.create_copy()

    @property
    def data_type(self):
        """ type off data *XRR or XRF*
        """
        return self._data_to_add_type

    def get_data_list(self):
        """" load data list from database
        """
        self._database = self._centralizer.database
        element_list = []
        for element_name in self._database.keys():
            if isinstance(self._database[uni(element_name)],
                          pyxcel.engine.database.ExperimentalData):
                element_list.append(element_name)
        return element_list

    def validate_slot(self):
        """ slot for validate button of add data widget clicked
        """
        new_axes = self.new_axes_check.isChecked()
        legend = self.legend_edit.text()
        self._parent.add_data(self._dataset_to_add, new_axes, legend)

    def show_dataset(self):
        """ show selected dataset
        """
        graphical_layout = self.graphical_widget.layout()
        clear_layout(graphical_layout)
        dataset = self._dataset_to_add
        new_data_view = data_view.ExperimentalDataView(self, dataset, self.
                                                       _data_to_add_type)
        if self.original_data_check.isChecked():
            new_data_view.add_data(self._parent.data_widget.original_dataset)
        graphical_layout.addWidget(new_data_view)

    def selecct_column(self, index):
        """ slot for selecting column
        """
        data_name = uni(self.select_combo.currentText())
        dataset_to_add = pyxcel.engine.optimization.fom.DataSet()
        all_GIXRF_data = np.loadtxt(data_name, skiprows=1)
        dataset_to_add.x = all_GIXRF_data[:, 0]
        dataset_to_add.y = all_GIXRF_data[:, index]
        dataset_to_add.error = np.sqrt(self._dataset_to_add.y)
        if self._database[uni(data_name)]["2_Theta"].value:
            dataset_to_add.x /= 2
        self.dataset_to_add = dataset_to_add
        self.show_dataset()

    def fill_column_selector(self):
        """ fill column selector with column name on currently selected
        data
        """
        clear_layout(self.graphical_widget.layout())
        data_name = uni(self.select_combo.currentText())
        GIXRF_file_header = open(data_name).readline()
        list_column = GIXRF_file_header.split()
        self.xrf_column_combo.clear()
        self.xrf_column_combo.addItems(list_column)

    def modify_data(self):
        """ apply offset and multipliacator on dataset
        """
        try:
            mult_x = float(self.mult_x_edit.text())
            offset_x = float(self.offset_x_edit.text())
            mult_y = float(self.mult_y_edit.text())
            offset_y = float(self.offset_y_edit.text())
            self._dataset_to_add = self._dataset_no_mod.create_copy()
            self._dataset_to_add.x *= mult_x
            self._dataset_to_add.x += offset_x
            self._dataset_to_add.y *= mult_y
            self._dataset_to_add.y += offset_y
            self.show_dataset()
        except ValueError:
            pass

    def selecte_data_slot(self):
        """ slot for notify selected data
        """
        data_name = uni(self.select_combo.currentText())
        if self._database.get_type(data_name) == "XRF":
            self._data_to_add_type = "XRF"
            self.xrf_column_widget.show()
            self.fill_column_selector()
        elif self._database.get_type(data_name) == "XRR":
            self._data_to_add_type = "XRR"
            self.xrf_column_widget.hide()
            # load XRR data file
            dataset_to_add = pyxcel.engine.optimization.fom.DataSet()
            dataset_to_add.load_file(data_name)
            if self._database[uni(data_name)]["2_Theta"].value:
                dataset_to_add.x /= 2
            self.dataset_to_add = dataset_to_add
            self.show_dataset()


class AnalysisWindow(MDIWindow):
    """ window for analysis
    """
    def __init__(self, parent, data=None):
        """ initialization
        """
#         self._centralizer = mpyxcelCentralizer()
#         former = self._centralizer.option.ui_dir + "analysis_window.ui"
        MDIWindow.__init__(self, parent, former.Ui_analysis_windows())
        self._centralizer = pyxcel.engine.centralizer.Centralizer()

        # configuring widget
        self._add_sim_button = self.findChild(QPushButton, "add_sim_button")
        self._add_sim_button.clicked.connect(self.add_fast_sim)

        self._choose_data_combo = self.findChild(QComboBox,
                                                 "choose_data_combo")

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

        self._add_data_button = self.findChild(QWidget, "add_data_button")
        self._add_data_button.clicked.connect(self.select_data_to_add)

        self._fom_selector = self.findChild(QComboBox, "fom_selector")
        for index, fom_name in enumerate(sorted(list(self._centralizer.option.
                                                     fom_dict.keys()))):
            self._fom_selector.addItem(fom_name)
            if fom_name == "b_normalized":
                self._fom_selector.setCurrentIndex(index)
        self._fom_selector.currentIndexChanged.connect(self.change_fom)

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
        return self._main_widget

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
        self._main_widget.add_data(dataset, new_axes, type_, legend)
        self._add_widget = None

    def change_fom(self, index):
        """ slot for changing FOM
        """
        name = uni(self._fom_selector.currentText())
        self._main_widget.fom_func = self._centralizer.option.fom_dict[name]()
        fom = str(self._main_widget.fom)
        self._fom_line.setText(fom)

    def show_fom(self, show=True):
        """ slot for fom calculable

        :param show: if it's true it show the fom widget and hide it if not
        :type show: bool
        """
        if show:
            self._fom_widget.show()
            fom = str(self._main_widget.fom)
            self._fom_line.setText(fom)
        else:
            self._fom_widget.hide()

    def save_data(self):
        """ save data in a file
        """
        file_name = QFileDialog.getSaveFileName(self, "ouvrir")
        try:
            is_ok = file_name[1]
            if isinstance(is_ok, str):
                is_ok = file_name[0] != ""
                file_name = file_name[0]
        except IndexError:
            is_ok = False
        if is_ok:
            self._main_widget.save_to_file(file_name)

    def add_selected_copier(self, copier):
        """ add slot for copy select button.
        """
        self._copy_select_button.show()
        self._copy_select_button.clicked.connect(copier)
        self._to_unconnect = True

    def copy_data(self):
        """ copy actual showing data
        """
        self._main_widget.copy_to_clipboard()

    def new_widget(self, data):
        """ creating new widget
        """
        self._copy_select_button.hide()
        if self._to_unconnect:
            self._copy_select_button.clicked.disconnect()
            self._to_unconnect = False
        self._data = data
        self._choose_data_combo.clear()
        presentation_widget = choose_presentation_widget(data)
        if presentation_widget is None:
            return
        widget = presentation_widget(self, data)
        widget.fom_calculable.connect(self.show_fom)
        try:
            combo = self._choose_data_combo
            combo.addItems(widget.column_list)
            combo.currentIndexChanged.connect(widget.change_XRF_column)
        except:
            pass
        return widget

    def add_fast_sim(self):
        """ add a new fast simulation into graphical view
        """
        if self._data.abstract_type == "experimental_data":
            instrument_name = self._data["Instrument_name"].value
            theta_array = self._main_widget.theta_array
            fast_sim_window = pyxcel.view.fast_sim.FastSim(self.add_simulation,
                                                           theta_array)
            fast_sim_window.instrument = instrument_name
            fast_sim_window.show()
            self._fast_sim_window = fast_sim_window

    def add_simulation(self, data):
        """ add a new simulation in the widget.
        """
        if data.abstract_type == "data_XRR":
            simulation = data["XRR"].value
            self._main_widget.add_simulation(simulation)
        elif data.abstract_type == "data_XRF":
            simulation = data["XRF"].value
            self._main_widget.add_simulation(simulation)
