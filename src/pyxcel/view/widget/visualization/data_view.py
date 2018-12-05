"""
Created on 27 mars 2015

@author: GP243515
"""
import pylab as pl
import numpy as np
from matplotlib.figure import Figure
import pyxcel.engine.optimization.fom as fom
import pyxcel.engine.database as database
from pyxcel.engine.centralizer import Centralizer
from pyxcel.view.cute import QWidget, QVBoxLayout, FigureCanvas
from pyxcel.view.cute import NavigationToolbar, pyqtSignal


class Graphical_view(QWidget):
    """ super class for any graphical view
    """
    fom_calculable = pyqtSignal(bool)

    def __init__(self, parent, data):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._data = data
        self._parent = parent
        self._data_set = None
        self._simulation = None
        self._theta_array = None
        self._fom_calculable = True
        self._fom_func = fom.b_normalized()
        self._twinx = None
        self._resize_cid = 0

    @property
    def original_dataset(self):
        """ return the originale dataset
        """
        if self._data_set is not None:
            return self._data_set
        else:
            new_dataset = fom.DataSet()
            new_dataset.x = self._theta_array
            new_dataset.y = self._simulation
            return new_dataset

    @property
    def fom(self):
        """ return FOM of the current simulation if the view have only a
        dataset and a simulation
        """
        if self._data_set is not None and self._simulation is not None:
            data_set = self._data_set.create_copy()
            simulation = self._fom_func.del_error_to_inf(data_set,
                                                         self._simulation)
            return self._fom_func(simulation, data_set)
        else:
            return None

    @property
    def fom_func(self):
        """ accessing to fom function
        """
        return self._fom_func

    @fom_func.setter
    def fom_func(self, value):
        """ setter for fom function
        """
        self._fom_func = value

    def create_canva(self):
        """ create figure and canvas
        """
        self.setLayout(QVBoxLayout(self))
        self.layout().setMargin(0)
        self.layout().setSpacing(0)
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout().addWidget(self.canvas)
        self.layout().addWidget(self.toolbar)
        self.canvas.setParent(self)
        self.axes = self.fig.add_subplot(111)
        self._resize_cid = self.canvas.mpl_connect("resize_event",
                                                   self.resize_canvas)

    def add_simulation(self, simulation, theta_x=None, labal="sim"):
        """ add result of a simulation
        """
        if self._simulation is None and self._fom_calculable:
            self._simulation = simulation
            self.fom_calculable.emit(True)
        else:
            self._fom_calculable = False
            self.fom_calculable.emit(False)
        self.axes.plot(theta_x, simulation, 'r-', label=labal)
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()
        self.fig.canvas.draw()
        self.resize_canvas()

    def add_data(self, data_set, new_axes=False, type_="XRF", labal="data"):
        """ add result of a simulation
        """
        if new_axes:
            if self._twinx is None:
                axes = self.axes.twinx()
                self._twinx = axes
                if type_ == "XRR":
                    axes.set_yscale('log')
            else:
                axes = self._twinx
        else:
            axes = self.axes
        self.fom_calculable.emit(False)
        self._fom_calculable = False
        axes.plot(data_set.x, data_set.y, 'k-', label=labal, marker='o',
                  ms=2.0)
        axes.relim()
        axes.autoscale_view(True, True, True)
        axes.legend()
        self.fig.canvas.draw()
        self.resize_canvas()

    def data_to_str(self):
        """ convert data to string
        """
        result = "not implemented yet"
        return result

    def resize_canvas(self, event=None):
        """ matplotlib event for resizing canvas
        """
        self.fig.tight_layout()

    def save_to_file(self, file_name):
        """ save data to file
        """
        with open(unicode(file_name), "w") as data_file:
            data_file.write(self.data_to_str().decode('utf-8'))

    def copy_to_clipboard(self):
        """ copy courrant show into clipboard
        """
        clipboard = Centralizer().clipboard
        clipboard.setText(self.data_to_str())


