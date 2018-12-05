# -*- coding: utf8 -*-
"""
Filters for doing creating variable parameter.

    :platform: Unix, Windows
    :synopsis: variale parameter.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import numpy as np
import paf.filter_base
import paf.port as port
import paf.data
from pyxcel.engine.optimization.generic import ParaTab, CustomModel
MAKE_DATA = paf.data.make_data


class Variator(paf.filter_base.Filter):
    """ create a series of object with one parameter variiing
    """
    def __init__(self):
        paf.filter_base.Filter.__init__(self)

        # add input
        self.input_port["instrument"] = port.Port()

        # add output
        self.output_port["instrument"] = port.Port()

        # add parameters
        self.add_expected_parameter("start", MAKE_DATA(.1), MAKE_DATA(.1))
        self.add_expected_parameter("stop", MAKE_DATA(1.), MAKE_DATA(1.))
        self.add_expected_parameter("points", MAKE_DATA(10), MAKE_DATA(10))
        self.add_expected_parameter("element", MAKE_DATA(""), MAKE_DATA(""))

    def run(self):
        paf.filter_base.Filter.run(self)
        mod = CustomModel()
        mod.add_sample(self.get_data("main").value)
        inst = self.get_data("instrument").value
        self._mod.add_instrument({inst["name"].value: inst})
        values = np.linspace(self["start"].value, self["stop"].value,
                             self["points"].value).tolist()
        para_tab = ParaTab()
        string_value = "\n" + self.get_data("element").value + "\t"
        for _ in range(7):
            string_value += "\t0"
        for value in values:
            para_tab.x = [value]
            para_tab.apply_to_dict(mod.script_dict, self._result)
            self.fill_port("instrument", mod.instruments[0])
            self.fill_port("main", mod.sample)
