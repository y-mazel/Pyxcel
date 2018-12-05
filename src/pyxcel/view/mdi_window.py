# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Common element for all MDI window

    :platform: Unix, Windows
    :synopsis: main windows.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.view.cute import QSize
try:
    from PyQt4.QtGui import QWidget, QVBoxLayout
except ImportError:
    from PyQt5.QtWidgets import QWidget, QVBoxLayout


class MDIWindow(QWidget):
    """ parent for all MDI window
    """

    def __init__(self, parent, former):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._parent = parent
        self._history = []
        # uic.loadUi(former, self)
        self._former = former
        self._former.setupUi(self)
        self._main_widget = self.findChild(QWidget, "main_widget")
        self._main_layout = self.findChild(QVBoxLayout, "main_layout")

    def sizeHint(self, *args, **kwargs):
        """ rewrite size hint for give default size for window
        """
        return QSize(600, 500)

    def refresh(self):
        """ refresh the window
        """
        self.data = self._data
        if self._history:
            self._history.pop()

    def clear_history(self):
        """ clear history of the windows.
        """
        self._history = []

    def go_back(self):
        """ go_back in the windows history.
        """
        self._main_widget.setParent(None)
        self._main_widget.deleteLater()
        if len(self._history) > 0:
            self._main_widget = self._history.pop()
            self._main_layout.addWidget(self._main_widget)
        else:
            self._main_widget = QWidget(self)

    def new_widget(self, data):
        """ create new main widget

        :param data: data for the widget
        """
        pass

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if self._main_widget is not None:
            try:
                self._main_widget.setParent(None)
                self._main_widget.deleteLater()
            except RuntimeError as re:
                print(re)
        self._history.append(self._main_widget)
        self._data = data
        new_widget = self.new_widget(data)
        if new_widget is not None:
            new_widget.setContentsMargins(0, 0, 0, 0)
            self._main_widget = new_widget
            self._main_layout.addWidget(self._main_widget)
