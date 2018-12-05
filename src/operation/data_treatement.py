# -*- coding: utf8 -*-
"""
To create a pipeline for data treatement.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.engine.pipeline
import pyxcel.engine.modeling.pumps as pumps
import pyxcel.engine.optimization.fom as fom
import paf.sink_base as sink
import pyxcel.engine.data_treatement


class DataWriter(sink.Sink):
    """ sink for writing data.
    """
    def __init__(self, data_name=""):
        """ initialization
        """
        sink.Sink.__init__(self)
        self._data_name = data_name
        self.add_expected_parameter("temporary_data",
                                    pyxcel.engine.pipeline.TemporaryData(),
                                    pyxcel.engine.pipeline.TemporaryData())

    @property
    def data_name(self):
        """ data name
        """
        return self._data_name

    @data_name.setter
    def data_name(self, value):
        """ setter for data name
        """
        self._data_name = value

    def run(self):
        """ démarage
        """
        dataset = self.get_data("main")
        self["temporary_data"].real_value[self._data_name] = dataset


class DataTreatementOp(pyxcel.engine.pipeline.Pipeline):
    """ create a pipeline of data treatment
    """
    def __init__(self, data_filter, data_name):
        """ initialization
        """
        pyxcel.engine.pipeline.Pipeline.__init__(self)
        # create and add element
        pump = pumps.EntityPump(fom.DataSet)
        pump["el_name"] = data_name
        self.add_element("pump", pump)
        sink = DataWriter(data_name)
        self.add_element("sink", sink)
        self.add_element("data_filter", data_filter)

        # make connection
        self.connect("pump", "data_filter")
        self.connect("data_filter", "sink")


def select_windows(data_name):
    """ create pipeline to select a windows on data
    """
    data_filter = pyxcel.engine.data_treatement.WindowsFilter()
    pipeline = DataTreatementOp(data_filter, data_name)
    pipeline.add_to_essential("data_filter", "inf", "Lower bound")
    pipeline.add_to_essential("data_filter", "sup", "Upper bound")
    return pipeline
