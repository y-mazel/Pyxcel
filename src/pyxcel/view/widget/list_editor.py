# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit list data.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import paf.data
from pyxcel.uni import uni
from pyxcel.engine.database import ListDataObservable
from pyxcel.view.cute import QWidget, QListWidget, QPushButton
try:
    import pyxcel.view.widget.list_editor_4 as former
except ImportError:
    import pyxcel.view.widget.list_editor_5 as former


class ListEditor(QWidget):
    """ widget to edit list data
    """
    class FalseIndex(object):
        """ imitate an index
        """
        def __init__(self, i):
            """ initialization
            """
            self.i = i

        def row(self):
            """ virtual row
            """
            return self.i

    def __init__(self, parent, data_list):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._index = None

        # create observable if necessary
        if not isinstance(data_list, ListDataObservable):
            data_list = ListDataObservable(data_list)

        #: parent
        self._parent = parent

        #: creating basic form
        self._former = former.Ui_Form()
        self._former.setupUi(self)

        #: data
        self._data = data_list

        #: temporal data
        temp_data = paf.data.copy_data(self._data.list_data)
        self._data_list = ListDataObservable(temp_data)

        # connect the signal
        self.connect_signal()

    def connect_signal(self):
        """ connect all signal and slot
        """
        self._list_view = self.findChild(QListWidget, 'list_widget')
        self.load_list()
        self._list_view.clicked.connect(self.ItemClicked)
        up_button = self.findChild(QPushButton, 'up_button')
        up_button.clicked.connect(self.up_item)
        down_button = self.findChild(QPushButton, 'down_button')
        down_button.clicked.connect(self.down_item)
        add_button = self.findChild(QPushButton, 'add_button')
        add_button.clicked.connect(self.new_item)
        mod_button = self.findChild(QPushButton, 'mod_button')
        mod_button.clicked.connect(self.modify_item)
        del_button = self.findChild(QPushButton, 'del_button')
        del_button.clicked.connect(self.del_item)
        cancel_button = self.findChild(QPushButton, 'cancel_button')
        cancel_button.clicked.connect(self.cancel)
        validate_button = self.findChild(QPushButton, 'validate_button')
        validate_button.clicked.connect(self.validate)

    def validate(self):
        """validate edited list
        """
        self._data.clear()
        for item in self._data_list:
            self._data.append(item)
        self._parent.go_back()

    def cancel(self):
        """ cancel values
        """
        self._parent.go_back()

    def modify_item(self):
        """ edit selected item
        """
        index = self._index.row()
        edit_data = self._data_list[index]
        self._parent.data = edit_data

    def new_item(self):
        """ add a new item
        """
        new_data = paf.data.copy_data(self._data_list[0])
        self._data_list.append(new_data)
        self._index = self.FalseIndex(len(self._data_list)-1)
        self.load_list()

    def up_item(self):
        """ up selected value
        """
        list_ = self._data_list
        index = self._index.row()
        (list_[index], list_[index-1]) = (list_[index-1], list_[index])
        self._index = self.FalseIndex(len(self._data_list)-1)
        self.load_list()

    def down_item(self):
        """ down selected value
        """
        list_ = self._data_list
        index = self._index.row()
        (list_[index], list_[index+1]) = (list_[index+1], list_[index])
        self._index = self.FalseIndex(len(self._data_list)-1)
        self.load_list()

    def load_list(self):
        """ reload the full list
        """
        self._list_view.clear()
        item = False
        for element in self._data_list:
            self._list_view.addItem(uni(element))
            item = True
        if item:
            self._index = self.FalseIndex(0)

    def ItemClicked(self, index):
        """ select a new item
        """
        self._index = index

    def del_item(self):
        """ delete selected item
        """
        del self._data_list[self._index.row()]
        self.load_list()
