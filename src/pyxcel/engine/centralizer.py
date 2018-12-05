# -*- coding: utf8 -*-
"""
Contain the centralizer element for option and database.

    :platform: Unix, Windows
    :synopsis: centralizer

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.engine.database
import pyxcel.controller
import pyxcel.engine.options


class Centralizer(object):
    """ class singleton for centralizing element
    """
    _instance = None

    def __new__(cls, *args, **kargs):
        """ constructor
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kargs)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        """ initialization
        """
        class BasicSimulateur(object):
            """ object to access to basic operation like dictionnary
            """
            def __init__(self, options):
                """ initialization
                """
                self._options = options

            def __getitem__(self, key):
                """ accessing to an operation
                """
                return self._options.get_operation(key)
        self._options = pyxcel.engine.options.Options()
        self._database = pyxcel.engine.database.Database()
        self._controller = pyxcel.controller.DatabaseController()
        self._clipboard = None
        self._main_window = None
        self._basic_simulateur = BasicSimulateur(self._options)

    @property
    def option(self):
        """ access to option object
        """
        return self._options

    @property
    def basic_simulator(self):
        """ property to access to basic simulator
        """
        return self._basic_simulateur

    @property
    def main_window(self):
        """ property for accessing main windows
        """
        return self._main_window

    @main_window.setter
    def main_window(self, value):
        """ setter for main windows
        """
        self._main_window = value

    @property
    def clipboard(self):
        """ property for accessing clipboard
        """
        return self._clipboard

    @clipboard.setter
    def clipboard(self, clipboard):
        """ setter for clipboard
        """
        self._clipboard = clipboard

    @property
    def database(self):
        """ property for accessing database
        """
        return self._database

    @database.setter
    def database(self, database):
        """ setter for database
        """
        self._database = database

    @property
    def controller(self):
        """ property for accessing ccontroller
        """
        return self._controller
