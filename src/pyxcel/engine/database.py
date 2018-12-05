# -*- coding: utf8 -*-
"""
Module for representing a database of the software.

    :platform: Unix, Windows
    :synopsis: Module for define a Pipeline.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import logging
import paf.data
import paf.filter_base
import pyxcel.engine.modeling.entity as entity
import pyxcel.engine.pipeline
import pyxcel.engine.centralizer
from pyxcel.view.cute import QObject, pyqtSignal, QApplication
from pyxcel.uni import uni
MAKE_DATA = paf.data.make_data

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig=None):
        return QApplication.translate(context, text, disambig)


class CompositeMultiEditor(paf.data.CompositeData):
    """ composite object build to change other part of other composite
    """
    def __init__(self, abstract="multi_editor"):
        """ initialization
        """
        paf.data.CompositeData.__init__(self, {}, abstract)
        self._connexion = {}

    def add_element(self, composite_ref, old_value, showing_info="",
                    new_value=None):
        """ add new element to edit
        """
        if new_value is None:
            new_value = old_value
        if showing_info == "":
            showing_info = new_value
        if showing_info is not None:
            self._showing_info.append((new_value, showing_info))
        self._value[new_value] = composite_ref[old_value]
        self._connexion[new_value] = [(old_value, composite_ref)]

    def add_connexion(self, key, composite_ref, old_value=None):
        """ add a new connexion to a data
        """
        if old_value is None:
            old_value = key
        self._connexion[key].append((old_value, composite_ref))

    def __setitem__(self, key, value):
        """ modify the value of one element and the corresponding reference.

        :param key: name of the element to return
        :type key: str
        :param value: new value of the element.
        """
        paf.data.CompositeData.__setitem__(self, key, value)
        olds = self._connexion[key]
        for old in olds:
            old[1][old[0]] = value

    def __delitem__(self, key):
        """ delete an item
        """
        del self._connexion[key]
        del self._value[key]
        index = [value for value, _ in self.showing_info].index(key)
        del self._showing_info[index]


class PhysicalInstrumentFilter(paf.filter_base.Filter):
    """ filter to extract the default value of an instrument.
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self, PhysicalInstrument(),
                                        entity.InstrumentData())

    def run(self):
        """ running filter
        """
        physical_instrument = self.get_data("main")
        self.fill_port("main", physical_instrument['default_value'])


def modifiing_function(function):
    """ decorator for function to emit self.data_modified signal.
    """
    def new_function(self, *args, **kw):
        """ new function
        """
        function(self, *args, **kw)
        self.data_modified.signal.emit()
    return new_function


class CompositeDataObservable(paf.data.CompositeData):
    """ Composite data using Qt signal to notify connected slot.
    """

    class DataModifiedNotifier(QObject):
        """ notifier object
        """
        #: notifier signal
        _signal = pyqtSignal()

        @property
        def signal(self):
            """ property for accessing signal
            """
            return self._signal

    #: event sender using Qt
    data_modified = DataModifiedNotifier()

    def __init__(self, composite_data):
        """ initialization
        """
        paf.data.CompositeData.__init__(self)
        self._abstract_data_type = composite_data.abstract_type
        self._composite_data = composite_data
        self.connect_to_signal(self.auto_refresh)

        # observe child
        for key, item in composite_data.items():
            if isinstance(item, paf.data.CompositeData):
                self._value[key] = CompositeDataObservable(item)
            elif isinstance(item, paf.data.ListData):
                self._value[key] = ListDataObservable(item)
            else:
                self._value[key] = item
        try:
            self._showing_info = composite_data.showing_info
        except:
            pass

    @property
    def composite_data(self):
        """ return composite data
        """
        return self._composite_data

    def auto_refresh(self):
        for key, item in self._composite_data.items():
            if isinstance(item, paf.data.CompositeData):
                self._value[key] = CompositeDataObservable(item)
            else:
                self._value[key] = item

    def connect_to_signal(self, slot):
        """ connect to the data modified signal.
        """
        self.data_modified.signal.connect(slot)

    def disconnect_to_signal(self, slot):
        """ disconnect to the data modified signal.
        """
        self.data_modified.signal.disconnect(slot)

    @modifiing_function
    def emit_modify(self):
        """ emit modify signal
        """
        pass

    @modifiing_function
    def __setitem__(self, key, value):
        """ emit the data modified signal on each component data.
        """
        paf.data.CompositeData.__setitem__(self, key, value)
        if isinstance(value, CompositeDataObservable):
            self._composite_data[key] = value.composite_data
        else:
            self._composite_data[key] = value


