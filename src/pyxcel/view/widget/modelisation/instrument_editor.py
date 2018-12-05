# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit a stack for modeling a sample.

    :platform: Unix, Windows
    :synopsis: stack editor.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
from pyxcel.view.cute import QWidget, QPushButton, QLineEdit
try:
    import pyxcel.view.widget.modelisation.instrument_editor_4 as former
except ImportError:
    import pyxcel.view.widget.modelisation.instrument_editor_5 as former


class InstrumentEditor(QWidget):
    """ widget to edit an instrument
    """
    def __init__(self, parent, data):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        self._data = data
        default_value_ed_button = self.findChild(QPushButton,
                                                 "default_value_ed_button")
        default_value_ed_button.clicked.connect(self.edit_default_instrument)
        default_value_edit = self.findChild(QLineEdit, "default_value_edit")
        default_value_edit.setText(uni(self._data["default_value"].value))

    def edit_default_instrument(self):
        """ for extract default instrument from a physical instrument
        """
        self._parent.data = self._data["default_value"]
