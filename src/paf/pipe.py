# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
For connect a pump to a sink, it's better to use connect function.

    :platform: Unix, Windows
    :synopsis: Module for define a pipe.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.data
import paf.sink_base
MAKE_DATA = paf.data.make_data


class NoSink(paf.sink_base.Sink):
    """ default sink for creating alone pipe
    """
    def __init__(self):
        """ constructor
        """
        paf.sink_base.Sink.__init__(self)

    def run(self):
        """ do nothing
        """
        pass


class Pipe(object):
    """ class of pipe
    """

    def __init__(self, data_type=MAKE_DATA()):
        """ initialization

        :param data_typ: a sample _data container to determine the type
        :type data_type: paf._data.Data
        :param sink: sink to notify when the pipe is filled
        :type sink: paf.sink_base.Sink
        """
        #: type of _data can be contain by the pipe
        self._data_type = data_type

        #: output to notify when the pipe is filled
        self._output = NoSink()
        self._output.input_port.connect("main", self)
        #: output prot name
        self._output_port = ""

        #: input
        self._input = None
        #: input prot name
        self._input_port = ""

        #: _data contain in the pipe
        self._data = []

    @property
    def is_fill(self):
        """ return if the pipe contain data

        :returns: true if the pipe contain data, false otherwise
        :rtype: boolean
        """
        return len(self._data) >= 1

    @property
    def data_type(self):
        """ property accessing to data_type
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """ setter for data type the pipe can contain

        :param data_type: a sample of the new data_type
        :type data_type: paf.data.Data
        """
        self._data_type = data_type

    @property
    def output(self):
        """ property for accessing to the output.
        """
        return self._output

    @output.setter
    def output(self, sink):
        """ connect a new output. *This function is automatically call by the
        Sink class*

        :param sink: sink to notify when the pipe is filled
        :type sink: paf.sink_base.Sink
        """
        self._output = sink

    @property
    def input(self):
        """ property for accessing to the input.
        """
        return self._input

    @input.setter
    def input(self, sink):
        """ connect a new input.

        :param sink: sink to notify when the pipe is filled
        :type sink: paf.sink_base.Sink
        """
        self._input = sink

    @property
    def input_port(self):
        """ property for accessing to the input.
        """
        return self._input_port

    @input_port.setter
    def input_port(self, input_port):
        """ connect a new input.

        :param sink: sink to notify when the pipe is filled
        :type sink: paf.sink_base.Sink
        """
        self._input_port = input_port

    @property
    def output_port(self):
        """ property for accessing to the input.
        """
        return self._output_port

    @output_port.setter
    def output_port(self, output_port):
        """ connect a new input.

        :param sink: sink to notify when the pipe is filled
        :type sink: paf.sink_base.Sink
        """
        self._output_port = output_port

    def pop(self):
        """ get the first element of the contained data

        :return: The first element of the contained data
        :rtype: paf.data.Data
        """
        return self._data.pop(0)

    def fill(self, data):
        """ fill the pipe with new data. Notify the output Sink.

        :param data: the new data to fill with
        :type data: paf.data.Data
        :raise: TypeError
        """
        self._data.append(data)
        self._output.pipe_filled()

    def clear(self):
        """ clear all data in the pipe
        """
        self._data = []


def connect(pump, sink, pump_port="main", sink_port="main"):
    """ connect a pump and a sink with an anonymous pipe.

    :param pump: the pump to connect
    :type pump: paf.pump_base.Pump
    :param sink: the sink to connect
    :type sink: paf.sink_pump.Sink
    :param pump_port: name of connecting port of the pump
    :type pump_port: str
    :param sink_port: name of connecting port of the sink
    :type sink: str
    :raise: TypeError
    """
    pipe = Pipe()
    pump.output_port.connect(pump_port, pipe)
    sink.input_port.connect(sink_port, pipe)
    return pipe
