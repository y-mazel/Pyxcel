# -*- coding: utf8 -*-
"""
Contain filter for defining physical parameter.

    :platform: Unix, Windows
    :synopsis: Module for modeling an experiment.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import paf.filter_base
import paf.data as data
import paf.port as port
from pyxcel.engine.modeling.entity import InstrumentData, StackData
MAKE_DATA = data.make_data


class ApplyPhysicalParameter(paf.filter_base.Filter):
    """ create a GenX compatible model for XRR from an instrument and a stack
    Data.
    """
    def __init__(self):
        """ initialization
        """
        # create filter
        paf.filter_base.Filter.__init__(self, StackData(), StackData())

        # add input port
        self.input_port["instrument"] = port.Port(InstrumentData())

        # add output port
        self.output_port["instrument"] = port.Port(InstrumentData())
        self.output_port["sample_name"] = port.Port(MAKE_DATA({}))

    def run(self):
        """ running
        """

        # get needed data
        instrument_data = self.get_data("instrument")
        sample_data = self.get_data("main")
        wavelength = instrument_data["source"]['wavelength'].value

        # create sample GenX
        sample_data.wavelength = wavelength

        self.fill_port("main", sample_data)
        self.fill_port("instrument", instrument_data)
        self.fill_port("sample_name", MAKE_DATA({"sample": sample_data}))
