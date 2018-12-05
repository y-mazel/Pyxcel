# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
The composite filter is a filter containing a full pipeline.

    :platform: Unix, Windows
    :synopsis: For create composite filter

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.sink_base
import paf.filter_base
import paf.pump_base


class OutputSink(paf.sink_base.Sink):
    """ Sink use by composite filter for map a sink directly to the
    corresponding port.
    """
    def __init__(self, port):
        """ initialization

        :param port: port object for corresponding output port.
        :type port: paf.port.Port
        """
        paf.sink_base.Sink.__init__(self)
        self._output_port = port

    def run(self):
        """ fill the corresponding port
        """
        for pipe in self._output_port.pipes:
            pipe.fill(self._data["main"])


class CompositFilter(paf.filter_base.Filter):
    """ Class to extend for create a composite filter.
    """

    class PDC(paf.port.PortDictonary):
        """ port dictionary for composite filter
        """
        def __init__(self, value, add_element, element, input_):
            """ initialization
            """
            paf.port.PortDictonary.__init__(self, value, element, input_)
            self._add_element = add_element

        def __setitem__(self, name, value):
            """ parameter setter.

            :param name: name of the port
            :type name: str
            :param value: new port
            :raises: TypeError, KeyError
            """
            if name not in self.keys():
                self._add_element(name, value)
            self._value[name] = value

    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)
        self._input_pump = {"main": paf.pump_base.PumpInterface()}
        self._output_sink = {"main": OutputSink(self._output_port["main"])}

        def add_output_sink(name, value):
            """ add output sink slot
            """
            self._output_sink[name] = OutputSink(value)
        self._output_port = CompositFilter.PDC(self._output_port.value,
                                               add_output_sink, self, False)

        def add_input_sink(name, value):
            """ add input sink slot
            """
            self._input_pump[name] = paf.pump_base.PumpInterface()
        self._input_port = CompositFilter.PDC(self._input_port.value,
                                              add_input_sink, self, True)

    def run(self):
        """ every input is redirect to the corresponding input pump.
        """
        for key in self._data.keys():
            self._input_pump[key].fill_port("main", self._data[key])

    def get_input_pump(self, name):
        """ get the input pump corresponding with the input port *name*

        :param name: name of an input port
        :type name: str
        :return: input pump
        :rtype: paf.pump_base.PumpInterface
        """
        return self._input_pump[name]

    def get_output_sink(self, name):
        """ get the output sink corresponding with the output port *name*

        :param name: name of an output port
        :type name: str
        :return: output sink
        :rtype: OutputSink
        """
        return self._output_sink[name]
