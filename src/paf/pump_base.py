# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
To create a pump you must create a new class extending Pump.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta, abstractmethod
import paf.data
import paf.element
import paf.port
import threading
MAKE_DATA = paf.data.make_data


class PumpInterface(object):
    """ Abstract class to define a pump.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data_type=MAKE_DATA()):
        """ initialization

        :param data_type: a sample of a _data type the main port support.
        :type data_type: paf._data.Data
        """
        self._current_locker = 0
        local_port = paf.port.Port(data_type)
        #: list of all output port
        self._output_port = paf.port.PortDictonary({"main": local_port}, self)
        self._stop = False
        self._is_finished = False
        self._is_stop = False

    @property
    def output_port(self):
        """ getter for list of output port
        """
        return self._output_port

    @property
    def is_finish(self):
        """ return True if the element is stoped and can't rerun (all connected
        pump is finish too).
        """
        if self._is_finished:
            return True
        else:
            if self._is_stop:
                self._is_finished = True
            return self._is_stop

    @is_finish.setter
    def is_finish(self, value):
        """ set is finish value
        """
        self._is_finished = value

    def fill_port(self, port_name, data):
        """ fill a port. *This method is usually use for output _data*

        :param port_name: name of the port to fill.
        :type port_name: str
        :param data: data for filling the port.
        :type data: paf.data.Data
        """
        port = self._output_port[port_name]
        for pipe in port.pipes:
            pipe.fill(data)

    def stop(self):
        """ stop pumping
        """
        self._stop = True


class Pump(PumpInterface, paf.element.Element):
    """ Abstract class to inherit for create a pump class
    """
    __metaclass__ = ABCMeta

    def __init__(self, data_type=MAKE_DATA()):
        """ initialization

        :param data_type: a sample of a data type the main port support.
        :type data_type: paf.data.Data
        """
        PumpInterface.__init__(self, data_type)
        paf.element.Element.__init__(self)
        #: lock for input port access
        self.lock = threading.RLock()

    def reinit(self):
        """ initialize the thread again.
        """
        self._runner = threading.Thread(target=self.run)
        self._stop = False

    def _wait_endding(self):
        """ thread for wait ending of runner thread
        """
        self._runner.join()
        self._is_stop = True

    def start(self):
        """ method for initialize _parameter and start the pumping.
        """
        self._is_stop = False
        self._data = {}
        self._runner.start()
        threading.Thread(target=self._wait_endding).start()

    def stop(self):
        """ stop the pump.
        """
        PumpInterface.stop(self)
        paf.runnable.Runnable.stop(self)
        self.reinit()

    @abstractmethod
    def run(self):
        """ Abstract method to define the pumping
        """
        pass