class DataXRR(Graphical_view):
    """ data xrr view
    """
    def __init__(self, parent, data):
        """ initialization
        """
        Graphical_view.__init__(self, parent, data)
        self._data = data
        self._theta_array = self._data["data"]["theta_array"].value
        self._simulation = self._data["data"]["XRR"].value
        self.create_canva()
        self.axes.plot(self._theta_array, self._simulation, 'r-',
                       label='XRR sim')
        self.axes.set_yscale('log')
        self.axes.set_ylabel('XRR')
        self.axes.set_xlabel('theta (deg.)')
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()

    def data_to_str(self):
        """ convert data to string
        """
        result = ""
        for line, theta in enumerate(self._theta_array):
            result += str(theta) + "\t" + str(self._simulation[line]) + "\n"
        return result


class DataXRF(Graphical_view):
    """ data xrf view
    """
    def __init__(self, parent, data):
        """ initialization
        """
        Graphical_view.__init__(self, parent, data)
        self._theta_array = self._data["data"]["theta_array"].value
        self._simulation = self._data["data"]["XRF"].value
        self.create_canva()
        self.axes.plot(self._theta_array, self._simulation, 'r-',
                       label='XRF data')
        self.axes.set_ylabel('XRF')
        self.axes.set_xlabel('theta (deg.)')
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()

    def data_to_str(self):
        """ convert data to string
        """
        result = ""
        for line, theta in enumerate(self._theta_array):
            result += str(theta) + "\t" + str(self._simulation[line]) + "\n"
        return result


class DataXSW(Graphical_view):
    """ data xsw view
    """
    def __init__(self, parent, data):
        """ initialization
        """
        Graphical_view.__init__(self, parent, data)

        # load data
        self._theta_array = self._data["theta_array"].value
        self._XSW = self._data["XSW"].value
        self._z_array = self._data["z_array"].value

        # create widget
        self.create_canva()
        self._rlines = None
        self.draw_XSW()

    def copy_selected(self):
        """ copy selected data
        """
        clipboard = Centralizer().clipboard
        result = ""
        for line, caption in enumerate(self._selected_caption):
            result += str(caption) + "\t" + str(self._selected[line]) + "\n"
        clipboard.setText(result)

    def draw_XSW(self):
        """ draw XSW data
        """
        z_interface = self._data["z_interface"].value
        xx, yy = pl.meshgrid(self._theta_array, self._z_array)
        my_plot = self.axes.contourf(xx, yy, self._XSW, 300, vmin=0, vmax=4)
        for z_value in z_interface[:-1]:
            self.axes.plot(self._theta_array, z_value *
                           np.ones(self._theta_array.shape), 'k')
        self.axes.set_title('XSW')
        self.axes.set_xlabel('theta (deg)')
        self.axes.set_ylabel('depth($\AA$)')
        self.fig.colorbar(my_plot, ax=self.axes, extend='max')

        self.axes.legend()
        self._start_point = None
        self._start_data = None
        self._axes_ext = None
        self._click_cid = self.canvas.mpl_connect('button_press_event',
                                                  self.on_click)
        self._click_cid = self.canvas.mpl_connect('button_release_event',
                                                  self.on_release)

    def add_x_graph(self, x):
        """ add a graph for an X
        """
        if self._axes_ext is None:
            self._parent.add_selected_copier(self.copy_selected)
            self.fig.clear()
            self.axes = self.fig.add_subplot(211)
            self.draw_XSW()
            self._axes_ext = self.fig.add_subplot(212)
        else:
            self._axes_ext.clear()
        if self._rlines is not None:
            self._rlines.pop(0).remove()
        line = list(self._z_array).index(x)
        XSW = self._XSW[line]
        self._selected = XSW
        self._selected_caption = self._theta_array
        self._axes_ext.plot(self._theta_array, XSW, 'k-', label='XSW')
        self._axes_ext.set_ylabel('XSW')
        self._axes_ext.set_xlabel('theta (deg.)')
        red_line = np.array([x]*len(list(self._theta_array)))
        self._rlines = self.axes.plot(self._theta_array, red_line, 'r-')
        self.fig.canvas.draw()
        self.resize_canvas()

    def add_y_graph(self, y):
        """ add a graph for an X
        """
        if self._axes_ext is None:
            self._parent.add_selected_copier(self.copy_selected)
            self.fig.clear()
            self.axes = self.fig.add_subplot(211)
            self.draw_XSW()
            self._axes_ext = self.fig.add_subplot(212)
        else:
            self._axes_ext.clear()
        if self._rlines is not None:
            self._rlines.pop(0).remove()
        col = list(self._theta_array).index(y)
        XSW = self._XSW[:, col]
        self._selected = XSW
        self._selected_caption = self._z_array
        self._axes_ext.plot(self._z_array, XSW, 'k-', label='XSW')
        self._axes_ext.set_ylabel('XSW')
        self._axes_ext.set_xlabel('depth')
        red_line = np.array([y]*len(list(self._z_array)))
        self._rlines = self.axes.plot(red_line, self._z_array, 'r-')
        self.fig.canvas.draw()
        self.resize_canvas()

    def on_click(self, event):
        """ event for clicking in canvas
        """
        if event.inaxes == self.axes:
            self._start_point = (event.x, event.y)
            self._start_data = (event.xdata, event.ydata)

    def on_release(self, event):
        """ event for releasing the mouse button
        """
        if event.inaxes == self.axes:
            diff_x = abs(self._start_point[0] - event.x)
            diff_y = abs(self._start_point[1] - event.y)
            if diff_x >= diff_y:
                x = self._z_array[0]
                for depth in self._z_array:
                    if self._start_data[1] >= depth:
                        x = depth
                self.add_x_graph(x)
            else:
                y = self._theta_array[0]
                for depth in self._theta_array:
                    if self._start_data[0] >= depth:
                        y = depth
                self.add_y_graph(y)

    def data_to_str(self):
        """ convert data to string
        """
        result = "depth/angle"
        for theta in self._theta_array:
            result += "\t" + str(theta)
        result += "\n"
        for line, depth in enumerate(self._z_array):
            result += str(depth)
            for value in self._XSW[line]:
                result += "\t" + str(value)
            result += "\n"
        return result


