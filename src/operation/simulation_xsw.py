# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
To create a pipeline for simulating XSW.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.engine.pipeline
import pyxcel.engine.modeling.pumps as pumps
import pyxcel.engine.modeling.entity as entity
import pyxcel.engine.simulation.simulation_xsw as xsw
import pyxcel.engine.modeling.physical_parameter as phyp
from pyxcel.uni import uni


def simulation_xsw_build():
    """ create pipeline for XSW simulation
    """
    simulation_xsw = pyxcel.engine.pipeline.Pipeline()

    # creating pump
    instrument = pumps.EntityPump(pyxcel.engine.database.PhysicalInstrument)
    physical_filter = pyxcel.engine.database.PhysicalInstrumentFilter()
    stack = pumps.EntityPump(entity.StackData)
    simulation_xsw.add_element("instrument", instrument)
    simulation_xsw.add_element("stack", stack)
    simulation_xsw.add_element("physical_filter", physical_filter)

    # creating filter
    apply_phy = phyp.ApplyPhysicalParameter()
    simulation_xsw.add_element("apply_phy", apply_phy)
    simulation_xsw.add_element("Simulator", xsw.GenXSWFSimFilter(), ["XSW"],
                               True)

    # create essential parameter
    simulation_xsw.add_to_essential("Simulator", "dz",
                                    uni("Sub-layers thickness"))
    simulation_xsw.add_to_essential("Simulator", "start_theta",
                                    uni("Min angle"))
    simulation_xsw.add_to_essential("Simulator", "end_theta",
                                    uni("Max angle"))
    simulation_xsw.add_to_essential("Simulator", "nb_of_point",
                                    uni("Number of points"))

    # connecting element
    simulation_xsw.connect("instrument", "physical_filter")
    simulation_xsw.connect("physical_filter", "apply_phy",
                           sink_port="instrument")
    simulation_xsw.connect("stack", "apply_phy")
    simulation_xsw.connect("apply_phy", "Simulator")
    simulation_xsw.connect("apply_phy", "Simulator", "instrument",
                           "instrument")

    return simulation_xsw
