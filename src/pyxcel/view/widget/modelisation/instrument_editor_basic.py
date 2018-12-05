# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit a stack for modeling a sample.

    :platform: Unix, Windows
    :synopsis: stack editor.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.view.widget.composite_editor as composite_editor
from pyxcel.view.cute import QWidget, QGroupBox
try:
    import pyxcel.view.widget.modelisation.instrument_editor_basic_4 as former
except ImportError:
    import pyxcel.view.widget.modelisation.instrument_editor_basic_5 as former


class InstrumentEditor(QWidget):
    def __init__(self, parent, data):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        self._data = data
        self._default_value = self._data["default_value"]
        self._source_box = self.findChild(QGroupBox, "source_box")
        source = self._default_value["source"]
        self._source_editor = composite_editor.CompositeEditor(self, source)
        self._source_box_layout = self._source_box.layout()
        self._source_box_layout.addWidget(self._source_editor)
        self._detector_box = self.findChild(QGroupBox, "detector_box")
        self._detector_box_layout = self._detector_box.layout()
        detector = self._default_value["detector"]
        self._detector_editor = composite_editor.CompositeEditor(self,
                                                                 detector)
        self._detector_box_layout.addWidget(self._detector_editor)

    def go_back(self):
        pass