class DataXRROpt(Graphical_view):
    """ data xrr optimized view
    """
    def __init__(self, parent, data):
        """ initialization
        """
        Graphical_view.__init__(self, parent, data)
        self._data = data
        self._theta_array = self._data["theta_array"].value
        self._sim = self._data["XRR_sim"].value
        self._point = self._data["XRR_data"].value
        self.create_canva()
        self.axes.plot(self._theta_array, self._sim, 'r-', label='XRR sim')
        self.axes.plot(self._theta_array, self._point, 'k-', label='XRR data',
                       marker='o', ms=2.0)
        self.axes.set_yscale('log')
        self.axes.set_ylabel('XRR')
        self.axes.set_xlabel('theta (deg.)')
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()

    def data_to_str(self):
        """ convert data to string
        """
        result = ""
        for line, theta in enumerate(self._theta_array):
            result += str(theta) + "\t" + str(self._point[line])
            result += "\t" + str(self._sim[line])
            result += "\n"
        return result


class DataXRFOpt(Graphical_view):
    """ data xrf optimized view
    """
    def __init__(self, parent, data):
        """ initialization
        """
        Graphical_view.__init__(self, parent, data)
        self._theta_array = self._data["theta_array"].value
        self._sim = self._data["XRF_sim"].value
        self._point = self._data["XRF_data"].value
        self.create_canva()
        self.axes.plot(self._theta_array, self._sim, 'r-', label='XRF sim')
        self.axes.plot(self._theta_array, self._point, 'k-', label='XRF data',
                       marker='o', ms=2.0)
        self.axes.set_ylabel('XRF')
        self.axes.set_xlabel('theta (deg.)')
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()

    def data_to_str(self):
        """ convert data to string
        """
        result = ""
        for line, theta in enumerate(self._theta_array):
            result += str(theta) + "\t" + str(self._point[line])
            result += "\t" + str(self._sim[line])
            result += "\n"
        return result