class ListDataObservable(paf.data.ListData):
    """ observable version of list data
    """

    def __init__(self, list_data=None, abstract=""):
        """ initialization
        """
        paf.data.ListData.__init__(self)
        if list_data is not None:
            self._abstract_data_type = list_data.abstract_type
            self._list_data = list_data
            # observe child
            for item in self._list_data:
                if isinstance(item, paf.data.CompositeData):
                    self._value.append(CompositeDataObservable(item))
                elif isinstance(item, paf.data.ListData):
                    self._value.append(ListDataObservable(item))
                else:
                    self._value.append(item)
        self.data_modified = CompositeDataObservable.data_modified
        self.connect_to_signal(self.auto_refresh)

    @modifiing_function
    def clear(self):
        paf.data.ListData.clear(self)
        self.list_data.clear()

    def auto_refresh(self):
        for key, item in enumerate(self._list_data):
            if isinstance(item, paf.data.CompositeData):
                self._value[key] = CompositeDataObservable(item)
            else:
                self._value[key] = item

    @property
    def list_data(self):
        return self._list_data

    def connect_to_signal(self, slot):
        """ connect to the data modified signal.
        """
        self.data_modified.signal.connect(slot)

    def disconnect_to_signal(self, slot):
        """ disconnect to the data modified signal.
        """
        self.data_modified.signal.disconnect(slot)

    @modifiing_function
    def emit_modify(self):
        """ emit modify signal
        """
        pass

    @modifiing_function
    def __delitem__(self, key):
        paf.data.ListData.__delitem__(self, key)
        self.list_data.__delitem__(key)

    @modifiing_function
    def __setitem__(self, key, value):
        """ emit the data modified signal on each component data.
        """
        self._original_setitem(key, value)

    @modifiing_function
    def append(self, value):
        """ append a new value in the list

        :param value: new value to add in the list.
        :type value: Data
        """
        paf.data.ListData.append(self, value)
        self.list_data.append(value)


class Operation(paf.data.CompositeData):
    """ correspond to one operations file in database
    """

    def __init__(self, name=None, database=None):
        """ initialization
        """
        self._last_instance = None
        self._option = pyxcel.engine.centralizer.Centralizer().option
        is_default = name in self._option.default_operation.keys()
        value = {"name": name, "result": [], "is_default": is_default}
        paf.data.CompositeData.__init__(self, value, abstract="operations")

    def create_instance(self):
        """ execute operations file to create a new pipeline.
        """
        name = self["name"].value
        main_win = pyxcel.engine.centralizer.Centralizer().main_window
        if self["is_default"].value:
            self.last_instance = self._option.default_operation[name]()
        else:
            tmp_dict = {}
            with open(name, "r") as pipeline_file:
                exec(pipeline_file.read(), tmp_dict)
            for var_name in list(tmp_dict.keys()):
                if isinstance(tmp_dict[var_name],
                              pyxcel.engine.pipeline.Pipeline):
                    self.last_instance = tmp_dict[var_name]
        self.last_instance.change_state.connect(main_win.update_state)
        self.last_instance.error_detected.connect(main_win.error_detected)

    @property
    def last_instance(self):
        """ property to access of the last created operations
        """
        return self._last_instance

    @last_instance.setter
    def last_instance(self, value):
        """ set last instance new value
        """
        self._last_instance = value


