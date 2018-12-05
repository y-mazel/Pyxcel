# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for view parameter evolution.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
import numpy as np
from re import sub
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from pyxcel.view.mdi_window import MDIWindow
import pyxcel.engine.centralizer
from pyxcel.view.cute import QTableWidget, QTableWidgetItem, Qt, QWidget
from pyxcel.view.cute import QVBoxLayout, FigureCanvas, QAbstractTableModel
from pyxcel.view.cute import QTableView, QPushButton, QVariant
try:
    import pyxcel.view.param_evol_4 as former
except ImportError:
    import pyxcel.view.param_evol_5 as former


class CorrModel(QAbstractTableModel):
    """ model for show correlation matrix
    """
    def __init__(self):
        """ initialization
        """
        QAbstractTableModel.__init__(self)
        self._corr_matrix = np.array([[]])
        self._header = None

    @property
    def corr_matrix(self):
        """ get correlation matrix
        """
        return self._corr_matrix

    @corr_matrix.setter
    def corr_matrix(self, value):
        """ set value for correlation matrix
        """
        self._corr_matrix = value
        start = self.createIndex(0, 0)
        shape = self._corr_matrix.shape
        try:
            stop = self.createIndex(shape[0]-1, shape[1]-1)
        except IndexError:
            stop = self.createIndex(0, 0)
        self.dataChanged.emit(start, stop)

    @property
    def header(self):
        """ get header list
        """
        return self._header

    @header.setter
    def header(self, value):
        """ set header
        """
        self._header = value

    def headerData(self, section, orientation, role):
        """ return header
        """
        if role == Qt.DisplayRole and self.header is not None:
            return self.header[section]
        else:
            return QVariant()

    def columnCount(self, *args, **kwargs):
        """ return number of column
        """
        try:
            return self._corr_matrix.shape[1]
        except IndexError:
            return 1

    def rowCount(self, *args, **kwargs):
        """ return number of row
        """
        try:
            return self._corr_matrix.shape[1]
        except IndexError:
            return 1

    def data(self, index, role):
        """ return data at index
        """
        if role == Qt.DisplayRole and index.isValid():
            return uni(self._corr_matrix[index.column(), index.row()])
        else:
            return QVariant()


class FOMView(QWidget):
    """ viewer for figure of merit
    """
    def __init__(self, parent):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self._fig = Figure((5.0, 4.0), dpi=100)
        self._canvas = FigureCanvas(self._fig)
        self.layout().addWidget(self._canvas)
        self._canvas.setParent(self)
        self._axes = self._fig.add_subplot(111)
        self._axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self._foms = np.array([])
        self._x = np.array([])
        self._resize_cid = self._canvas.mpl_connect("resize_event",
                                                    self.resize_canvas)

    def resize_canvas(self, event=None):
        """ matplotlib event for resizing canvas
        """
        self._fig.tight_layout()

    def append_fom(self, fom):
        """ append a new value to foms
        """
        nb_value = self._x.size
        self._x = np.append(self._x, [nb_value])
        self._foms = np.append(self._foms, [fom])
        self.draw_axes()

    def draw_axes(self):
        """ draw current self._x and self._foms
        """
        self._axes.clear()
        self._axes.plot(self._x, self._foms, 'k-')
        self._axes.set_ylabel('FOM')
        self._axes.set_xlabel('Iteration')
        self._axes.relim()
        self._axes.autoscale_view(True, True, True)
        self._axes.set_xlim(left=0)
        self._axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        self._fig.canvas.draw()
        self.resize_canvas()

    @property
    def foms(self):
        """ return all figure of merite in history
        """
        return self._foms

    @foms.setter
    def foms(self, value):
        """ stter for figure of merite history
        """
        self._foms = value
        self._x = np.linspace(0, value.size-1, value.size)
        self.draw_axes()


class ParamEvolution(MDIWindow):
    """ windows for showing state of an operation
    """
    def __init__(self, parent, op_name):
        """ initialization
        """
        MDIWindow.__init__(self, parent, former.Ui_Form())

        # configure operation
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        self._op = self._centralizer.database.get_operation(uni(op_name))
        self._op = self._op[0]
        self._op.evolution_report.connect(self.refresh_parameter)

        #: fom evolution wiever
        self._fom = FOMView(self)
        self.findChild(QWidget, "fom_widget").layout().addWidget(self._fom)

        corrcoef_button = self.findChild(QPushButton, "corrcoef_button")
        corrcoef_button.clicked.connect(self.show_corr_matrix)

        #: parameter widget
        self._tab = self.findChild(QTableWidget, "parameter_widget")

        #: correlation widget
        self._corr_widget = None

        #: correlation matrix model
        self._corr_model = CorrModel()

    def show_corr_matrix(self):
        """ show correlation matrix
        """
        if self._corr_widget is None:
            self._corr_widget = QTableView()
            self._corr_widget.setModel(self._corr_model)
        self._corr_widget.show()

    def refresh_parameter(self, report):
        """ refresh parameter with new report
        """
        # refresh parameter_widget
        self._tab.setRowCount(0)
        tab_lines = report["param"].value.split("\n")[1:]
        self._fom.append_fom(report["FOM"].value)
        self._corr_model.corr_matrix = report["corr"].value
        for tab_line in tab_lines:
            cells_text = tab_line.split()
            del cells_text[2]
            line_count = self._tab.rowCount()
            self._tab.setRowCount(line_count+1)
            for index in range(5):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled)
                item.setText('{text:{formating}}'.format(text = cells_text[index] if index == 0 else float(cells_text[index]) , formating = 's' if index == 0 else '.3g'))
                self._tab.setItem(line_count, index, item)
#                 self._tab.setItem(lineIdx, index, item)
        self._corr_model.header = report["corr_header"].value
