# -*- coding: utf8 -*-
"""
Implementation of class for pumping entities into a pipeline...

    :platform: Unix, Windows
    :synopsis: Module for modeling an experiment.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.pump_base
import paf.data
import pyxcel.engine.centralizer
import pyxcel.engine.pipeline
MAKE_DATA = paf.data.make_data


class EntityPump(paf.pump_base.Pump):
    """ special pump to pump a data in database
    """
    def __init__(self, entity_type):
        """ initialization

        :param entity_type: define type of expected entity
        :param database: database where find the entity
        """
        paf.pump_base.Pump.__init__(self, entity_type())
        self.add_expected_parameter("validate", MAKE_DATA(False),
                                    MAKE_DATA(False))
        self.add_expected_parameter("el_name", MAKE_DATA(""), MAKE_DATA(""))
        self.add_expected_parameter("temporary_data",
                                    pyxcel.engine.pipeline.TemporaryData(),
                                    pyxcel.engine.pipeline.TemporaryData())
        self._entity_type = entity_type
        centralizer = pyxcel.engine.centralizer.Centralizer()
        self._db = centralizer.database

    @property
    def validate(self):
        return self["validate"].value

    @property
    def entity_name(self):
        return self["el_name"].value

    @property
    def entity_type(self):
        """ property for entity type access
        """
        return self._entity_type

    @property
    def data(self):
        """ access to data
        """
        try:
            return self["temporary_data"][self["el_name"].value]
        except KeyError:
            return None

    @data.setter
    def data(self, data_name):
        """ create the copy of data to inject in pipeline
        """
        self["temporary_data"][data_name] = self._db[data_name]
        self["el_name"] = data_name
        self["validate"] = True

    def run(self):
        """ running
        """
        # send data
        try:
            el_name = self["el_name"].value
            temporary_data = self["temporary_data"]
            data = temporary_data[el_name]
            temporary_data[el_name + "_save"] = paf.data.copy_data(data)
            self.fill_port("main", data)
        except KeyError:
            self.fill_port("main", self._db[self["el_name"].value])