class PhysicalInstrument(paf.data.CompositeData):
    """ describe a physical instrument and include all data about it.
    """

    def __init__(self, source_type=entity.XRaySourceData,
                 detector_type=entity.XRRDetectorData, type_instrument="XRR"):
        """ initialization
        """
        self._detector_type = detector_type
        self._source_type = source_type
        self._type_instrument = type_instrument
        instrument = entity.InstrumentData(source_type(), detector_type(),
                                           type_instrument)
        self._current_parameter = instrument
        value = {"default_value": instrument, "current_parameter": instrument}
        paf.data.CompositeData.__init__(self, value, "physical_instrument")

    @property
    def type_instrument(self):
        """ property to access to instrument type
        """
        return self._type_instrument


class PhysicalSample(paf.data.CompositeData):
    """ describe a physical sample and include all data about it.
    """

    def __init__(self, name=""):
        """ initialization
        """
        value = {"name": name, "models": [], "data": [], "results": []}
        paf.data.CompositeData.__init__(self, value, "physical_sample")

    def add_model(self, name):
        """ add new model in model list
        """
        self["models"].append(MAKE_DATA(name))

    def add_data(self, name):
        """ add new data in data list
        """
        self["data"].append(MAKE_DATA(name))

    def remove_model(self, name):
        """ remove a model from model list
        """
        for index, model in enumerate(self["models"].value):
            if model == name:
                del self["models"][index]

    def remove_data(self, name):
        """ remove a data from data list
        """
        for index, data in enumerate(self["data"].value):
            if data == name:
                del self["data"][index]


class ExperimentalData(paf.data.CompositeData):
    """ represent experimental data in database
    """

    def __init__(self, file_name="", Instrument_name="", two_tetha=True):
        #TODO: ajouté paramétre dans valeur
        value = {"file_name": file_name, "Instrument_name": Instrument_name,
                 "2_Theta": two_tetha}
        paf.data.CompositeData.__init__(self, value, "experimental_data")
        self.showing_info = [("file_name", "File name"),
                             ("Instrument_name", "Sample name"),
                             ("2_Theta", "2 theta scale")]


