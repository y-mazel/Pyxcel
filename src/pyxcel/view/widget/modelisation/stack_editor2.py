# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit a stack for modeling a sample.

    :platform: Unix, Windows
    :synopsis: stack editor.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import os
import numpy as np
from matplotlib.figure import Figure
import pyxcel.view.modeling_window
import pyxcel.view.fast_sim
import paf.data
import pyxcel.engine.centralizer
import pyxcel.engine.modeling.profile as profile
from pyxcel.view.widget.composite_editor import CompositeEditor, clear_layout
from pyxcel.engine.modeling.entity import LayerProfileData
from pyxcel.uni import uni
from pyxcel.engine.database import CompositeDataObservable
from pyxcel.view.cute import QWidget, QTableWidgetItem, QTableWidget, QSpinBox
from pyxcel.view.cute import QInputDialog, QPushButton, QApplication, QMdiArea
from pyxcel.view.cute import Qt, uic, FigureCanvas, NavigationToolbar, QAction
try:
    import pyxcel.view.widget.modelisation.stack_editor2_4 as former
except ImportError:
    import pyxcel.view.widget.modelisation.stack_editor2_5 as former

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class ProfileFunctionEditor(QWidget):
    """ widget to edit one function in profile
    """
    def __init__(self, parent, index, computer=None):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._index = index
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        ui_file = os.path.join(self._centralizer.option.ui_dir,
                               "profile_func.ui")
        uic.loadUi(ui_file, self)

        # configuring widget
        self.func_combo.addItems(self._centralizer.option.profile_list)
        self.func_combo.currentIndexChanged.connect(self.modify_func)

        self.delete_button.clicked.connect(self.delete)

        self.mat_line.textChanged.connect(self.change_mat)

        # add selected function to layer profile
        default_func_name = self._centralizer.option.profile_list[0]
        default_func = self._centralizer.option.profile_dict[default_func_name]
        if computer is None:
            self._curent_func = default_func()
            self._parent.layer.add_computer(self._curent_func)
        else:
            self._curent_func = computer
            self.mat_line.setText(computer["material"].value)
        kwargs_editor = CompositeEditor(self, self._curent_func["kwargs"])
        self.kwargs_widget.layout().addWidget(kwargs_editor)

    def change_mat(self):
        """ change material definition
        """
        self._curent_func["material"] = uni(self.mat_line.text())

    def delete(self):
        """ delete func
        """
        self._parent.del_func(self._index)

    def decremented_index(self):
        """ decremented current index
        """
        self._index -= 1

    def modify_func(self):
        """ modify current function
        """
        func_name = uni(self.func_combo.currentText())
        func = self._centralizer.option.profile_dict[func_name]
        self._curent_func = func(uni(self.mat_line.text()))
        self._parent.layer.change_computer(self._index, self._curent_func)
        kwargs_editor = CompositeEditor(self, self._curent_func["kwargs"])
        clear_layout(self.kwargs_widget.layout())
        self.kwargs_widget.layout().addWidget(kwargs_editor)


