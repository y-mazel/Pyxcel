# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
To create a very basic pipeline for simulate with a variing value.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.engine.pipeline
import pyxcel.engine.database as database
import pyxcel.engine.modeling.pumps as pumps
import pyxcel.engine.modeling.entity as entity
from pyxcel.engine.simulation.multiple import Variator


def multiple_simulator_build(simulator, model_creator):
    """ create simulation xrr pipeline
    """
    db = pyxcel.engine.centralizer.Centralizer().database

    def create_new_pump_run(self):
        """ create new to redefine pump running
        """
        def new_pump_run():
            """ new to redefine pump running
            """
            # send data
            try:
                el_name = self["el_name"].value
                temporary_data = self["temporary_data"]
                data = temporary_data[el_name]
                self.fill_port("main", data)
            except KeyError:
                self.fill_port("main", db[self["el_name"].value])
        return new_pump_run

    basic_simulation = pyxcel.engine.pipeline.Pipeline()
    instrument_pump = pumps.EntityPump(database.PhysicalInstrument)
    stack_pump = pumps.EntityPump(entity.StackData)
    instrument_pump.run = create_new_pump_run(instrument_pump)
    stack_pump.run = create_new_pump_run(stack_pump)
    basic_simulation.add_element("instrument", instrument_pump)
    basic_simulation.add_element("stack", stack_pump)

    basic_simulation.add_element("GenXiffier", model_creator)

    variator = Variator()
    basic_simulation.add_element("variator", variator)
    basic_simulation.add_to_essential("variator", "start", "Start")
    basic_simulation.add_to_essential("variator", "stop", "End")
    basic_simulation.add_to_essential("variator", "points", "Number of points")
    basic_simulation.add_to_essential("variator", "element", "Element")

    basic_simulation.add_element("Simulator", simulator, ["main"])

    basic_simulation.connect("instrument", "GenXiffier",
                             sink_port="instrument")
    basic_simulation.connect("stack", "GenXiffier")
    basic_simulation.connect("GenXiffier", "Simulator")
    basic_simulation.connect("GenXiffier", "Simulator", "instrument",
                             "instrument")

    return basic_simulation
