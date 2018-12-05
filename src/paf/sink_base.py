# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
To create a new sink you must create a new class extending Sink class.


   :platform: Unix, Windows
   :synopsis: A base to create sink on a pipeline

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta, abstractmethod
import paf.data
import paf.port
import paf.element
from paf.synchronizing import synchronized
import threading
import sys
MAKE_DATA = paf.data.make_data

if sys.version_info[0] >= 3:
    unicode = str


class Sink(paf.element.Element):
    """ Abstract base class to defined a sink
    """
    __metaclass__ = ABCMeta

    def __init__(self, data_type=MAKE_DATA()):
        """ initialization

        :param data_type: a data sample to determine the data type of main port
        :type data_type: paf.data.Data
        """
        paf.element.Element.__init__(self)
        local_port = paf.port.Port(data_type)
        #: _data of the actual session
        self._data = {"main": None}
        #: list of all input port
        self._input_port = paf.port.PortDictonary({"main": local_port}, self,
                                                  True)
        #: thread of sink
        self._runner = None
        #: lock for input port access
        self.lock = threading.RLock()

    @property
    def input_port(self):
        """ setter for list of input port
        """
        return self._input_port

    def _pre_finish(self):
        """ return true if the preceeding elements are finished
        """
        for pipe in self._input_port.pipes:
            if pipe[0].is_fill and not self._is_stop:
                return False
            elif pipe[0].input is not None:
                if not pipe[0].input.is_finish:
                    return False
            return True

    @property
    def is_finish(self):
        """ return tru if the sink and all connected pump is finished.
        """
        if self._is_finished:
            return True
        else:
            if self._is_stop:
                self._is_finished = self._pre_finish()
                return self._is_finished
            else:
                return False

    @is_finish.setter
    def is_finish(self, value):
        """ set is finish value
        """
        self._is_finished = value

    def reinit(self):
        """ reinitialization
        """
        paf.element.Element.reinit(self)

    def get_data(self, name):
        """ get _data for actual session

        :param name: name of the data (same of the original port) to get
        :type name: str
        :return: the data
        :rtype: Data
        """
        return self._data[name]

    @synchronized
    def pipe_filled(self):
        """ Method to notify on pipe is filled. *usually this method is call by
        a connected pipe. If all input pipe is filled the method job is call in
        a new thread
        """
        if self._runner is None:
            if self.all_fill():
                self._runner = threading.Thread(target=self.job)
                self._runner.start()

    def job(self):
        """ Method copying the _data of the inputs pipes in self._data while
        the inputs ports is filled, and initialize _parameter and start the run
        method each time.
        """
        self._is_stop = False
        while self.all_fill():
            for key in self._input_port.keys():
                self._data[key] = self._input_port[key].pipes[0].pop()
            self.run()
        self._runner = None
        self._is_stop = True
        if self._pre_finish():
            self._is_finished = True

    @synchronized
    def all_fill(self):
        """ Method for verifying if all input port is fill

        :return: true if all input port is full.
        :rtype: boolean
        """
        for pipe in self.input_port.pipes:
            if not pipe[0].is_fill:
                return False
        return True

    @abstractmethod
    def run(self):
        """ Abstract method to define the sinking
        """
        pass
