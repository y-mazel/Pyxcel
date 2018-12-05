# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to main windows.

    :platform: Unix, Windows
    :synopsis: main windows.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import os.path
import logging
import webbrowser
from pyxcel.uni import uni
import pyxcel.view.modeling_window
import pyxcel.view.full_analysis_window
import pyxcel.view.param_evol
import pyxcel.engine.database
import pyxcel.view.create_instrument as ci
import paf.data
import pyxcel.engine.centralizer
import pyxcel.view.op_io
import pyxcel.view.op_graph_run
from pyxcel.view.cute import QMainWindow, QMdiArea, QAction, QTabWidget
from pyxcel.view.cute import QTreeWidget, QInputDialog, QTreeWidgetItem
from pyxcel.view.cute import QApplication, QFileDialog, QMessageBox, QComboBox
from pyxcel.view.cute import QLabel, QPushButton, QMenu, QLocale

import pyxcel.view.main_window_4 as former
# try:
#     import pyxcel.view.main_window_4 as former
# except ImportError:
#     import pyxcel.view.main_window_5 as former
# MAKE_DATA = paf.data.make_data

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig)


def endding():
    """ quit the application
    """
    if QMessageBox.question(None, '', "Do you really want to quit?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No) == QMessageBox.Yes:
        QApplication.quit()


class AbstractChanger(paf.data.CompositeData):
    """ container to change the abstract type of a data
    """

    def __init__(self, data, abstract):
        """ initialization
        """
        self._value = data
        self._abstract_data_type = abstract


class MainWindows(QMainWindow):
    """ class defining the main windows of the application.
    """

    def __init__(self):
        """ initialization
        """
        QMainWindow.__init__(self)
        self._data_io = paf.data.DataIo()
        self._c = pyxcel.engine.centralizer.Centralizer()

        #: number of independent modeling windows create
        self._nb_modeling_windows = -1

        #: current selected operation
        self._current_op = ""

        #: dictionnary assotiating operation to name
        self._op_dict = {}

        #: data tree
        self._former = former.Ui_main_window()
        self._former.setupUi(self)
        self._data_tree = self.findChild(QTreeWidget, "data_tree")
        self.create_mdi_context_menu()
        self.create_tree_context_menu()
        self.connect_signal_action()

        self._c.database.connect_to_signal(self.refresh_database)

        #: workspace for each launched operation
        self._op_workspace = {}
        self._op_workspace[""] = []
        self._c.database.instance_op_notif.connect(self.creating_new_workspace)

        # create first operation windows
        mdiarea = self.findChild(QMdiArea, "operation_mdiarea")
        new_form = pyxcel.view.op_io.OperationIO(self)
        mdiarea.addSubWindow(new_form)
        new_form.create_graph_view()
        new_form.last_selected_view.show()
        new_form.show()
        mdiarea.activateNextSubWindow()
        mdiarea.tileSubWindows()

        self._op_workspace[""].append(new_form)

        #: operation mdi area
        self._op_mdi_area = mdiarea

        # create first analysing windows
        mdiarea = self.findChild(QMdiArea, "analyse_mdiarea")
        new_form = pyxcel.view.full_analysis_window.FullAnalysisWindow(self)
        mdiarea.addSubWindow(new_form)
        new_form.showMaximized()

        # create first modelization windows
        mdiarea = self.findChild(QMdiArea, "modelisation_mdiarea")
        new_form1 = pyxcel.view.modeling_window.ModelingWindow(self)
        mdiarea.addSubWindow(new_form1)
        new_form1.show()
        new_form2 = pyxcel.view.modeling_window.ModelingWindow(self)
        new_form1.ext_window = new_form2
        mdiarea.addSubWindow(new_form2)
        new_form2.show()
        new_form3 = pyxcel.view.modeling_window.ModelingWindow(self)
        mdiarea.addSubWindow(new_form3)
        new_form3.show()
        mdiarea.activateNextSubWindow()
        mdiarea.tileSubWindows()

        self._default_status = "Idle"
        #: status softwar information
        self._status_showing = QLabel(self._default_status)
        self.statusBar().addPermanentWidget(self._status_showing)

        #: item menu to tree element
        self._tree_el = {}

        #: number of running operation
        self._nb_op = 0

        #: list of running operation
        self._op = set()

        #: list of opening widget tool
        self._opening_tools = []

    @property
    def new_modeler_number(self):
        """ get and increment number of modeling windows
        """
        self._nb_modeling_windows += 1
        return self._nb_modeling_windows

    @property
    def op_workspace(self):
        """ accessing to the list of workspace for each operation launched
        """
        return self._op_workspace

    @property
    def current_op(self):
        """ accessing to the name of current operation
        """
        return self._current_op

    def create_starting_windows(self, workspace):
        """ open a new set of starting windows in workspce.

        :param workspace: name of the operation workspace
        :type workspace: str
        """
        mdiarea = self.findChild(QMdiArea, "operation_mdiarea")
        self.set_current_op(workspace)
        new_form = pyxcel.view.op_io.OperationIO(self)
        mdiarea.addSubWindow(new_form)
        new_form.create_graph_view()
        new_form.show()
        new_form.last_selected_view.show()
        mdiarea.tileSubWindows()
        self._op_workspace[workspace] = [new_form]
        self._op_workspace[workspace].append(new_form.last_selected_view)
        return new_form

    def creating_new_workspace(self, name):
        """ create a new workspace for a launched operation.
        """
        name = uni(name)
        self._op_dict[self._c.database.get_operation(name)[0]] = name
        mdiarea = self.findChild(QMdiArea, "operation_mdiarea")
        if name in self._op_workspace.keys():
            for win in self._op_workspace[name]:
                try:
                    win.parent().close()
                except RuntimeError:
                    pass
        new_form = pyxcel.view.param_evol.ParamEvolution(self, name)
        mdiarea.addSubWindow(new_form)
        if name in self._op_workspace.keys():
            new_form.show()
        self._op_workspace[name] = [new_form]
        new_form = pyxcel.view.op_graph_run.OpGraph(self, name)
        mdiarea.addSubWindow(new_form)
        if name in self._op_workspace.keys():
            new_form.show()
        self._op_workspace[name].append(new_form)
        self.set_current_op(name)
        mdiarea.tileSubWindows()
        self._op_selecter.setEditText(self._current_op)
        logging.info("Creating new workspace : %s", name)

    def connect_signal_action(self):
        """ connect all signals for action and other interaction with the GUI
        """
        # datatree
        self._data_tree.itemClicked.connect(self.select_data)
        self._data_tree.itemDoubleClicked.connect(self.activate_data)
        self._data_tree.itemExpanded.connect(self.expand_menu_item)
        self._data_tree.itemCollapsed.connect(self.collapse_menu_item)

        # add new instrument action
        new_instrument_action = self.findChild(QAction,
                                               "new_instrument_action")
        new_instrument_action.triggered.connect(self.create_instrument)

        # add new sample action
        new_sample_action = self.findChild(QAction, "new_sample_action")
        new_sample_action.triggered.connect(self.create_sample)

        # open operation action
        open_operation_action = self.findChild(QAction,
                                               "open_operation_action")
        open_operation_action.triggered.connect(self.open_operation)

        # save database action
        save_database_action = self.findChild(QAction, "save_database_action")
        save_database_action.triggered.connect(self.save_database)

        # exit button
        exit_action = self.findChild(QAction, "exit_action")
        exit_action.triggered.connect(endding)

        # open database action
        DB_open_action = self.findChild(QAction, "DB_open_action")
        DB_open_action.triggered.connect(self.open_database)

        # close database action
        close_DB_action = self.findChild(QAction, "close_DB_action")
        close_DB_action.triggered.connect(self.close_database)

        # operation combobox change
        op_selecter = self.findChild(QComboBox, "running_operation_combo")
        op_selecter.lineEdit().textChanged.connect(self.set_current_op)
        op_selecter.lineEdit().setReadOnly(True)
        self._op_selecter = op_selecter

        # stop button action
        self._stop_button = self.findChild(QPushButton, "stop_button")
        self._stop_button.clicked.connect(self.stop_current_op)

        # add translation
#         self._language_actions = []
#         self.create_translator_action()

        # create tools menu
        self._tools_actions = []
        self.create_tools_menu()

        # add new instrument action
        old_data_import_action = self.findChild(QAction,
                                                "old_data_import_action")
        old_data_import_action.triggered.connect(self.import_old_database)

        # add help connection
        help_action = self.findChild(QAction, "help_action")
        help_action.triggered.connect(self.open_doc)

    def create_tools_menu(self):
        """ create tools menu from options
        """
        def create_open_tools_slot(tool):
            """ create slot for opening a tool

            :param tool: tool widget to open
            :type tool: QWidget
            """
            def open_tools_slot():
                """ slot for opening a tool
                """
                new_tool = tool()
                self._opening_tools.append(new_tool)
                new_tool.show()
            return open_tools_slot
        tools_dict = self._c.option.tools_dict
        tools_menu = self.findChild(QMenu, "tools_menu")
        for tool_name in sorted(list(tools_dict.keys())):
            new_action = tools_menu.addAction(tool_name)
            self._tools_actions.append(new_action)
            tool = tools_dict[tool_name]
            new_action.triggered.connect(create_open_tools_slot(tool))

    def create_translator_action(self):
        """ create action for all .qm in i18n directory
        """
        def create_slot(act, locale_name):
            """ create a new slot for language
            """
            def language_slot():
                """ new slot for language
                """
#                 for lang_action in self._language_actions:
#                     lang_action.setChecked(False)
#                 self.translate(locale_name)
#                 act.setChecked(True)
#             return language_slot
#         i18n_directory = self._c.option.i18n_directory
#         i18n_files = os.listdir(i18n_directory)
#         language_menu = self.findChild(QMenu, "language_menu")
#         for file_name in i18n_files:
#             file_name = os.path.split(file_name)[1]
#             if file_name[-2:] == "qm":
#                 locale = QLocale(file_name[:-3]).nativeLanguageName()
#                 new_action = language_menu.addAction(locale)
#                 self._language_actions.append(new_action)
#                 new_action.triggered.connect(create_slot(new_action,
#                                                          file_name[:-3]))

    def stop_current_op(self):
        """ stopping current operation slot
        """
        name = self._current_op
        self._c.controller.end_op(name)
        logging.info("Stopping operation: %s", name)

    def set_current_op(self, name):
        """ select current lunched operation.
        """
        name = uni(name)
        if name == "":
            self._stop_button.setEnabled(False)
        else:
            self._stop_button.setEnabled(True)
        if name != self._current_op:
            for (i, widget) in enumerate(self._op_workspace[self._current_op]):
                try:
                    widget.parent().hide()
                except RuntimeError:
                    del self._op_workspace[self._current_op][i]
            for (i, widget) in enumerate(self._op_workspace[name]):
                try:
                    widget.parent().show()
                except RuntimeError:
                    pass
        self._current_op = name
        logging.info("setting current operation : %s", name)

    def open_database(self):
        """ open a database file.
        """
        file_name = QFileDialog.getOpenFileName(self, "Open")
        try:
            is_ok = file_name[1]
            if isinstance(is_ok, str):
                is_ok = file_name[0] != ""
                file_name = file_name[0]
        except IndexError:
            is_ok = False
        if is_ok:
#            try:
                self._c.database = (self._data_io.
                                    file_to_data(uni(file_name))['main'])
                self.refresh_database()
                logging.info("Opening databse from file %s", file_name)
#             except:
#                 message = _translate("main_window",
#                                      "base de donnée incompatible")
#                 title = _translate("main_window", "erreur de format")
#                 QMessageBox.about(self, title, message)
#                 logging.error("try to open not well formed database")

    def close_database(self):
        """ close current
        """
        if QMessageBox.question(None, '', "Do you really want to close the current database?",
                                QMessageBox.Yes | QMessageBox.No,
                                QMessageBox.No) == QMessageBox.Yes:
            self._c.database = pyxcel.engine.database.Database()
            self._c.database.instance_op_notif.connect(self.
                                                       creating_new_workspace)
            self._c.database.connect_to_signal(self.refresh_database)
            self.refresh_database()

    def import_old_database(self):
        """ open an old database file.
        """
        file_name = QFileDialog.getOpenFileName(self, "Import old database")
        try:
            is_ok = file_name[1]
            if isinstance(is_ok, str):
                is_ok = file_name[0] != ""
                file_name = file_name[0]
        except IndexError:
            is_ok = False
        if is_ok:
            xml_content = None
            with open(file_name, 'r') as file_open:
                xml_content = file_open.read()
                if xml_content.find("OperationFile") != -1:
                    xml_content = xml_content.replace("OperationFile",
                                                      "Operation")
                if xml_content.find("ObservableStack") != -1:
                    old_value = "database.ObservableStack"
                    new_value = "modeling.entity.StackData"
                    xml_content = xml_content.replace(old_value, new_value)
                if xml_content.find("ObservableLayer") != -1:
                    old_value = "database.ObservableLayer"
                    new_value = "modeling.entity.LayerData"
                    xml_content = xml_content.replace(old_value, new_value)
                if xml_content.find("scipy_d_e_combined.FOM") != -1:
                    old_value = "scipy_d_e_combined.FOM"
                    new_value = "scipy_d_e_combined.Problem"
                    xml_content = xml_content.replace(old_value, new_value)
                if xml_content.find("mo_combined.ParetoFOM") != -1:
                    old_value = "scipy_d_e_combined.ParetoFOM"
                    new_value = "scipy_d_e_combined.ParetoProblem"
                    xml_content = xml_content.replace(old_value, new_value)
                old_value = "medepy"
                new_value = "pyxcel"
                xml_content = xml_content.replace(old_value, new_value)
            try:
                self._c.database = (self._data_io.main_data_format.
                                    from_xml_string(xml_content)['main'])
                self.refresh_database()
                logging.info("Importing old databse from file %s", file_name)
            except:
                message = "Import impossible"
                title = "Format error"
                QMessageBox.about(self, title, message)
                logging.error("tried to import not well formed database")

    def save_database(self):
        """ save a database in a file.
        """
        file_name = uni(QFileDialog.getSaveFileName(self, "Save database"))
#         try:
#             file_name_string = str(uni(file_name).encode('utf-8'))
#             if isinstance(file_name_string, str):
#                 is_ok = file_name_string != ""
#                 file_name = file_name_string
#         except IndexError:
#             is_ok = False
        
        if file_name != "":
            self._data_io.data_to_file(file_name, self._c.database)
            logging.info("Saving database %s", file_name)

    def create_tree_context_menu(self):
        """ create a context menu for the database tree
        """
        new_instrument_acition = self.findChild(QAction,
                                                "new_instrument_acition")
        new_sample_task = self.findChild(QAction, "new_sample_task")
        open_op_action = self.findChild(QAction, "open_op_action")
        delete_action = self.findChild(QAction, "delete_action")

        new_sample_task.triggered.connect(self.create_sample)
        new_instrument_acition.triggered.connect(self.create_instrument)
        open_op_action.triggered.connect(self.open_operation)
        delete_action.triggered.connect(self.delete_selected)
        self._data_tree.addAction(new_instrument_acition)
        self._data_tree.addAction(new_sample_task)
        self._data_tree.addAction(open_op_action)

        # create menu open operation
        self._menu_operation = QMenu(self)
        menu_operation = QAction(self)
        menu_operation.setMenu(self._menu_operation)
        menu_operation.setText("Add operation")
        default_operation_order = self._c.option.default_operation_order
        for text in default_operation_order:
            new_operation = QAction(self)
            new_operation.setText(text)
            self._menu_operation.addAction(new_operation)
            new_operation.triggered.connect(self.
                                            create_add_operation_slot(text))
        self._data_tree.addAction(menu_operation)
        self._data_tree.addAction(delete_action)

    def delete_selected(self):
        """ delete selected element in the database.
        """
        def delete_element(item_name):
            """ delete an item ad it's child from the database

            :param item_name: item name to delete
            """
            tree_item = self._c.database["tree"].find_by_name(item_name)
            for child in tree_item["children"]:
                delete_element(child['name'].value)
            try:
                del self._c.database[item_name]
            except KeyError:
                pass
        selected_elements = self._data_tree.selectedItems()
        for selected_element in selected_elements:
            logging.info("Deletting %s", uni(selected_element.text(0)))
            delete_element(uni(selected_element.text(0)))
            del self._c.database["tree"][uni(selected_element.text(0))]
        self.refresh_database()

    def open_operation(self):
        """ open a python file implementing a new pipeline
        """
        result = QFileDialog.getOpenFileName(self, "Select a python file containing operation(s)")
        try:
            is_ok = result[1]
            if isinstance(is_ok, str):
                is_ok = result[0] != ""
                result = result[0]
        except IndexError:
            is_ok = False
        if is_ok:
            self._c.controller.add_operation(result)
            logging.info("Opening operation %s", result)

    def create_add_operation_slot(self, name):
        """ create add a new operation in working database slot
        """
        name = uni(name)

        def add_operation_slot():
            """ add a new operation in working database
            """
            self._c.controller.add_operation(name)
            logging.info("Opening operation %s", name)
        return add_operation_slot

    def create_mdi_context_menu(self):
        """ create the context menu of all MDI widget.
        """
        action_tile_windows = self.findChild(QAction, "tile_mode_action")
        action_tile_windows.triggered.connect(self.tile_windows)
        action_cascade_windows = self.findChild(QAction,
                                                "casscade_mode_action")
        action_cascade_windows.triggered.connect(self.cascade_windows)

        # modeling
        mdiarea = self.findChild(QMdiArea, "modelisation_mdiarea")
        action_new_win = self.findChild(QAction, "new_mod_win_action")
        action_new_win.triggered.connect(self.new_modelisation_windows)
        mdiarea.addAction(action_new_win)
        mdiarea.addAction(action_tile_windows)
        mdiarea.addAction(action_cascade_windows)

        # operation
        mdiarea = self.findChild(QMdiArea, "operation_mdiarea")
        action_new_win = self.findChild(QAction, "new_op_win_action")
        action_new_win.triggered.connect(self.new_operation_windows)
        mdiarea.addAction(action_new_win)
        mdiarea.addAction(action_tile_windows)
        mdiarea.addAction(action_cascade_windows)

        # analysis
        mdiarea = self.findChild(QMdiArea, "analyse_mdiarea")
        action_new_win = self.findChild(QAction, "new_analyse_win_action")
        action_new_win.triggered.connect(self.new_analysis_windows)
        mdiarea.addAction(action_new_win)
        mdiarea.addAction(action_tile_windows)
        mdiarea.addAction(action_cascade_windows)

    def tile_windows(self):
        """ reorganize windows in tile.
        """
        workspace_tab = self.findChild(QTabWidget, "workspace_tab")
        tab_name = ""
        if workspace_tab.currentIndex() == 0:
            tab_name = "modelisation_mdiarea"
        elif workspace_tab.currentIndex() == 1:
            tab_name = "operation_mdiarea"
        elif workspace_tab.currentIndex() == 2:
            tab_name = "analyse_mdiarea"
        else:
            logging.error("Tab number error %d", workspace_tab.currentIndex())
            tab_name = "modelisation_mdiarea"
        mdiarea = self.findChild(QMdiArea, tab_name)
        mdiarea.tileSubWindows()
        logging.info("Tile subwindows of %s", tab_name)

    def cascade_windows(self):
        """ reorganize windows in tile.
        """
        workspace_tab = self.findChild(QTabWidget, "workspace_tab")
        tab_name = ""
        if workspace_tab.currentIndex() == 0:
            tab_name = "modelisation_mdiarea"
        elif workspace_tab.currentIndex() == 1:
            tab_name = "operation_mdiarea"
        elif workspace_tab.currentIndex() == 2:
            tab_name = "analyse_mdiarea"
        else:
            logging.error("tab number error %d", workspace_tab.currentIndex())
            tab_name = "modelisation_mdiarea"
        mdiarea = self.findChild(QMdiArea, tab_name)
        mdiarea.cascadeSubWindows()
        logging.info("Cascade subwindows of %s", tab_name)

    def new_modelisation_windows(self):
        """ create a new windows to modelize data.
        """
        mdiarea = self.findChild(QMdiArea, "modelisation_mdiarea")
        new_form = pyxcel.view.modeling_window.ModelingWindow(self)
        mdiarea.addSubWindow(new_form)
        new_form.show()
        logging.info("Creating new modeling windows")

    def new_operation_windows(self):
        """ create a new windows to show some data from an specific operation.
        """
        name = self._current_op
        if name == "" or not self._c.database.get_operation(name)[1]:
            new_form = pyxcel.view.op_io.OperationIO(self)
        else:
            new_form = pyxcel.view.param_evol.ParamEvolution(self, name)
        mdiarea = self.findChild(QMdiArea, "operation_mdiarea")
        mdiarea.addSubWindow(new_form)
        self._op_workspace[name].append(new_form)
        new_form.show()
        logging.info("createing new operation windows")

    def new_analysis_windows(self):
        """ create a new windows to analyse some data.
        """
        mdiarea = self.findChild(QMdiArea, "analyse_mdiarea")
        new_form = pyxcel.view.full_analysis_window.FullAnalysisWindow(self)
        mdiarea.addSubWindow(new_form)
        new_form.show()
        logging.info("Creating new analysis windows")

    def create_sample(self):
        """ create a new sample, ask the name with a dialog.
        """
        message = "Name of the new sample"
        title = "New sample"
        result = QInputDialog.getText(self, title, message)
        if result[1]:
            self._c.controller.create_sample(result[0])
            logging.info("Creating sample named : %s", result[0])

    def create_instrument(self):
        """ create a new sample, ask the name with a dialog.
        """
        self._n = ci.CreateInstrument(self)

    def refresh_database(self):
        """ refresh the view of the database.
        """
        # disconnect to signal
        self._c.database.disconnect_to_signal(self.refresh_database)

        def create_sub_tree(q_tree, tree_data):
            for element in tree_data["children"]:
                new_item = QTreeWidgetItem(q_tree)
                new_item.setText(0, element["name"].value)
                new_item.setExpanded(element["expended"].value)
                self._tree_el[element["name"].value] = element
                create_sub_tree(new_item, element)
        tree = self._c.database['tree']
        self._data_tree.clear()
        self._tree_el = {}

        # refresh instrument items
        instrument_item = QTreeWidgetItem(self._data_tree)
        instrument_item_name = "Instrument"
        instrument_item.setText(0, instrument_item_name)
        instrument_item.setExpanded(tree["children"][0]["expended"].value)
        new_tree = tree["children"][0]
        self._tree_el[instrument_item_name] = new_tree
        instrument_data_tree = tree["children"][0]
        create_sub_tree(instrument_item, instrument_data_tree)

        # refresh sample items
        sample_item = QTreeWidgetItem(self._data_tree)
        sample_item_name = "Sample"
        sample_item.setText(0, sample_item_name)
        sample_item.setExpanded(tree["children"][1]["expended"].value)
        self._tree_el[sample_item_name] = tree["children"][1]
        sample_data_tree = tree["children"][1]
        create_sub_tree(sample_item, sample_data_tree)

        # refresh operation items
        operation_item = QTreeWidgetItem(self._data_tree)
        operation_item_name = "Operation"
        operation_item.setText(0, operation_item_name)
        operation_item.setExpanded(tree["children"][2]["expended"].value)
        self._tree_el[operation_item_name] = tree["children"][2]
        operation_data_tree = tree["children"][2]
        create_sub_tree(operation_item, operation_data_tree)

        # refresh operation launched list
        launched_op = [""]
        launched_op = launched_op + list(self._c.database.operations_launched)
        current_op = self._current_op
        self._op_selecter.clear()
        self._op_selecter.addItems(launched_op)
        self._op_selecter.setEditText(current_op)
        self._current_op = current_op

        # reconnect signal
        self._c.database.connect_to_signal(self.refresh_database)

    def collapse_menu_item(self, item):
        """ register collapsing one item in the menu.

        :param item: item collapsed
        :type item: QTreeWidgetItem
        """
        if uni(item.text(0)) in list(self._tree_el.keys()):
            self._tree_el[uni(item.text(0))]["expended"] = False

    def expand_menu_item(self, item):
        """ register expanding one item in the menu.

        :param item: item expanded
        :type item: QTreeWidgetItem
        """
#         modified to solve the Unicode Warning in the if statement "failed to convert both arguments to unicode"
#         if uni(item.text(0)) in list(self._tree_el.keys()): # old if statement
        if uni(item.text(0)) in [uni(x) for x in self._tree_el.keys()]:
            self._tree_el[uni(item.text(0))]["expended"] = True

    def select_data(self, item):
        """ select data in a tree database. Called when a click is made in the left panel ("tree")
        """
        logging.info("Selecting data: %s", uni(item.text(0)))
        selected_element = None
        if uni(item.text(0)) in list(self._tree_el.keys()):
            item_name = uni(item.text(0))
        workspace_tab = self.findChild(QTabWidget, "workspace_tab")
        op = False
        try:
            # selected element correspond to a data
            selected_element = self._c.database[item_name]
        except:
            models_name = uni("Model")
            data_name = uni("Data")
            if item.parent() is not None:
                parent_name = uni(item.parent().text(0))
                # selected element is a part of a sample
                if uni(item_name) == models_name:
                    selected_element = AbstractChanger(self._c.
                                                       database[parent_name],
                                                       abstract='model')
                elif uni(item_name) == data_name:
                    selected_element = AbstractChanger(self._c.
                                                       database[parent_name],
                                                       abstract='data')
                else:
                    try:
                        if item.parent() is not None:
                            parent_element = self._c.database[parent_name]
                            if isinstance(parent_element,
                                          pyxcel.engine.database.Operation):
                                # selected element is an operation
                                workspace_tab.setCurrentIndex(1)
                                op = True
                                selected_element = uni(item_name)
                                self._c.controller.reactivate(item_name)
                                workspace_name = self._op_workspace.keys()
                                if selected_element in workspace_name:
                                    (self._op_selecter.
                                     setEditText(selected_element))
                                else:
                                    self._op_selecter.setEditText("")
                        if selected_element is None:
                            return
                    except KeyError:
                        return
        if isinstance(selected_element, paf.data.Data):
            if selected_element.abstract_type == "results":
                workspace_tab.setCurrentIndex(2)
        if op:
            mdiarea = self.findChild(QMdiArea, "operation_mdiarea")
        elif workspace_tab.currentIndex() == 0:
            mdiarea = self.findChild(QMdiArea, "modelisation_mdiarea")
        elif workspace_tab.currentIndex() == 1:
            mdiarea = self.findChild(QMdiArea, "modelisation_mdiarea")
            workspace_tab.setCurrentIndex(0)
        elif workspace_tab.currentIndex() == 2:
            mdiarea = self.findChild(QMdiArea, "analyse_mdiarea")
        selected_window = mdiarea.activeSubWindow()
        if selected_window is not None:
            selected_window.widget().clear_history()
            if selected_element is not None:
                selected_window.widget().data = selected_element

    def activate_data(self, item):
        """ activate a data (by double click) in a tree database
        """
        item_name = uni(item.text(0))
        logging.info("Activating data: %s", item_name)
        selected_element = None
        try:
            selected_element = self._c.database[item_name]
        except KeyError:
            return
        if isinstance(selected_element, pyxcel.engine.database.Operation):
            message = "Name of the new operation"
            title = "New operation"
            result = QInputDialog.getText(self, title, message)
            if result[1]:
                try:
                    self._c.controller.create_op_instance(item_name, result[0])
                except AttributeError:
                    message = "Name already exists"
                    title = "Naming error"
                    QMessageBox.about(self, title, message)

    def endding_op(self, op):
        """ endding an operation by closing dynamic view and openning relunch
        view.
        """
        self._nb_op -= 1
        self._op.remove(op)
        name = self._op_dict[op]
        self._c.database.get_operation(name)[1] = False
        workspace = self._op_workspace[name]
        if name == self.current_op:
            for win in workspace:
                win.parent().close()
        else:
            for win in workspace:
                win.close()
        new_form = self.create_starting_windows(name)
        new_form.data = name

    def update_state(self, op):
        """ update operation state.
        """
        if op.running:
            if op not in self._op:
                self._nb_op += 1
                self._op.add(op)
        else:
            if op in self._op:
                self.endding_op(op)
        if self._nb_op == 0:
            self._status_showing.setText(self._default_status)
        else:
            self._status_showing.setText(uni(self._nb_op) + uni(" operation running"))

    def error_detected(self, error_type, error_message):
        """ slot for pipeline error detection
        """
        message = ""
        message += uni(error_type)
        message += "\nmessage :\n"
        message += error_message
        QMessageBox.critical(self, "An error happened", message)
        logging.error("Error %s occured", message)

    def translate(self, language):
        """ translate app to selected language
        """
        self._c.option.local = language
        self._former.retranslateUi(self)

    def open_doc(self):
        """ open documentation in webbrowser
        """
        webbrowser.open(os.path.join(self._c.option.doc_dir, "index.html"))
