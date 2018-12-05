# -*- coding: utf8 -*-
"""
Filter for doing simulation with a simulator.

    :platform: Unix, Windows
    :synopsis: generic simulation using a simulator.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import numpy as np
import paf.data
import paf.filter_base
import paf.port as port
MAKE_DATA = paf.data.make_data


class GenericGenXSimulatorFilter(paf.filter_base.Filter):
    """ filter for doing simulation using simulator
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)

        # create input port
        p = port.Port(MAKE_DATA())
        self.input_port["instrument"] = p

        # add expected parameter
        self.add_expected_parameter("scan_start", MAKE_DATA(.1), MAKE_DATA(.1))
        self.add_expected_parameter("scan_stop", MAKE_DATA(1.), MAKE_DATA(1.))
        self.add_expected_parameter("points", MAKE_DATA(100), MAKE_DATA(100),
                                    'Number of points')
        self.add_expected_parameter("custom_array", MAKE_DATA(False),
                                    MAKE_DATA(False))
        self.add_expected_parameter("simulator", MAKE_DATA(), MAKE_DATA())
        self.add_expected_parameter("parameter", paf.data.CompositeData({}),
                                    paf.data.CompositeData({}))
        del self.showing_info[-2]
        del self.showing_info[-2]

    def run(self):
        """ running
        """
        simulator = self["simulator"]
        simulator["instrument"] = self.get_data("instrument")
        simulator["parameter"] = self["parameter"]
        simulator["stack"] = self.get_data("main")
        theta_array = None
        if not self["custom_array"].value:
            theta_array = np.linspace(self["scan_start"].value,
                                      self["scan_stop"].value,
                                      self["points"].value)
            simulator["theta_array"] = theta_array
        else:
            theta_array = simulator["theta_array"]
        type_name = simulator.abstract_type.split("_")[-1]
        simulator.initialization(self)
        sim = simulator.simulate()
        self.fill_port("main", MAKE_DATA({type_name: sim,
                                          "theta_array": theta_array,
                                          "composite": True},
                                         abstract="data_"+type_name))
