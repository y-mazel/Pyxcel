# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to windows for moding.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from pyxcel.view.mdi_window import MDIWindow
import pyxcel.view.widget.modelisation.sample_editor as sample_editor
import pyxcel.view.widget.modelisation.stack_editor2 as stack_editor
import pyxcel.view.widget.modelisation.instrument_editor_basic as instrument
import pyxcel.view.widget.composite_editor
import pyxcel.view.widget.list_editor
import pyxcel.view.analysis_window as analysis_window
from pyxcel.uni import uni
try:
    import pyxcel.view.modeling_window_4 as former
except ImportError:
    import pyxcel.view.modeling_window_5 as former


class ModelingWindow(MDIWindow):
    """ main window for modeling
    """

    #: list of widget for some abstract type
    abstract_type_widget = {"physical_instrument":
                            instrument.InstrumentEditor,
                            "physical_sample": sample_editor.SampleEditor,
                            "stack": stack_editor.StackEditor,
                            # for compatibility with old database
                            "stake": stack_editor.StackEditor,
                            "data": sample_editor.SampleEditor,
                            "model": sample_editor.SampleEditor
                            }

    #: list of widget for some type
    type_widget = {dict: pyxcel.view.widget.composite_editor.CompositeEditor,
                   list: pyxcel.view.widget.list_editor.ListEditor}

    def __init__(self, parent):
        """ initialization
        """
        MDIWindow.__init__(self, parent, former.Ui_modeling_window())
        data_analisable = ["experimental_data", "data_XRR", "data_XRF",
                           "data_XSW", "opti_XRR", "opti_XRF", "sim"]
        ana_widget = analysis_window.AnalysisWindow
        self._ext_window = None
        for analysable in data_analisable:
            self.abstract_type_widget[analysable] = ana_widget

        # apply number
        self._number = parent.new_modeler_number
        self.setWindowTitle(uni("Modeling Window ") + uni(self._number))

    @property
    def ext_window(self):
        """ accessing to extention windows for drawing result of simulation or
        print data
        """
        return self._ext_window

    @ext_window.setter
    def ext_window(self, value):
        """ setter for extention window
        """
        self._ext_window = value
        old_title = uni(self._ext_window.windowTitle())
        self._ext_window.setWindowTitle(old_title + " (extension of " +
                                        str(self._number) + ")")
        self._ext_window.closeEvent = self.unregistred_ext_window

    def unregistred_ext_window(self, sim_window):
        """ slot for simulation windows closing
        """
        self._ext_window = None

    def new_widget(self, data):
        """ create new widget for data
        """
        if data.abstract_type in list(self.abstract_type_widget.keys()):
            return self.abstract_type_widget[data.abstract_type](self, data)
        else:
            return self.type_widget[data.data_type](self, data)

    @staticmethod
    def add_abstract_type_widget(abstract_type, widget_type):
        """ add new widget type for abstract type
        """
        ModelingWindow.abstract_type_widget[abstract_type] = widget_type

    @staticmethod
    def add_type_widget(type_, widget_type):
        """ add new widget type for type
        """
        ModelingWindow.type_widget[type_] = widget_type
