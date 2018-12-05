# -*- coding: utf8 -*-
"""
Module for create a Pipeline and interact with GUI.

    :platform: Unix, Windows
    :synopsis: Module for define a Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import time
import logging
import numpy as np
import pyxcel.engine.modeling.pumps
import pyxcel.engine.database
import paf.element
import paf.pipe
import paf.pump_base
import paf.sink_base
import paf.data
from pyxcel.view.cute import QObject, pyqtSignal
from paf.synchronizing import synchronized
from pyxcel.uni import uni
MAKE_DATA = paf.data.make_data


class PlugSink(paf.sink_base.Sink):
    """ Automatically added on every output of every element to dynamically
    connect viewer or pipeline.
    """
    class DataSender(QObject):
        """ class to send data.
        """
        #: signal for received new data
        receive_data = pyqtSignal(paf.data.Data)

        def __init__(self):
            """ initialization
            """
            QObject.__init__(self)

        def connect_to_signal(self, slot):
            """ connect a slot to the signal.
            """
            self.receive_data.connect(slot)

        def disconnect(self, slot=None):
            """ disconnect a connected slot to the signal
            """
            try:
                if slot is None:
                    self.receive_data.disconnect()
                else:
                    self.receive_data.disconnect(slot)
            except TypeError:
                pass

        def emit(self, data):
            """ emit signal
            """
            self.receive_data.emit(data)

    def __init__(self, data_type):
        """ initialization

        :param data_type: data type of input port
        """
        paf.sink_base.Sink.__init__(self, data_type)
        #: event sender using Qt
        self.data_sender = self.DataSender()

    @synchronized
    def get_data(self):
        """ getter to data

        :param data_type: say if the expected value must be a type.
        :type data_type: boolean
        :return: the last data input
        """
        return paf.sink_base.Sink.get_data(self, 'main')

    def connect_to_signal(self, slot):
        """ connect slot to receive data signal

        :param slot: slot to connect.
        :type slot: callable
        """
        self.data_sender.connect_to_signal(slot)

    def disconnect(self, slot=None):
        """ disconnect a slot from a signal
        """
        self.data_sender.disconnect(slot)

    def run(self):
        """ emit signal with data
        """
        self.data_sender.emit(self.get_data())


class TemporaryData(paf.data.CompositeData):
    """ composite data of temporary data
    """
    def __init__(self):
        """ initialization
        """
        paf.data.CompositeData.__init__(self, {})

    def __setitem__(self, key, data):
        """ new set item to automated copy data and create key.
        """
        data = paf.data.copy_data(data)
        self._value[key] = data


class EvolutionReport(paf.data.CompositeData):
    """ report for one evolution
    """
    def __init__(self):
        value = {"source": "", "FOM": 0., "param": "", "corr": np.array([[]]),
                 "simulations": TemporaryData(), "FOMS": [],
                 "corr_header": []}
        paf.data.CompositeData.__init__(self, value, "evolution_report")


class Result(paf.data.CompositeData):
    """ a result from one operation
    """

    def __init__(self):
        """ initialization
        """
        value = {"data": paf.data.CompositeData(), "start": time.time(),
                 "name": "", "operation": "",  "end": 0., "foms": None}
        paf.data.CompositeData.__init__(self, value, abstract='results')

    @property
    def name(self):
        """ get the name
        """
        return self["name"].value

    @name.setter
    def name(self, value):
        """ setter for name
        """
        self.real_value["name"] = MAKE_DATA(value)

    @property
    def operation(self):
        """ get the name
        """
        return self["operation"].value

    @operation.setter
    def operation(self, value):
        """ setter for name
        """
        self["operation"] = value

    @property
    def foms(self):
        """ get list of all FOM names
        """
        return self["foms"].value

    @foms.setter
    def foms(self, value):
        """ setter for fom list
        """
        self["foms"] = value

    def add_recordable(self, name):
        """ add recordable
        """
        self["data"].real_value[name] = MAKE_DATA([])

    def create_record_slot(self, name):
        """ create a slot for recording a data
        """
        def recording(data):
            """ slot for recording a data
            """
            self["data"][name].append(data)
        return recording


class Pipeline(QObject):
    """ Modeling a Pipeline.
    """
    # added signal

    #: element stopping
    element_ending = pyqtSignal(paf.element.Element)

    #: element running
    element_running = pyqtSignal(paf.element.Element)

    #: change state
    change_state = pyqtSignal(QObject)

    #: error detect
    error_detected = pyqtSignal(str, str)

    #: evolution report
    evolution_report = pyqtSignal(EvolutionReport)

    def __init__(self, state_saving=True):
        """ initialization: create all included element. The filter his add to
        pump list and sink list
        """
        QObject.__init__(self)
        #: list of all connection (tuple of sink and pump for key and pipe for
        #: value
        self._connection = {}
        #: list of all pump are not filter
        self._pump_only = {}
        #: list of entity_pump
        self._entity_pump = {}
        #: list of all element
        self._elements = {}
        #: list of plug sink
        self._plug_sink = {}
        #: list of recordable element
        self._recordable = {}
        #: list of modifiable element
        self._modifiable = {}
        #: temporary data
        self._temporary_data = TemporaryData()
        #: if it's started
        self._started = False
        #: stoking result of current or last execution
        self._result = None
        #: save result slot to disconnect after use
        self._result_slot = None

        #: essential parameter
        self._essential = pyxcel.engine.database.CompositeMultiEditor()
        #: save essential parameter conjig
        self._essential_config = {}

        # for recording state
        #: number of element running
        self._nb_finish = 0
        if state_saving:
            self.element_ending.connect(self.end_element)
        #: self clear infinity reisque
        self.clear_inf = [None]
        #: number of data accepted *None is infity*
        self._nb_data_max = 0

        # connect event
        self.change_state.connect(self._endding)

    @property
    def result(self):
        """ return result of current or last execution
        """
        return self._result

    @property
    def essential_config(self):
        """ accessing to essential config
        """
        return self._essential_config

    @property
    def connection(self):
        """ access to connection
        """
        return self._connection

    @property
    def nb_data_max(self):
        """ return number of data expected *None is infinity*
        """
        return self._nb_data_max

    @nb_data_max.setter
    def nb_data_max(self, value):
        """ set number of data max
        """
        self._nb_data_max = value

    @property
    def essential(self):
        """ accessing to essential parameter
        """
        return self._essential

    @property
    def temporary_data(self):
        """ access to temporary data
        """
        return self._temporary_data

    @temporary_data.setter
    def temporary_data(self, value):
        """ change temporary data object
        """
        self._temporary_data = value
        for element in self.elements:
            try:
                element = self.get_element(element)
                element["temporary_data"] = self.temporary_data
            except KeyError:
                pass
            except TypeError:
                pass

    @property
    def entity_pump(self):
        """ list of entity pump
        """
        return self._entity_pump

    @property
    def all_finish(self):
        """ return True if all element is finish
        """
        finished_list = [element.is_finish
                         for _, element in self._elements.items()]
        return all(finished_list)

    @property
    def running(self):
        """ property for knowing if the pipeline is running or not.
        """
        return not self.all_finish and self._started

    @property
    def recordable(self):
        """ property for the list of recordable element.
        """
        return self._recordable

    @property
    def modifiable(self):
        """ property for accessing to modifiable element.
        """
        return self._modifiable

    @property
    def param_value(self):
        """ transform all parameter of each element to a single composite data
        """
        all_parameter = {}
        for name, elements in self.elements.items():
            new_param = elements.composite_value
            if new_param is not None:
                if "temporary_data" in new_param.keys():
                    del new_param.real_value["temporary_data"]
            all_parameter[name] = new_param
        return MAKE_DATA(all_parameter, composite=True)

    @param_value.setter
    def param_value(self, value):
        """ set a value to all param from a single composite data
        """
        self.recreate_pipeline(value)
        for name, params in value.items():
            self._elements[name].composite_value = params

    @property
    def elements(self):
        """ property for accessing to elements dictionary.
        """
        return self._elements

    @property
    def plug_sink_list(self):
        """ property to get the list of all name of plug sink

        :return: list of names of all the plug sink
        :rtype: list(str)
        """
        return list(self._plug_sink.keys())

    def recreate_pipeline(self, element_config):
        """ recreate all pipeline dynamic parts
        """
        pass

    def add_data(self, name, *args, **kwargs):
        """ add new data

        :return: new pump name
        :rtype: str
        """
        logging.info("Adding %s in pipeline", name)

    def delete_data(self, pump_name):
        """ delete pump and pipeline part linked to a data

        :param pump_name: name of pump to delete
        :type pump_name: str
        """
        logging.info("Deleting %s in pipeline", pump_name)

    def add_to_essential(self, element, parameter, showing_info="",
                         new_value=None):
        """ add parameter to essential
        """
        self._essential.add_element(self._elements[element].
                                    to_composite_data(), parameter,
                                    showing_info, new_value)
        if new_value is None:
            new_value = parameter
        self._essential_config[new_value] = [showing_info,
                                             (element, parameter)]

    def add_essential_connexion(self, key, element, old_value):
        """ add a new connection to a data with essential parameter
        """
        self._essential.add_connexion(key, self._elements[element].
                                      to_composite_data(), old_value)
        self._essential_config[key].append((element, old_value))

    def reinit_essential(self):
        """ reinit essential parameter
        """
        self._essential = pyxcel.engine.database.CompositeMultiEditor()
        for key, value in self._essential_config.items():
            showing_info = value.pop(0)
            element, parameter = value.pop(0)
            self.add_to_essential(element, parameter, showing_info, key)
            nb_value = len(value)
            for _ in range(nb_value):
                element, old_value = value.pop()
                self.add_essential_connexion(key, element, old_value)

    def end_element(self, element):
        """ connect signal for editing state when he is notify.
        """
        if element.is_finish:
            self._nb_finish += 1
            self.change_state.emit(self)

    def add_notifier(self, element, name):
        """ modify the element function to add notification using QSignal

        :param element: element to add notifier.
        :type element: paf.element.Element
        :param name: name to notifier
        :type name: str
        """
        def signal_running(run):
            """ create a function notifying when the element start and when
            it's stop

            :param run: run function.
            """
            def new_run():
                """ new runner
                """
                self.element_running.emit(element)
                # try:
                run()
#                 except Exception as error:
#                     self.error_detected.emit(str(error.__class__.__name__),
#                                              str(error))
#                 self.element_ending.emit(element)
            return new_run

        element.run = signal_running(element.run)

    def create_report_slot(self, name):
        """ create slot for reporting signal
        """
        def report_slot(evolution_report):
            """ slot for reporting signal
            """
            evolution_report["source"] = name
            self.evolution_report.emit(evolution_report)
        return report_slot

    def add_element(self, name, element, saveable_output=[], modifiable=False):
        """ add in list a new element.

        :param name: name of new pump to add.
        :type name: str
        :param element: element to add
        :type element: paf.element.Element
        """
        if isinstance(element, paf.element.Element):
            try:
                element["temporary_data"] = self.temporary_data
            except KeyError:
                pass
            except TypeError:
                pass
            try:
                element.report_notifier.signal.connect(self.create_report_slot
                                                       (name))
            except AttributeError:
                pass
            name = uni(name)
            self.add_notifier(element, name)
            self._elements[name] = element
            if modifiable:
                self._modifiable[name] = element

            # add sink for each output port
            if isinstance(element, paf.pump_base.PumpInterface):
                list_output = element.output_port.keys()
                for output_port_name in list_output:
                    port = element.output_port[output_port_name]
                    new_sink = PlugSink(port.data_type)
                    self._plug_sink[name + "_" + output_port_name] = new_sink
                    paf.pipe.connect(element, new_sink, output_port_name)
                    if output_port_name in saveable_output:
                        self._recordable[name + "_" +
                                         output_port_name] = new_sink

                # add to pump to automated starting
                if isinstance(element, paf.pump_base.Pump):
                    self._pump_only[name] = element
                    if isinstance(element, pyxcel.engine.modeling.pumps.
                                  EntityPump):
                        self._entity_pump[name] = element
        else:
            raise TypeError("you can only add element (paf.element.Element).")

    def get_element(self, name):
        """ get the pump by is name in the Pipeline.

        :return: the pump
        :rtype: paf.pump_base.Pump
        """
        return self._elements[name]

    def del_element(self, name):
        """ delete a pump.

        :param name: name of the pump must be delete.
        :type name: str
        """
        if isinstance(self._elements[name], paf.pump_base.PumpInterface):
            element = self._elements[name]
            for output_port_name in element.output_port.keys():
                del self._plug_sink[name + "_" + output_port_name]
            if isinstance(self._elements[name], paf.pump_base.Pump):
                del self._pump_only[name]
            if isinstance(self._elements[name],
                          pyxcel.engine.modeling.pumps.EntityPump):
                del self._entity_pump[name]
            if name in list(self._modifiable.keys()):
                del self._modifiable[name]
        del self._elements[name]

    def connect(self, pump_name, sink_name, pump_port="main", sink_port="main"
                ):
        """ Connect one pump and one sink using there name in the Pipeline.

        :param pump_name: name of the pump in the Pipeline.
        :type pump_name: str
        :param sink_name: name of the sink in the Pipeline.
        :type sink_name: str
        :param pump_port: name of the port on the pump.
        :type pump_port: str
        :param sink_port: name of the port on the sink.
        :type sink_port: str
        """
        self._connection[(pump_name, sink_name)] =\
            paf.pipe.connect(self._elements[pump_name],
                             self._elements[sink_name], pump_port, sink_port)

    def disconnect(self, pump_name, sink_name, pump_port="main",
                   sink_port="main"):
        """ Connect one pump and one sink using there name in the Pipeline.

        :param pump_name: name of the pump in the Pipeline.
        :type pump_name: str
        :param sink_name: name of the sink in the Pipeline.
        :type sink_name: str
        :param pump_port: name of the port on the pump.
        :type pump_port: str
        :param sink_port: name of the port on the sink.
        :type sink_port: str
        """
        self._connection[(pump_name, sink_name)] =\
            paf.pipe.connect(self._elements[pump_name],
                             self._elements[sink_name], pump_port, sink_port)

    def clear_result_connection(self):
        """ clear all slot connection for result
        """
        for (name, value) in self.recordable.items():
            if self._result_slot is not None:
                value.disconnect(self._result_slot[name])

    def start(self):
        """ start all pumps
        """
        # reconfigure is finish to False for all element
        self._started = True
        self._nb_finish = 0
        for (_, element) in self._elements.items():
            element.is_finish = False

        # create object to store result data
        self._result = Result()
        try:
            self._result.foms = self.foms
        except AttributeError:
            pass
        self.clear_result_connection()
        self._result_slot = {}
        for (name, value) in self.recordable.items():
            self._result.add_recordable(name)
            self._result_slot[name] = self._result.create_record_slot(name)
            value.connect_to_signal(self._result_slot[name])

        # start operation
        for (_, pump) in self._pump_only.items():
            pump.start()
        self.change_state.emit(self)
        logging.info("start pipeline")

    def _endding(self):
        """ call when the operation is fully endded
        """
        if self.all_finish and self._started:
            self._started = False

            # save endding time in result
            self._result["end"] = time.time()

            # empty pipe
            for _, pipe in self._connection.items():
                pipe.clear()

#             print("Operation finished")
            self.change_state.emit(self)

    def reinit(self):
        """ initialize the Pipeline again. *recreate the thread on every pump*
        """
        # stop filling port
        for _, element in self._elements.items():
            element.stop()
            self.element_ending.emit(element)
        logging.info("reinit pipeline")