class ExperimentalDataView(Graphical_view):
    """ viewer for experimental data view
    """
    def __init__(self, parent, data, type_=None):
        """ initialization
        """
        Graphical_view.__init__(self, parent, data)
        if ((not isinstance(data, database.ExperimentalData)) and
                (not isinstance(data, fom.DataSet))):
            print("Experimental data view init error : data given not instance of Experimental Data or fom.DataSet")
            return
        self._type_name = ""
        if isinstance(data, fom.DataSet):
            self.create_canva()
            self.load_dataset(data, type_)
        else:
            self.load_from_database()

    @property
    def column_list(self):
        """ accessing to column list
        """
        return self._column_list

    @property
    def theta_array(self):
        """ accessing to data
        """
        return self._theta_array

    @property
    def type(self):
        """ accessing to the type of the data
        """
        return self._type

    def load_dataset(self, data, type_=""):
        """ load a dataset
        """
        self._data_set = data
        self._type = type_
        self._theta_array = data.x
        self._ploted_data = data.y
        self.axes.plot(self._theta_array, data.y, 'k-', label=type_+" data",
                       marker='o', ms=2.0)
        if type_ == "XRR":
            self.axes.set_yscale('log')
        self.axes.set_ylabel(type_)
        self.axes.set_xlabel('theta (deg.)')
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()
        self._point = data.y
        try:                                        ####EDITED
            self.fig.canvas.draw()
        except StopIteration as Se:                 ####
            print("data_view - StopIteration:")     ####
            print(Se)                               ####
            pass                                    ####


    def load_from_database(self):
        """ load data from database
        """
        centralizer = Centralizer()
        self._type = centralizer.database.get_type(self._data)
        file_name = self._data["file_name"].value
        self._file_name = file_name
        self._column_list = []
        if self._type == "XRR":
            input_XRR = fom.DataSet()
            input_XRR.load_file(file_name)
            if self._data["2_Theta"].value:
                input_XRR.x /= 2
            self.create_canva()
            self.load_dataset(input_XRR, "XRR")
        elif self._type == "XRF":
            self._all_GIXRF_data = np.loadtxt(file_name, skiprows=1)
            GIXRF_file_header = open(file_name).readline()
            self._column_list = GIXRF_file_header.split()
        self._sim = None

    def data_to_str(self):
        """ convert data to string
        """
        result = ""
        for line, theta in enumerate(self._theta_array):
            result += str(theta) + "\t" + str(self._point[line])
            if self._sim is not None:
                result += "\t" + str(self._sim[line])
            result += "\n"
        return result

    def change_XRF_column(self, new_column):
        """ slot for current item changing
        """
        new_data = fom.DataSet()
        try:
            self._theta_array = self._all_GIXRF_data[:, 0]
            new_data.x = self._theta_array
            new_data.y = self._all_GIXRF_data[:, new_column]
            new_data.error = np.copy(new_data.y)
        except AttributeError:
            return
        try:
            self.axes.clear()
        except AttributeError:
            self.setLayout(QVBoxLayout(self))
            self.create_canva()
        if self._data["2_Theta"].value:
            new_data.x /= 2
        self.load_dataset(new_data, "XRF")

    def add_simulation(self, simulation, theta_x=None, label=None):
        """ add result of a simulation
        """
        self._simulation = simulation
        self.fom_calculable.emit(True)
        self._sim = simulation
        self.axes.clear()
        if self._type == "XRR":
            self.axes.set_yscale('log')
        theta_array = self.theta_array
        self.axes.plot(theta_array, self._ploted_data, 'k-', label=self._type +
                       ' data', marker='o', ms=2.0)
        self.axes.set_ylabel(self.type)
        self.axes.set_xlabel('theta (deg.)')
        self.axes.plot(self.theta_array, simulation, 'r-', label=self._type +
                       ' sim')
        self.axes.relim()
        self.axes.autoscale_view(True, True, True)
        self.axes.legend()
        self.fig.canvas.draw()
