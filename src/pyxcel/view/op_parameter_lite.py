# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for edit parameter of an operation.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import pyxcel.view.widget.operation.tab_editor as tab_editor
from pyxcel.view.widget.operation.line_editor import LineEditor
import pyxcel.view.widget.composite_editor as composite_editor
import pyxcel.view.widget.list_editor as list_editor
import pyxcel.engine.centralizer
import pyxcel.engine.pipeline
import paf.data
import pyxcel.view.op_parameter as op_parameter
from pyxcel.view.mdi_window import MDIWindow
from pyxcel.view.cute import QWidget, QPushButton, QMdiArea, QSize
try:
    import pyxcel.view.op_parameter_lite_4 as former
except ImportError:
    import pyxcel.view.op_parameter_lite_5 as former


class OperationParameterLite(MDIWindow):
    """ widget to configure an operation
    """

    #: list of widget for some abstract type
    abstract_type = {"tab_data": tab_editor.TabEditor,
                     "line": LineEditor}

    #: list of widget for some type
    type_widget = {dict: composite_editor.CompositeEditor,
                   list: list_editor.ListEditor}

    def __init__(self, parent, data):
        """ initialization

        :param parent: parent widget
        :type parent: QWidget
        :param controller: controller to modify model
        """
        MDIWindow.__init__(self, parent, former.Ui_Form())
        self._parent = parent
        self._c = pyxcel.engine.centralizer.Centralizer()
        self._pipeline = None
        self._data = None

        self._parametre_button_list = self.findChild(QWidget, "button_list")
        self._data_parameter = self.findChild(QWidget, "data_parameter")

        close_button = self.findChild(QPushButton, "close_button")
        close_button.clicked.connect(self.kill_win)

        full_button = self.findChild(QPushButton, "full_button")
        full_button.clicked.connect(self.open_full_win)

        self.data = data

    def sizeHint(self, *args, **kwargs):
        """ rewrite size hint for give default size for window
        """
        return QSize(600, 400)

    def open_full_win(self):
        """ open full windows with actual pipeline
        """
        if self._pipeline is not None:
            new_form = op_parameter.OperationParameter(self, self._pipeline)
            mdiarea = self._parent._parent.findChild(QMdiArea,
                                                     "operation_mdiarea")
            mdiarea.addSubWindow(new_form)
            new_form.show()

    def kill_win(self):
        """ close the windows
        """
        self.parentWidget().mdiArea().closeActiveSubWindow()

    @staticmethod
    def clear_element(layout):
        """ clear all element on a layout.
        """
        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget() is not None:
                layout.itemAt(i).widget().setParent(None)
            else:
                layout.removeItem(layout.itemAt(i))

    def open_parameter_editor(self):
        """ open the named parameterizable with editor
        """
        self.clear_element(self._data_parameter.layout())
        data_composite = self._data.essential
        self._editor = composite_editor.CompositeEditor(self, data_composite)
        self._data_parameter.layout().addWidget(self._editor)

    @property
    def data(self):
        """ property to access to the data
        """
        return self._data

    @data.setter
    def data(self, data):
        """ setter for data property
        """
        if isinstance(data, pyxcel.engine.pipeline.Pipeline):
            self._data = data
            self._pipeline = data
            self.open_parameter_editor()
        elif isinstance(data, paf.data.Data):
            self._editor.setParent(None)
            self._history.append(self._editor)
            self.clear_element(self._data_parameter.layout())
            if data.abstract_type in list(self.abstract_type.keys()):
                widget_type = self.abstract_type[data.abstract_type]
            elif isinstance(data, paf.data.SimpleData):
                widget_type = composite_editor.CompositeEditor
            else:
                widget_type = self.type_widget[data.data_type]
            self._editor = widget_type(self, data)
            self._data_parameter.layout().addWidget(self._editor)

    def go_back(self):
        """ redefine go back function for parameter part.
        """
        self._editor.setParent(None)
        if len(self._history) > 0:
            self._editor = self._history.pop()
        self._data_parameter.layout().addWidget(self._editor)

    @property
    def data_field(self):
        """ property to access to data field
        """
        return self._parent.data_field

    @property
    def input_field(self):
        """ property to access to the list of input field
        """
        return self._parent.input_field
