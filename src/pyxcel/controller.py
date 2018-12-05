# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Controller module for modeling.

    :platform: Unix, Windows
    :synopsis: Controller module for modeling.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
import pyxcel.engine.centralizer


def type_inst(instrument):
    """ find if the instrument is XRF
    """
    if instrument.abstract_type == "XRFInstrument":
        return "XRF"
    elif instrument.abstract_type == "XRRInstrument":
        return "XRR"


class DatabaseController(object):
    """ controller for global modification of the database
    """

    def __init__(self):
        """ initialization

        :param database: database to control
        :type database: mpyxcelengine.database.Database
        """
        #: database to control
        self._c = pyxcel.engine.centralizer.Centralizer()

    def create_sample(self, name):
        """ create a new sample in the database.

        :param name: name of the new sample must be create.
        :type name: str
        """
        self._c.database.create_sample(uni(name))

    def create_instrument(self, name, source_type, detector_type,
                          type_instrument):
        """ create a new instrument in the database

        :param name: name of the new instrument must be create.
        :type name: str
        """
        self._c.database.create_instrument(uni(name), source_type,
                                           detector_type, type_instrument)

    def create_model(self, sample_name, name):
        """ create a new modelization for a sample

        :param sample_name: name of the sample to modelize
        :type sample_name: str
        :param name: name of the model to create
        :type name: str
        """
        self._c.database.create_model(uni(sample_name), uni(name))

    def copy_model(self, source_name, sample_name, name):
        """ copy a stack object.

        :param source_name: name of the stack to copy.
        :type source_name: str
        :param sample_name: name of the sample where copy.
        :type sample_name: str
        :param name: name of the new sample.
        """
        self._c.database.copy_model(uni(source_name), uni(sample_name),
                                    uni(name))

    def create_layer(self, stack_name, name):
        """ create a new layer in a stack

        :param stack_name: name of the stack where create the new layer
        :type stack_name: str
        :param name: name of the new layer
        :type name: str
        """
        self._c.database.create_layer(uni(stack_name), uni(name))

    def add_exp_data(self, file_name, instrument_name, sample_name):
        """ add link to experiment data file.

        :param file_name: name of the file
        :type file_name: str
        :param instrument_name: name of the instrument to link
        :type instrument_name: str
        :param sample_name: name of the physical sample
        :type sample_name: str
        """
        self._c.database.add_exp_data(uni(file_name), uni(instrument_name),
                                      uni(sample_name))

    def add_operation(self, name):
        """ add a new operation file

        :param file_name: name of the new file
        :type file_name: str
        """
        self._c.database.add_operation(uni(name))

    def create_op_instance(self, op_name, name_new_op):
        """ execute an operation file.

        :param op_name: name of the operation file
        :type op_name: str
        :param name_new_op: name of the returned operation
        :type name_new_op: str
        """
        self._c.database.create_op_instance(uni(op_name), uni(name_new_op))

    def add_result(self, data, operation_name):
        """ add a result to database.

        :param data: data to save.
        :type data: paf.data.Data
        :param operation_name: name of the operation the data come from.
        :type operation_name: str
        :param entity_list: dictionary of input choosed entity
        :type entity_list: dict
        :param sink_name: name of the producer sink
        :type sink_name: str
        """
        self._c.database.add_result(data, uni(operation_name))

    def launch(self, name):
        """ launch an operation.

        :param name: name of the operation to launch.
        :type name: str
        """
        self._c.database.launch_op(uni(name))

    def end_op(self, name):
        """ set endded for an operation

        :param name: name of the operation to endded.
        :type name: str
        """
        self._c.database.end_op(uni(name))

    def reactivate(self, op_name):
        """ reactivate an operation

        :param op_name: name of operation to reactivate
        type op_name: str
        """
        self._c.database.reactivate(uni(op_name))
