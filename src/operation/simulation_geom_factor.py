# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
To create a pipeline for simulating XRF geometric factor.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.engine.database as database_pkg
import pyxcel.engine.pipeline
import pyxcel.engine.modeling.pumps as pumps
import pyxcel.engine.simulation.simulation_geom_factor as geom


def simulation_geom_build():
    """ create simulation XRF geometric factor pipeline
    """
    simulation_geom = pyxcel.engine.pipeline.Pipeline()
    instrument_pump = pumps.EntityPump(database_pkg.PhysicalInstrument)
    physical_filter = database_pkg.PhysicalInstrumentFilter()
    simulation_geom.add_element("physical_filter", physical_filter)
    simulation_geom.add_element("instrument_pump", instrument_pump)
    geom_filter = geom.GeomFactorSimulator()
    simulation_geom.add_element("geom_filter", geom_filter, ["main"], True)
    simulation_geom.connect("instrument_pump", "physical_filter")
    simulation_geom.connect("physical_filter", "geom_filter")
    return simulation_geom

pipeline = simulation_geom_build()
