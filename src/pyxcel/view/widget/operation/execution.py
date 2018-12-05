# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to see a Pipeline execution.

    :platform: Unix, Windows
    :synopsis: View to Pipeline execution.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from pyxcel.view.cute import QDialog
try:
    import pyxcel.view.widget.operation.execution_4 as former
except ImportError:
    import pyxcel.view.widget.operation.execution_5 as former


class Executionview(QDialog):
    """ class to create a form for show the execution of a pipeline.
    """
    def __init__(self, pipeline):
        QDialog.__init__(self)
        self._pipeline = pipeline
        self._former = former.Ui_Dialog()
        self._former.setupUi(self)
