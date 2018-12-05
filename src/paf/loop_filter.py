# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
The loop filter is a composite filter containing a full pipeline and reinject
the output in the input until the condition is false.

    :platform: Unix, Windows
    :synopsis: For create loop filter

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.filter_base
import paf.port
import paf.composite_filter
import paf.pipe
from paf.synchronizing import synchronized


class OutputFilter(paf.filter_base.Filter):
    """ filter to redirect on output to the output filter.
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)

    def run(self):
        """ when it receive data, it transmit to the output port
        """
        self.fill_port("main", self._data["main"])


class Looper(paf.filter_base.Filter):
    """ filter who synchronize all output port. It run when all output port is
    fill by is output Filter.
    """
    def __init__(self, loop_filter):
        """ initialization

        :param _loop_filter: loop filter
        """
        paf.filter_base.Filter.__init__(self)
        self.output_port.value = {}
        self.input_port.value = {}
        self._loop_filter = loop_filter

    def add_port(self, name, port):
        """ add a new port in output and a copy of this port in output.

        :param name: name of the port
        :type name: str
        :param port: the port to add
        :type port: paf.port.Port
        """
        local_port = paf.port.Port(port.data_type)
        self.input_port[name] = local_port
        self.output_port[name] = port

    def run(self):
        """ choose if the filter loop continue or end.
        """
        if self._loop_filter.condition():
            for key in self._data.keys():
                self._loop_filter.get_input_pump(key).fill_port("main",
                                                                self._data[key]
                                                                )
        else:
            for key in self._data.keys():
                self._loop_filter.fill_port(key, self._data[key])
            self._loop_filter.end()


class LoopFilter(paf.composite_filter.CompositFilter):
    """ Composite filter to be used in loop with reinjecting data
    """
    def __init__(self, boucle_number=10):
        """ initialization

        :param boucle_number: number of loop. *you can use a condition instead*
        :type boucle_number: integer
        """
        paf.composite_filter.CompositFilter.__init__(self)
        self._input_pump = {}
        self.input_port.value = {}
        self._output_sink = {}
        self.output_port.value = {}
        port = paf.port.Port()
        self._looper = Looper(self)
        self.add_port("main", port)
        self._boucle_number = boucle_number
        self._inc = 0

    def get_input_pump(self, key):
        """ access to input data

        :para key: name of the input data to access
        :type key: str
        """
        return self._input_pump[key]

    def add_port(self, name, port):
        """add a new port in output and a copy of this port in output. Create
        a new output filter and connect to a new port of the looper.

        :param name: name of the port
        :type name: str
        :param port: the port to add
        :type port: paf.port.Port
        """
        new_port = paf.port.Port(port.data_type)
        self.input_port[name] = port
        self.output_port[name] = new_port
        self._output_sink[name] = OutputFilter()
        self._looper.add_port(name, port)
        paf.pipe.connect(self._output_sink[name], self._looper,
                         "main", name)

    @synchronized
    def job(self):
        """ redefine to stop the copy of data after once.
        """
        for key in self._input_port.keys():
            self._data[key] = self._input_port[key].pipes[0].pop()
        self.run()

    def condition(self):
        """ return the condition of loop continuation

        :return: true if the loop must continue.
        :rtype: boolean
        """
        self._inc = self._inc + 1
        if self._inc >= self._boucle_number:
            return False
        else:
            return True

    @synchronized
    def end(self):
        """ execute at the end of the loop.
        """
        self._inc = 0
        self._runner = None
        self.pipe_filled()
