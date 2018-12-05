# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
A filter is a component being pump and sink at the same time.

To create filter you must create a class who extend Filter class.

    :platform: Unix, Windows
    :synopsis: Module for create filter.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.pump_base
import paf.sink_base
import paf.data
import paf.runnable
from paf.synchronizing import synchronized
from abc import ABCMeta
MAKE_DATA = paf.data.make_data


class Filter (paf.pump_base.PumpInterface, paf.sink_base.Sink):
    """ Abstract class to inherit for create a filter.
    """
    __metaclass__ = ABCMeta

    def __init__(self, data_type_sink=MAKE_DATA(), data_type_pump=MAKE_DATA()):
        """ initialization

        :param data_type_sink: a sample of data for the main input port
        :type data_type_sink: paf.data.Data
        :param data_type_pump: a sample of data for the main output port
        :type data_type_pump: paf.data.Data
        """
        paf.sink_base.Sink.__init__(self, data_type_sink)
        paf.pump_base.PumpInterface.__init__(self, data_type_pump)

    @synchronized
    def pipe_filled(self):
        """ Using for notify the filter when a input pipe is fill
        """
        paf.sink_base.Sink.pipe_filled(self)
        self._stop = False

    def stop(self):
        """ stop the filter
        """
        paf.pump_base.PumpInterface.stop(self)
        paf.runnable.Runnable.stop(self)
        self._stop = False

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