class ProfileEditor(QWidget):
    """ widget to edit a profile
    """
    def __init__(self, stack, layer_index):
        """ initialization
        """
        QWidget.__init__(self)
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        ui_file = os.path.join(self._centralizer.option.ui_dir,
                               "profile.ui")
        uic.loadUi(ui_file, self)
        self._stack = stack
        self._layer_index = layer_index
        self._layer = stack.real_value["layers"][layer_index]
        self._profil_funcs = []

        # config widget
        dens_prof_list = sorted(list(self._centralizer.option.
                                     profile_dens_dict.keys()))
        self.density_combo.addItems(dens_prof_list)
        self.density_combo.currentIndexChanged.connect(self.
                                                       change_density_profile)

        self.add_button.clicked.connect(self.add_profile_func)

        self.retrace_button.clicked.connect(self.draw_final_bars)

        self.delete_button.clicked.connect(self.delete_profile)

        self.x_parameter_spin.valueChanged.connect(self.change_nb_lay)

        # reopen created profile
        if isinstance(self._layer, LayerProfileData):
            for idx, comp in enumerate(self._layer["materials"]['computers']):
                new_prof = ProfileFunctionEditor(self, idx, comp)
                self._profil_funcs.append(new_prof)
                self.func_widget.layout().addWidget(new_prof)
            density_editor = CompositeEditor(self, self._layer["densities"])
            dens_kwargs_widget = self.findChild(QWidget, "dens_kwargs_widget")
            dens_kwargs_widget.layout().addWidget(density_editor)

        # create matplotlib visualizator
        self._fig = Figure((5.0, 4.0), dpi=100)
        self._canvas = FigureCanvas(self._fig)
        self._toolbar = NavigationToolbar(self._canvas, self)
        self.view_widget.layout().addWidget(self._canvas)
        self.view_widget.layout().addWidget(self._toolbar)

    @property
    def layer(self):
        """ return current layer
        """
        return self._layer

    def change_density_profile(self):
        """ slot for changing density profile
        """
        # TODO:
        pass

    def change_nb_lay(self, value):
        """ slot for changing value of nb_lay property
        """
        if isinstance(self._layer, LayerProfileData):
            self._layer.nb_lay = value

    def add_profile_func(self):
        """ add a new function in profile
        """
        if not isinstance(self._layer, LayerProfileData):
            self._layer = LayerProfileData.creat_from_layer(self._layer)
            self._layer["densities"] = profile.LinearDensityProfile()
            density_editor = CompositeEditor(self, self._layer["densities"])
            dens_kwargs_widget = self.findChild(QWidget, "dens_kwargs_widget")
            dens_kwargs_widget.layout().addWidget(density_editor)
            stack = self._stack.real_value["layers"].real_value
            stack[self._layer_index] = self._layer
        index = len(self._layer["materials"]["computers"])
        new_profil = ProfileFunctionEditor(self, index)
        self._profil_funcs.append(new_profil)
        self.func_widget.layout().addWidget(new_profil)

    def del_func(self, index):
        """ delete a function
        """
        self._layer.remove_computer(index)
        self.func_widget.layout().removeWidget(self._profil_funcs[index])
        del self._profil_funcs[index]
        for idx, wid in enumerate(self._profil_funcs):
            if idx >= index:
                wid.decremented_index()

    def draw_final_bars(self):
        """ draw final bar diagram
        """
        self._fig.clear()
        ax1 = self._fig.add_subplot(111)
        self._layer["materials"].create_listifier()
        materials_dict = self._layer.element_conc()
        color_list = ['r', 'g', 'b', 'magenta', 'orange', 'cyan']
        x = self._layer.x
        x2 = [0] + list(x)
        bottom = np.zeros(x.size)
        width = [x2[idx]-x2[idx+1] for idx in range(len(x2)-1)]
        width = np.array(width)
        for idx, (el, conc) in enumerate(materials_dict.items()):
            ax1.bar(x-width-x[0], conc, label=el, bottom=bottom, width=width,
                    color=color_list[idx % len(color_list)])
            bottom += conc
        ax1.legend()
        ax1.set_title('elements')
        ax1.set_xlabel('depth ($\AA$)')
        self._fig.canvas.draw()

    def delete_profile(self):
        """ delete current profile
        """
        self._fig.clear()
        for profil_func in self._profil_funcs:
            self.func_widget.layout().removeWidget(profil_func)
        self._layer = self._layer.to_one_layer()
        stack = self._stack.real_value["layers"].real_value
        stack[self._layer_index] = self._layer