class TreeElement(paf.data.CompositeData):
    """ modeling a tree element.
    """

    def __init__(self, name="", parent=None):
        """ initialization

        :param name: name of the tree element
        :type name: str
        :param parent: parent of the tree element
        :type parent: TreeElement
        """
        self._children = []
        value = {"name": name, "children": self._children, "expended": True}
        paf.data.CompositeData.__init__(self, value, 'tree_element')
        self._parent = parent
        if parent is not None:
            parent.append_child(self)

    def __delitem__(self, item_name):
        """ delete children
        """
        item = self.find_by_name(item_name)
        item.parent = None

    @property
    def parent(self):
        """ property to access to parent
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """ setter for parent property
        """
        if self._parent is not None:
            self._parent["children"]._value.remove(self)
            self._parent._children.remove(self)
        if parent is not None:
            self._parent = parent
            self._parent["children"]._value.append(self)
            self._parent._children.append(self)

    def append_child(self, child):
        """ method to append a new child
        """
        self._children.append(child)
        self["children"].append(child)

    def set_from_xml(self, xml_element):
        """ set value from an xml file
        """
        paf.data.CompositeData.set_from_xml(self, xml_element)
        for child in self._value["children"]:
            child._parent = self
            self._children.append(child)

    def find_by_name(self, name):
        """ find a child by is name.
        """
        if self['name'].value == uni(name):
            return self
        elif len(self._children) > 0:
            for child in self._children:
                child_return = child.find_by_name(name)
                if child_return is not None:
                    return child_return
        else:
            return None


class Database(CompositeDataObservable):
    """ composite data for representing database.
    """

    class InstanceOpNotifier(QObject):
        _modified_data = pyqtSignal(str)

        def connect(self, slot):
            self._modified_data.connect(slot)

        def emit(self, name):
            self._modified_data.emit(name)

    #: event sender using Qt
    data_modified = CompositeDataObservable.DataModifiedNotifier()

    #: event sender using Qt
    instance_op_notif = InstanceOpNotifier()

    @modifiing_function
    def emit_modify(self):
        """ emit modify signal
        """
        pass

    def __init__(self):
        """ initialization
        """
        self._root = TreeElement('root', None)
        self._instrument_root = TreeElement('instrument_root', self._root)
        self._sample_root = TreeElement('sample_root', self._root)
        self._op_root = TreeElement('op_root', self._root)
        value = {}
        self._op = {}
        self._op_parent = paf.data.CompositeData({})
        paf.data.CompositeData.__init__(self, value, 'database')
        self._value['tree'] = self._root
        self._value['op_parent'] = self._op_parent

    def __delitem__(self, item_name):
        """ delete an item from database.
        """
        if item_name in self._value.keys():
            if isinstance(self._value[item_name], entity.StackData):
                sample_e = (self._sample_root.find_by_name(item_name).parent.
                            parent)
                sample = self[sample_e["name"]]
                sample.remove_model(item_name)
            elif isinstance(self._value[item_name], ExperimentalData):
                sample_e = (self._sample_root.find_by_name(item_name).parent.
                            parent)
                sample = self[sample_e["name"]]
                sample.remove_data(item_name)
            del self._value[item_name]
        elif item_name in self._op.keys():
            del self._op[item_name]

    @property
    def operations(self):
        """ return list of name of opened pipeline
        """
        return list(self._op.keys())

    def get_operation(self, name):
        """ get operations by name
        """
        return self._op[name]

    @property
    def operations_launched(self):
        """ return list of name of operations launched
        """
        return [key for (key, op) in self._op.items() if op[1]]

    def add_entity(self, name, entity, parent=None):
        """ add a new entity in the database.
        """
        try:
            value = self._value[name]
        except KeyError:
            value = None
        if value is not None:
            raise KeyError("The name: " + name + " is already taken!")
        if parent is not None:
            TreeElement(name, parent)
        self._value[name] = entity
        self.emit_modify()

    def memorize_operation(self, name, entity, parent):
        """ add a new entity in the database.
        """
        if name in list(self._op.keys()):
            raise KeyError("The name: " + name + " is already taken!")
        self._op[name] = [entity, False]
        if name not in self._op_parent.keys():
            TreeElement(name, parent)
            self._op_parent.real_value[name] = parent["name"]
        self.emit_modify()

    @modifiing_function
    def create_instrument(self, name, source_type, detector_type,
                          type_instrument):
        """ create a new instrument in database.
        """
        physical_instrument = PhysicalInstrument(source_type, detector_type,
                                                 type_instrument)
        physical_instrument["default_value"]["name"] = name
        self.add_entity(name, physical_instrument, self._instrument_root)

    @modifiing_function
    def create_sample(self, name):
        """ create a new sample in database.
        """
        physical_sample = PhysicalSample(name)
        self.add_entity(name, physical_sample, self._sample_root)
        models_name = uni("Model")
        data_name = uni("Data")
        tree_element = self._root.find_by_name(name)
        TreeElement(models_name, tree_element)
        TreeElement(data_name, tree_element)

    @modifiing_function
    def create_model(self, sample_name, name):
        """ create a new model for an existent sample in database.
        """
        full_name = sample_name + '_' + name
        amb = entity.LayerData("N2", "ambiant")
        amb["mass_density"] = 0.0012
        sub = entity.LayerData("", "substrate")
        layers = MAKE_DATA([entity.LayerData()])
        new_stak = entity.StackData(full_name, amb, sub, layers)
        tree_element = self._root.find_by_name(sample_name)["children"][0]
        self.add_entity(full_name, new_stak, tree_element)
        self[sample_name].add_model(full_name)

    def copy_model(self, source_name, sample_name, name):
        """ create copy of a model
        """
        source = self[source_name]
        full_name = sample_name + '_' + name
        new_stak = paf.data.copy_data(source)
        new_stak["name"] = full_name
        tree_element = self._root.find_by_name(sample_name)["children"][0]
        self[sample_name].add_model(full_name)
        self.add_entity(full_name, new_stak, tree_element)

    def create_layer(self, stack_name, name):
        """ create a new layer in an existent model in database.
        """
        stack = self[stack_name]
        new_layer = entity.LayerData(name=name)
        stack.real_value["layers"].append(new_layer)

    def add_exp_data(self, file_name, instrument_name, sample_name):
        """ add experimental data in database.
        """
        xrf = False
        instrument = self[instrument_name]['default_value']
        if instrument.abstract_type == "XRFInstrument":
            xrf = True
        if xrf:
            new_data = ExperimentalData(file_name, instrument_name, False)
        else:
            new_data = ExperimentalData(file_name, instrument_name, True)
        self.add_entity(file_name, new_data,
                        self._root.find_by_name(sample_name)["children"][1])
        self[sample_name].add_data(file_name)

    def create_op_instance(self, op_name, name_new_op):
        """ execute a new operations file and create an instance of a pipeline.
        """
        test = False
        try:
            self._value[name_new_op]
            test = True
        except KeyError:
            pass
        if test:
            raise AttributeError()
        op_file = self._value[op_name]
        op_file.create_instance()
        self.memorize_operation(name_new_op, op_file.last_instance,
                                self._root.find_by_name(op_name))
        self.emit_modify()

    def add_operation(self, file_name):
        """ add a new operations file in database.
        """
        new_operation_file = Operation(file_name, self)
        self.add_entity(file_name, new_operation_file,
                        self._root["children"][2])
        self._root.find_by_name(file_name)
        self.emit_modify()

    def launch_op(self, name):
        """ launch an opening operations
        """
        if not self._op[name][1]:
            self._op[name][0].reinit()
            self._op[name][0].start()
            self._op[name][1] = True
            self.emit_modify()
            self.instance_op_notif.emit(name)
            logging.info("Operation launched : %s", name)

    def end_op(self, name):
        """ slot for end element of an operations
        """
        self._op[name][1] = False
        self._op[name][0].reinit()

    def add_result(self, data, operation_name):
        """ add result of an operations
        """
        result_name = operation_name + "_" + data.name
        data.operation = operation_name
        operation_element = self._root.find_by_name(operation_name)
        self.add_entity(result_name, data, operation_element)

    def set_from_xml(self, xml_element):
        """ load from an XML file
        """
        CompositeDataObservable.set_from_xml(self, xml_element)
        self._root = self._value['tree']
        self._instrument_root = self._root["children"][0]
        self._sample_root = self._root["children"][1]
        self._op_root = self._root["children"][2]
        self._op_parent = self["op_parent"]

    def to_xml(self, xml_doc, xml_parrent, name):
        """ save to xml
        """
        item_op = self._op.items()
        params = {name_op: op[0].param_value for name_op, op in item_op}
        temps = {name_op: op[0].temporary_data for name_op, op in item_op}
        self._value['param_op'] = MAKE_DATA(params, composite=True)
        self._value['tep_data_op'] = MAKE_DATA(temps, composite=True)
        paf.data.CompositeData.to_xml(self, xml_doc, xml_parrent, name)

    def get_type(self, data):
        """ get type (XRR, XRF, ...) from named element

        :param name: name of data or data (instrument or experimental data)
        :rtype: string
        :return: XRR or XRF
        """
        if not isinstance(data, paf.data.CompositeData):
            try:
                data = self._value[data]
            except KeyError:
                return ""
        if isinstance(data, ExperimentalData):
            data = self._value[data["Instrument_name"].value]
        return data["default_value"].abstract_type[:-10]

    def reactivate(self, op_name):
        """ reactivate an operation

        :param op_name: name of operation to reactivate
        type op_name: str
        """
        if (op_name in self._op_parent.keys() and
                op_name not in self._op.keys()):
            operation_type = self._op_parent[op_name].value
            self.create_op_instance(operation_type, op_name)
            op = self._op[op_name][0]
            op.temporary_data = self._value['tep_data_op'][op_name]
            op.param_value = self._value['param_op'][op_name]
            op.reinit_essential()
