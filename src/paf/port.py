# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
The port it use to connect a pipe on sink, pump or filter.


    :platform: Unix, Windows
    :synopsis: module for define a port

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.data
MAKE_DATA = paf.data.make_data


class ToManyInputError(Exception):
    """ Exception raise when you try to connect more than one pipe on the same
    input port.
    """
    def __init__(self, value):
        """ initialization

        :param value: value of the message
        """
        self._value = value

    def __str__(self):
        """ string translator

        :return: value of the message
        :rtype: str
        """
        return repr(self._value)


class PortDictonary(object):
    """ define a dictionary of port
    """
    def __init__(self, value, element, input_=False):
        """ initialization
        """
        #: value of the port dictionary
        self._value = value
        #: element
        self._element = element
        #: if it's input type
        self._input = input_

    def __getitem__(self, name):
        """ port getter.

        :param name: name of the port
        :type name: str
        :returns: port
        :rtype: Port
        """
        return self._value[name]

    def __setitem__(self, name, value):
        """ parameter setter.

        :param name: name of the port
        :type name: str
        :param value: new port
        :raises: TypeError, KeyError
        """
        self._value[name] = value

    def __delitem__(self, name):
        """ port deleter.

        :param name: name of the port
        :type name: str
        :returns: port
        :rtype: Port
        """
        del self._value[name]

    def __len__(self):
        """ return number of port in directory
        """
        return len(self._value)

    def items(self):
        """ items of value.
        """
        return self._value.items()

    def keys(self):
        """ keys of value.
        """
        return list(self._value.keys())

    def connect(self, port_name, pipe):
        """ Connect a pipe on a port *This method is usually use by
        paf.pipe.connect function*

        :param port_name: new port name
        :type port_name: str
        :param pipe: pipe to connect
        :type pipe: paf.pipe.Pipe
        """
        if len(self[port_name].pipes) != 0 and self._input:
            raise ToManyInputError("Sink can't have more than 1 input by port")
        self._value[port_name] += pipe
        if self._input:
            pipe.output = self._element
            pipe.output_port = port_name
        else:
            pipe.input = self._element
            pipe.input_port = port_name
            pipe.data_type = self._value[port_name].data_type

    def disconnect(self, pipe):
        """ disconnect a pipe

        :param pipe: pipe to disconnect
        """
        if self._input:
            port_name = pipe.output_port
        else:
            port_name = pipe.input_port
        del self._value[port_name][self._value[port_name].index(pipe)]

    @property
    def value(self):
        """ getter for value
        """
        return self._value

    @value.setter
    def value(self, value):
        """ setter for value
        """
        self._value = value

    @property
    def pipes(self):
        """ get all pipes for all port
        """
        return [port.pipes for (_, port) in self._value.items()]


class Port(object):
    """ class to define a connection port in sink or in pump
    """
    def __init__(self, data_type=MAKE_DATA()):
        """ initialization

        :param data_type: sample of _data of a type the port can support
        :type data_type: paf.data.Data
        """
        #: sample of _data of a type the port can support
        self._data_type = data_type
        #: list of pipe connected on
        self._pipes = []

    def __delitem__(self, key):
        """ call when you use **del x[key]

        :param key: index to delete
        :type key: integer
        """
        del self._pipes[key]

    def index(self, pipe):
        """ return index of the pipe

        param pipe: pipe to have index
        """
        return self._pipes.index(pipe)

    @property
    def data_type(self):
        """ getter for _data_type

        :return: sample of _data of a type the port can support
        :rtype: paf.data.Data
        """
        return self._data_type

    @property
    def pipes(self):
        """ getter of the list of connected pipes

        :return: the list of connected pipes
        :rtype: list of paf.pipe.Pipe
        """
        return self._pipes

    def __iadd__(self, pipe):
        """ redefine += for pipe like connecting pipe

        :param pipe: pipe to connect
        :type pipe: paf.pipe.Pipe
        """
        self._pipes.append(pipe)
        return self
