# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit a stack to adjust it before fitting.

    :platform: Unix, Windows
    :synopsis: stack editor.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
from pyxcel.view.cute import QWidget, QTableWidgetItem, QTableWidget
from pyxcel.view.cute import QPushButton, QInputDialog, QApplication
from pyxcel.view.cute import Qt
from pyxcel.engine.database import CompositeDataObservable
import pyxcel.engine.database
import pyxcel.engine.centralizer
try:
    import pyxcel.view.widget.modelisation.fast_stack_editor_4 as former
except ImportError:
    import pyxcel.view.widget.modelisation.fast_stack_editor_5 as former

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class FastStackEditor(QWidget):
    """ widget for fast stack editing
    """
    def __init__(self, parent, field):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        self._data = None
        self._field = field
        self._centralizer = pyxcel.engine.centralizer.Centralizer()

        self._layer_table = self.findChild(QTableWidget, "layer_table")
        self._layer_table.cellChanged.connect(self.modify)

        self._simulate_button = self.findChild(QPushButton, "simulate_button")
        self._simulate_button.clicked.connect(self.simulate)

        self._save_button = self.findChild(QPushButton, "save_button")
        self._save_button.clicked.connect(self.save_stack)

    @property
    def stack_name(self):
        """ acces to stackname
        """
        return self._field.selected_value

    def save_stack(self):
        """ save the actual stack
        """
        title = _translate("sample_editor", "nom", None)
        meesage = _translate("sample_editor", "Nom du nouveau modèle", None)
        result = QInputDialog.getText(self, title, meesage)
        if result[1]:
            title = _translate("sample_editor", "nom", None)
            mesage = _translate("sample_editor", "Nom du nouveau modèle",
                                None)
            list_sample = [name for name in self._centralizer.database.keys()
                           if isinstance(self._centralizer.database[name],
                                         pyxcel.engine.database.PhysicalSample)
                           ]
            sample = QInputDialog.getItem(self, title, mesage, list_sample,
                                          current=0, editable=False)
            if sample[1]:
                name_model = uni(result[0])
                sample_name = uni(sample[0])
                self._centralizer.controller.create_model(sample_name,
                                                          name_model)
                full_name = sample_name + "_" + name_model
                data_to_save = self._data.composite_data
                data_to_save["name"] = full_name
                self._centralizer.database.real_value[full_name] = data_to_save

    def simulate(self):
        """ slot for simulate
        """
        self._parent.active_stack = self._data
        self._parent.active_stack_editor = self
        self._parent.simulate()

    def get_layer_from_row(self, row):
        """ return layer corresponding to the row
        """
        layer = None
        if row == 0:
            layer = self._data["ambient"]
        elif row == self._layer_table.rowCount() - 1:
            layer = self._data["substrate"]
        else:
            row -= 1
            layer = self._data.real_value["layers"][row]
        return layer

    def get_name_by_column(self, column):
        """ return name of the column
        """
        name = "name"
        if column == 1:
            name = "material"
        elif column == 2:
            name = "d"
        elif column == 3:
            name = "numerical_density"
        elif column == 4:
            name = "mass_density"
        elif column == 5:
            name = "sigmar"
        return name

    def modify(self, row, column):
        """ slot to modify a value
        """
        layer = self.get_layer_from_row(row)
        column_name = self.get_name_by_column(column)
        data = None
        if column in [0, 1]:
            data = str(self._layer_table.item(row, column).text())
        else:
            data = float(self._layer_table.item(row, column).text())
        layer[column_name] = data

    def set_data(self, data):
        """ assign a data to the widget
        """
        self._data = CompositeDataObservable(data)
        self._data.connect_to_signal(self.refresh)
        self.refresh()

    def recreate_header(self):
        """ redraw the headers
        """
        self._layer_table.cellChanged.disconnect()
        layer_table = self._layer_table
        layer_table.clear()
        layer_table.setRowCount(0)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(5, item)
        self._former.retranslateUi(self)
        self._layer_table.cellChanged.connect(self.modify)

    def append_layer(self, layer, special=False):
        """ add new layer in tab
        """
        def lim_sig_figs(input_str):
            """ if input string is a number, limits it to 3 significant figures, otherwise do nothing
            """
            try:
                casted = float(input_str)
                return '{x:{f}}'.format(x=casted, f='.3g')
            except ValueError:
                return input_str
                
        self._layer_table.cellChanged.disconnect()
        layer_table = self._layer_table
        index = layer_table.rowCount()
        layer_table.setRowCount(index+1)
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled)
        item.setText(layer["name"].value)
        layer_table.setItem(index, 0, item)
        item = QTableWidgetItem()
        item.setText(layer["material"].value)
        layer_table.setItem(index, 1, item)
        item = QTableWidgetItem()
        if special:
            not_available = "N/A"
            item.setText(not_available)
            item.setFlags(Qt.ItemIsEnabled)
        else:
            item.setText(lim_sig_figs(layer["d"].value))
        layer_table.setItem(index, 2, item)
        item = QTableWidgetItem()
        item.setText(lim_sig_figs(layer["numerical_density"].value))
        layer_table.setItem(index, 3, item)
        item = QTableWidgetItem()
        item.setText(lim_sig_figs(layer["mass_density"].value))
        layer_table.setItem(index, 4, item)
        item = QTableWidgetItem()
        item.setText(lim_sig_figs(layer["sigmar"].value))
        layer_table.setItem(index, 5, item)
        self._layer_table.cellChanged.connect(self.modify)

    def refresh(self):
        """ refresh the view
        """
        self.recreate_header()
        self.append_layer(self._data["ambient"], True)
        for layer in self._data.real_value["layers"]:
            self.append_layer(layer)
        self.append_layer(self._data["substrate"], True)