class StackEditor(QWidget):
    """ widget for modeling and editing a stack
    """
    def __init__(self, parent, data):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        self._data = CompositeDataObservable(data)
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        self._data.connect_to_signal(self.refresh)
        self._sigmai_action = None

        # connect signals
        add_layer_button = self.findChild(QPushButton, "add_layer_button")
        add_layer_button.clicked.connect(self.create_new_layer)

        self._layer_table = self.findChild(QTableWidget, "layer_table")
        self._layer_table.cellChanged.connect(self.modify)
        self._layer_table.currentCellChanged.connect(self.cell_selection_change
                                                     )

        delete_layer_button = self.findChild(QPushButton,
                                             "delete_layer_button")
        delete_layer_button.clicked.connect(self.delete_selected_layer)

        up_button = self.findChild(QPushButton, "up_button")
        up_button.clicked.connect(self.up_selected_layer)

        down_button = self.findChild(QPushButton, "down_button")
        down_button.clicked.connect(self.down_selected_layer)

        simulate_button = self.findChild(QPushButton, "simulate_button")
        simulate_button.clicked.connect(self.simulate)

        repetition_spin = self.findChild(QSpinBox, "repetition_spin")
        repetition_spin.setValue(1)
        repetition_spin.valueChanged.connect(self.repetition_change)

        self._layer_table = self.findChild(QTableWidget, "layer_table")

        # refresh view
        self.create_context_menu()
        self.refresh()

    def create_context_menu(self):
        """ add action into context menu
        """
        delete_layer_action = self.findChild(QAction, "delete_layer_action")
        delete_layer_action.triggered.connect(self.delete_selected_layer)
        self._layer_table.addAction(delete_layer_action)

    def add_sigmai_action(self):
        """ add to contexte menu create intermixing action
        """
        self._sigmai_action = self.findChild(QAction, "create_sigmai_action")
        self._sigmai_action.triggered.connect(self.create_intermixing)
        self._layer_table.addAction(self._sigmai_action)

    def remove_sigmai_action(self):
        """ remove to contexte menu create intermixing action
        """
        if self._sigmai_action is not None:
            self._layer_table.removeAction(self._sigmai_action)
            self._sigmai_action = None

    def cell_selection_change(self):
        """ slot for the change of cell selection
        """
        selected_range = self._layer_table.selectedRanges()
        if len(selected_range) != 1:
            self.remove_sigmai_action()
            return
        if selected_range[0].rowCount() == 2:
            self.add_sigmai_action()
        else:
            self.remove_sigmai_action()

    def repetition_change(self, new_value):
        """ change number of repetition of layers
        """
        list_selected_rows = list(set([selcted_item.row() for selcted_item in
                                       self._layer_table.selectedItems()]))
        start = min(list_selected_rows) - 1
        stop = max(list_selected_rows) - 1
        self._data.composite_data.create_substack(start, stop, new_value)
        self.add_repetition()

    def simulate(self):
        """ fast simulation for the actual stack
        """
        if self._parent.ext_window is None:
            main_window = self._centralizer.main_window
            sim_windows = (pyxcel.view.modeling_window.
                           ModelingWindow(main_window))
            mdiarea = main_window.findChild(QMdiArea, "modelisation_mdiarea")
            mdiarea.addSubWindow(sim_windows)
            sim_windows.show()
            self._parent.ext_window = sim_windows
        stack_name = self._data["name"].value
        self.fast_sim_window = pyxcel.view.fast_sim.FastSim(self.show_sim)
        self.fast_sim_window.model = stack_name
        self.fast_sim_window.show()

    def show_sim(self, data):
        """ show simulation result
        """
        self._parent.ext_window.data = paf.data.CompositeData({"data": data},
                                                              abstract="sim")

    def up_selected_layer(self):
        """ up position of selected layer
        """
        list_selected_rows = list(set([selcted_item.row() for selcted_item in
                                       self._layer_table.selectedItems()]))
        for index in list_selected_rows:
            nb_row = self._layer_table.rowCount()
            if index <= 1 or index == nb_row-1:
                return
            index -= 1
            layers = self._data.real_value["layers"].real_value
            (layers[index-1], layers[index]) = (layers[index], layers[index-1])
            self._data.emit_modify()

    def down_selected_layer(self):
        """ down position of selected layer
        """
        list_selected_rows = list(set([selcted_item.row() for selcted_item in
                                       self._layer_table.selectedItems()]))
        for index in reversed(list_selected_rows):
            nb_row = self._layer_table.rowCount()
            if index == 0 or index >= nb_row-2:
                return
            index -= 1
            layers = self._data.real_value["layers"].real_value
            (layers[index+1], layers[index]) = (layers[index], layers[index+1])
            self._data.emit_modify()

    def delete_selected_layer(self):
        """ delete selected layer
        """
        list_selected_rows = list(set([selcted_item.row() for selcted_item in
                                       self._layer_table.selectedItems()]))
        for index in reversed(list_selected_rows):
            nb_row = self._layer_table.rowCount()
            if index == 0 or index == nb_row:
                return
            index -= 1
            try:
                del self._data.real_value["layers"][index]
            except:
                pass
            self._data.emit_modify()

    def create_new_layer(self):
        """ create and add a new layer to the stack
        """
        title = "New layer"
        message = "Name"
        result = QInputDialog.getText(self, title, message)
        if result[1]:
            self._centralizer.controller.create_layer(self._data["name"].value,
                                                      result[0])
        self._data.emit_modify()

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
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        layer_table.setHorizontalHeaderItem(7, item)
        self._former.retranslateUi(self)
        self._layer_table.cellChanged.connect(self.modify)

    def create_edit_profile_slot(self, layer_index):
        """ create a slot for editing profile
        """
        def edit_profile_slot():
            """ slot for editing profile
            """
            self._profile_editor = ProfileEditor(self._data.composite_data,
                                                 layer_index)
            self._profile_editor.show()
        return edit_profile_slot

    def append_layer(self, layer, profile=False):
        """ add new layer in tab
        """
        self._layer_table.cellChanged.disconnect()
        layer_table = self._layer_table
        index = layer_table.rowCount()
        layer_table.setRowCount(index+1)
        item = QTableWidgetItem()
        item.setText(layer["name"].value)
        layer_table.setItem(index, 0, item)
        item = QTableWidgetItem()
        item.setText(layer["material"].value)
        layer_table.setItem(index, 1, item)
        item = QTableWidgetItem()
        if profile:
            item.setText(uni(layer["d"].value))
        else:
            not_available = "N/A"
            item.setText(not_available)
            item.setFlags(Qt.ItemIsEnabled)
        layer_table.setItem(index, 2, item)
        item = QTableWidgetItem()
        item.setText(uni(layer["numerical_density"].value))
        layer_table.setItem(index, 3, item)
        item = QTableWidgetItem()
        item.setText(uni(layer["mass_density"].value))
        layer_table.setItem(index, 4, item)
        item = QTableWidgetItem()
        item.setText(uni(layer["sigmar"].value))
        layer_table.setItem(index, 5, item)
        if profile:
            profile_button = QPushButton("Profile")
            profile_button.clicked.connect(self.
                                           create_edit_profile_slot(index-1))
            self._layer_table.setCellWidget(index, 7, profile_button)
        self._layer_table.cellChanged.connect(self.modify)

    def add_repetition(self):
        """ add repetition column
        """
        def create_apply_slot(index):
            """ create a slot to apply a repetition
            """
            def slot():
                """ slot to apply a repetition
                """
                self._data.composite_data.apply_rep(index)
                self._data.emit_modify()
            return slot
        repetitions = self._data["repetition"]
        for currect_rep, rep in enumerate(repetitions):
            start = rep["start"].value + 1
            apply_button = QPushButton("x " + str(rep["repetition"].value))
            apply_button.clicked.connect(create_apply_slot(currect_rep))
            self._layer_table.setCellWidget(start, 6, apply_button)
            for index in range(start, rep["stop"].value+1):
                self._layer_table
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemIsEnabled)
                item.setText("+")
                self._layer_table.setItem(index, 6, item)

    def refresh(self):
        """ refresh the view
        """
        self.recreate_header()
        self.append_layer(self._data["ambient"])
        for layer in self._data["layers"]:
            self.append_layer(layer, True)
        self.append_layer(self._data["substrate"])
        self.add_repetition()

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
        if column == 6:
            return
        layer = self.get_layer_from_row(row)
        column_name = self.get_name_by_column(column)
        data = None
        if column in [0, 1]:
            data = str(self._layer_table.item(row, column).text())
        else:
            data = float(self._layer_table.item(row, column).text())
        layer[column_name] = data

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
            layer = self._data["layers"][row]
        return layer

    def create_intermixing(self):
        """ create intermixing beetween the two selected layer
        """
        selected_range = self._layer_table.selectedRanges()
        if len(selected_range) != 1:
            return
        if selected_range[0].rowCount() == 2:
            layer1 = self._data["layers"][selected_range[0].
                                          topRow()-1]
            layer2 = self._data["layers"][selected_range[0].
                                          bottomRow()-1]
            name = "mix_"
            name += layer1["name"].value
            name += "_"
            name += layer2["name"].value
            index = selected_range[0].topRow()
            i_layer = LayerProfileData(name=name, d=.5)
            dens1 = layer1["numerical_density"].value
            dens2 = layer2["numerical_density"].value
            i_layer["densities"] = profile.LinearDensityProfile(dens1, dens2)
            self._data.composite_data.real_value["layers"].insert(index,
                                                                  i_layer)
            prof_mat1 = profile.GaussianInterface(layer2["material"].value)
            prof_mat1["kwargs"]["center_of_mass"] = .5
            prof_mat1["kwargs"]["distribution_width"] = 1.
            prof_mat1["kwargs"]["amplitude"] = 1.
            AntiInterface = profile.AntiGaussianInterface
            prof_mat2 = AntiInterface(layer1["material"].value)
            prof_mat2["kwargs"]["center_of_mass"] = .5
            prof_mat2["kwargs"]["distribution_width"] = 1.
            prof_mat2["kwargs"]["amplitude"] = 1.
            i_layer.add_computer(prof_mat1)
            i_layer.add_computer(prof_mat2)
            self.refresh()
        else:
            return
