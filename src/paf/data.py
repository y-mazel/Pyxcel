# -*- coding: utf8 -*-
"""
Defining data type use to circulate in pipe and to configurate pipeline
element. It also contain IO utilities like data format.

    :platform: Unix, Windows
    :synopsis: Module to define data.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import sys
import numpy as np
import codecs
from xml.dom import minidom
from abc import ABCMeta, abstractmethod
import quantities as pq
import quantities.quantity
if sys.version_info[0] >= 3:
    unicode = str

# tryout
import string
import re


def characterRepl(matchObj):
    """ Ad hoc function to replace \n and \t with &#10; and &#x9; in the #Parameter fields of the xml database (otherwise minidom replaces them with a whitespace)
    """
    match = matchObj.group(0)
    match = match.replace('\n','&#10;')
    match = match.replace('\t','&#x9;')
    return match

class Data(object):
    """ Class for transport and type data into a Pipe
    """
    __metaclass__ = ABCMeta

    #: compatibility map of abstract type.
    abstract_Type_compatibility = {}

    def __init__(self, value, abstract=''):
        """ initialization of value and abstract type.

        :param value: value of data contain
        :param abstract: name of the abstract type.
        :type abstract: str
        """
        #: data contain in the Data object
        self._value = value
        #: abstract type of the data
        self._abstract_data_type = abstract
        #: type of the data
        self._data_type = type(value)

    def __len__(self):
        """ return length of the value

        :return: length of the value
        :rtype: int
        """
        return len(self._value)

    @property
    def real_value(self):
        """getter for the content of _value

        :returns: value in correct unit
        """
        return self._value

    @real_value.setter
    def real_value(self, new_value):
        """ set new value for self._value

        :param new_value: new value for data
        """
        self._value = new_value

    @property
    def data_type(self):
        """ property getter for concrete data type

        :returns: data type
        """
        return self._data_type

    @property
    def value(self):
        """ property getter for the value

        :returns: value in correct unit
        """
        return self._value

    @value.setter
    def value(self, value):
        """ property setter for the value.

        :param value: new value
        """
        self._value = value

    @property
    def abstract_type(self):
        """ property for the abstract type of the data.

        :return: name of the abstract type.
        :rtype: str
        """
        return self._abstract_data_type

    @abstract_type.setter
    def abstract_type(self, value):
        """ setter for the abstract type of the data.

        :param value: new value
        :type value: str
        """
        self._abstract_data_type = value

    @abstractmethod
    def to_xml(self, xml_doc, xml_parrent, name):
        """ add a new Data object in an XML document.

        :param xml_doc: document xml for adding data
        :type xml_doc: XMLDocument
        :param xml_parrent: parent XML element data
        :param name: of the adding data
        :type name: str
        """
        type_name = self.__class__.__module__ + '.' + self.__class__.__name__
        module_name = self.__class__.__module__
        new_element = xml_doc.createElement(type_name)
        new_element.attributes['name'] = name
        new_element.attributes['module_name'] = module_name
        new_element.attributes['abstract'] = self.abstract_type
        return new_element

    @abstractmethod
    def set_from_xml(self, xml_element):
        """ change value extracting data from an xml element.

        :param xml_element: xml element to extract data.
        """

    @staticmethod
    def add_abstract_compatibility(name_type1, name_type2):
        """ Static method to make type1 compatible with type2

        :param name_type1: name of the abstract type 1.
        :type name_type1: str
        :param name_type2: name of the abstract type 1.
        :type name_type2: str
        """
        try:
            Data.abstract_Type_compatibility[name_type1].append(name_type2)
        except KeyError:
            Data.abstract_Type_compatibility[name_type1] = [name_type2]

    @staticmethod
    def is_abstract_compatible(name_type1, name_type2):
        """ Verify if abstract type 1 is compatible to abstract type 2. If type
        1 is not define, it is compatible with type 2 only if type 2 is not
        define too.

        :param name_type1: name of the abstract type 1.
        :type name_type1: str
        :param name_type2: name of the abstract type 2.
        :type name_type2: str
        :return: true if is compatible. If type1 is not in base : return true
        :rtype: boolean
        """
        # if the abstract type are the same
        if name_type1 == name_type2:
            return True

        # if the abstract type 1 is define
        if name_type1 in list(Data.abstract_Type_compatibility.keys()):
            if name_type2 in Data.abstract_Type_compatibility[name_type1]:
                return True
            else:
                return False
        # if the abstract type 1 is not define
        else:
            if name_type2 in list(Data.abstract_Type_compatibility.keys()):
                return False
            else:
                return True

    def is_compatible(self, data):
        """ Test if data is compatible in concrete type and in *abstract type (
        not implemented)* to another data.

        :param data: other data to determine if it is compatible.
        :type data: Data
        :return: true if data is compatible to self.
        :rtype: boolean
        """
        # check if data is instance of Data
        if not isinstance(data, type(self)):
            return False

        if((self._data_type != data.data_type) and
           (self._data_type is not None) and
           (data.data_type is not None)):
            return False

        # check abstract data is compatible
        if not Data.is_abstract_compatible(self.abstract_type,
                                           data.abstract_type):
            return False
        return True

    def finish_copy(self):
        """ method call at the end of a copy on destination to terminate
        """
        pass


class SimpleData(Data):
    """ implementing a simple data.
    """
    def __init__(self, value=None, abstract=''):
        """ initialization of value and abstract type.

        :param value: value of data contain
        :param abstract: name of the abstract type.
        :type abstract: str
        """
        if value is None:
            new_value = 0
        else:
            new_value = value
        Data.__init__(self, new_value, abstract)
        if value is None:
            self._data_type = None

    def __str__(self):
        """ return string representation
        """
        return str(self._value)

    def to_xml(self, xml_doc, xml_parrent, name):
        """ add a new Data object in an XML document.

        :param xml_doc: document xml for adding data
        :type xml_doc: XMLDocument
        :param xml_parrent: parent XML element data
        :param name: of the adding data
        :type name: str
        """
        new_element = Data.to_xml(self, xml_doc, xml_parrent, name)
        new_element.attributes['value'] = unicode(self.value)
        if self._data_type is complex:
            new_element.attributes['type'] = "complex"
        elif self._data_type is int:
            new_element.attributes['type'] = "int"
        elif self._data_type is float:
            new_element.attributes['type'] = "float"
        elif self._data_type is bool:
            new_element.attributes['type'] = "bool"
        elif isinstance(self._value, np.ndarray):
            new_element.attributes['value'] = unicode(self.value.tolist())
            new_element.attributes['type'] = "numpy"
            new_element.attributes['dtype'] = unicode(self.value.dtype)
        elif self._data_type is type:
            new_element.attributes['type'] = "type"
            new_element.attributes['value'] = unicode(self.value.__name__)
            new_element.attributes['module'] = unicode(self.value.__module__)
        else:
            new_element.attributes['type'] = "unicode"
            # minidom seams to convert special characters to \n & \t as well (same as minidom.parseString())
            # the following is pointless
#             if '#Parameter' in new_element.attributes['value'].value:
#                 print(new_element.attributes['value'].value)
#                 new_element.attributes['value'].value.replace('\n','&#10;')
#                 print(new_element.attributes['value'].value)
#                 new_element.attributes['value'].value.replace('\n','&#x9;')
#                 print(new_element.attributes['value'].value)
            
        xml_parrent.childNodes.append(new_element)

    def set_from_xml(self, xml_element):
        """ extract data from an xml element

        :param xml_element: xml element to extract data.
        """
        value = xml_element.attributes['value'].value
        if xml_element.attributes['type'].value == "numpy":
            dtype = xml_element.attributes['dtype'].value
            self._data_type = type(np.array([]))
            if xml_element.attributes['name'].value == "XRF_sim":
                #print('XRF_sim')
                #print(value)
                value = value.replace('inf', '0')
                #print(value)
            
            self._value = np.array(eval(value),dtype)
        else:
            self._data_type = eval(xml_element.attributes['type'].value)
            if self._data_type is unicode:
                self._value = xml_element.attributes['value'].value
#                 print(self._value) ####
            elif self._data_type is type:
                if xml_element.attributes['module'].value != "builtins":
                    str_value = "import "
                    str_value += xml_element.attributes['module'].value
                    str_value += "\n" 
                    str_value += "x=" + xml_element.attributes['module'].value
                    str_value += '.' + xml_element.attributes['value'].value
                else:
                    str_value = "x=" + xml_element.attributes['value'].value
                cont = {}
                exec(str_value, cont)
                self._value = cont["x"]
            else:
                type_name = unicode(xml_element.attributes['type'].value)
                if type_name == "bool":
                    if value == "True":
                        self._value = True
                    else:
                        self._value = False
                else:
                    content = (type_name + '("' + value + '")')
                    self._value = eval(content)


class QuantitiesData(Data):
    """ implementing a data with unit using quantities.
    """
    def __init__(self, value=0, unit=pq.angstrom, abstract=''):
        """ initialization

        :param value: value of data contain
        :param unit: unit of the quantities
        :type unit: pq.Quantities
        :param abstract: name of the abstract type.
        :type abstract: str
        """
        Data.__init__(self, value * unit, abstract)
        self._value = value * unit
        #: type of the data
        self._data_type = type(self.value)
        #: save unit
        self._unit = unit

    def __str__(self):
        return str(self._value)

    def convert_unit(self, target):
        """ Convert unit to a Data target.

        :param target: data type of the target
        :type target: QuantitiesData
        """
        self.unit = target.unit

    @property
    def unit(self):
        """ give the unit of the quantity value.

        :return: the unit
        :rtype: pq.Quantity
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """ Change unit of data

        :param unit: new unit
        :type unit: pq.Quantities
        """
        self._unit = unit
        self._value.units = unit

    @property
    def value(self):
        """getter for the value transforming the unit on demand.

        :param unit: unit wanted for the value.
        :type unit: pq.Quantity
        :return: value
        """
        if self._value.size == 1:
            # it's a single value:
            return self._value.item()
        else:
            # it's an array:
            return [i.item() for i in self._value]

    @value.setter
    def value(self, value):
        if isinstance(value, quantities.quantity.Quantity):
            self._value = value
            self._unit = value.units
        else:
            self._value = value * self._unit
            self._data_type = type(value)

    def to_xml(self, xml_doc, xml_parrent, name):
        """ add a new Data object in an XML document.

        :param xml_doc: document xml for adding data
        :type xml_doc: XMLDocument
        :param xml_parrent: parent XML element data
        :param name: of the adding data
        :type name: str
        """
        new_element = Data.to_xml(self, xml_doc, xml_parrent, name)
        new_element.attributes['value'] = unicode(self.value)
        if unicode(self.unit)[:3] == '1.0':
            unit_name = unicode(self.unit)[3:].split(' (')[0]
        else:
            unit_name = unicode(self.unit)[2:].split(' (')[0]
#         print(unit_name) # added for debugging
        try:
            unit_name = self.unit.symbol
        except AttributeError as ex:
            unit_name = "dimensionless"
            print(ex)
        new_element.attributes['unit'] = unit_name
        xml_parrent.childNodes.append(new_element)

    def set_from_xml(self, xml_element):
        """ extract data from an xml element

        :param xml_element: xml element to extract data.
        """
        value = eval(xml_element.attributes['value'].value)
        self._data_type = type(value)
        unit = xml_element.attributes['unit'].value
        self._unit = pq.quantity.Quantity(1, unit)
        self._value = pq.quantity.Quantity(value, unit)


class CompositeData(Data):
    """ implementation for composite data.
    """
    def __init__(self, value=None, abstract='', default_showing=True):
        """ initialization

        :param value: value of data contain
        :param abstract: name of the abstract type.
        :type abstract: str
        """
        # create value
        if value is not None:
            if not isinstance(value, dict):
                raise TypeError("value of a composite must be a dict")
            value = dict((key, make_data(value[key]))
                         for key in list(value.keys()))
        else:
            value = {}

        # initialize Data attributes
        Data.__init__(self, value, abstract)
        #: type of data
        self._data_type = dict

        #: information for showing list of tuple (name, key)
        self._showing_info = []

        # initialize default showing info
        if default_showing and self._value is not None:
            self.set_default_showing_info()

    @property
    def showing_info(self):
        """ property for access to showing information.
        """
        return self._showing_info

    @showing_info.setter
    def showing_info(self, showing_info):
        """ setting showing information list.
        """
        self._showing_info = showing_info

    def set_showing_info(self, key, showing_name="", index=None):
        """ create a new showing information
        """
        if showing_name == "":
            showing_name = key
        if index is None:
            self._showing_info.append((showing_name, key))
        else:
            self._showing_info.insert(index, (showing_name, key))

    def set_default_showing_info(self):
        """ set default showing information
        """
        for key in list(self._value.keys()):
            self.set_showing_info(key)

    def __getitem__(self, key):
        """ return an element

        :param key: name of the element to return
        :type key: str
        """
        if isinstance(key, SimpleData):
            key = unicode(key.value)
        if key not in list(self._value.keys()):
            raise KeyError("value " + unicode(key) + " does not exist - Ok if an operation has been selected")
        return self._value[key]

    def __setitem__(self, key, value):
        """ modify the value of one element.

        :param key: name of the element to return
        :type key: str
        :param value: new value of the element.
        """
        if key not in list(self._value.keys()):
            raise KeyError("value not in range")
        if isinstance(value, Data):
            self._value[key] = value
        else:
            if isinstance(self._value[key], QuantitiesData):
                unit = self._value[key].unit
            else:
                unit = None
            abstract = self._value[key].abstract_type
            composite = isinstance(self._value[key], CompositeData)
            self._value[key] = make_data(value, unit, abstract, composite)

    def __str__(self):
        """ get a string representation
        """
        result = ""
        for key, value in sorted(self._value.items()):
            if isinstance(value, CompositeData):
                result += str(key) + " = (" + str(value) + "), "
            else:
                result += str(key) + " = " + str(value) + ", "
        return result[:-2]

    def items(self):
        """ return component element list

        :return: list of component
        :rtype: list
        """
        return self._value.items()

    def keys(self):
        """ return component element name list

        :return: list of name of component
        :rtype: list
        """
        return list(self._value.keys())

    def convert_unit(self, target):
        """ Convert unit of every unit convertible component to a Data target.

        :param target: data type of the target
        :type target: Data
        """
        for key in list(self._value.keys()):
            if isinstance(self._value[key], QuantitiesData) or\
                    isinstance(self._value[key], CompositeData):
                self._value[key].convert_unit(target.real_value[key])

    @property
    def value(self):
        """getter for the _value

        :return: value
        :rtype: dict
        """
        return dict((key, self._value[key].value)
                    for key in list(self._value.keys()))

    @property
    def composite_key(self):
        """ return the list of key.

        :return: list of key
        :rtype: list
        """
        return sorted(list(self._value.keys()))

    def is_compatible(self, data):
        """ Test if data is compatible to another data.

        :param data: other data to determine if it is compatible.
        :type data: Data
        :return: true if data is compatible to self.
        :rtype: boolean
        """
        if not Data.is_compatible(self, data):
            return False
        for (key, element) in self._value.items():
            try:
                if not element.is_compatible(data.real_value[key]):
                    return False
            except KeyError:
                return False
        return True

    def to_xml(self, xml_doc, xml_parrent, name):
        """ add a new Data object in an XML document.

        :param xml_doc: document xml for adding data
        :type xml_doc: XMLDocument
        :param xml_parrent: parent XML element data
        :param name: of the adding data
        :type name: str
        """
        new_element = Data.to_xml(self, xml_doc, xml_parrent, name)
        for key in self._value.keys():
            value = self._value[key]
            value.to_xml(xml_doc, new_element, key)
        xml_parrent.childNodes.append(new_element)

    def set_from_xml(self, xml_element):
        """ extract data from an xml element

        :param xml_element: xml element to extract data.
        """
        for element in xml_element.childNodes:
            if element.attributes is not None:
                name = element.attributes["name"].value
                self._value[name] = XMLDataFormat.from_xml(element)
        self._abstract_data_type = xml_element.attributes['abstract'].value
        if self._showing_info == []:
            self.set_default_showing_info()


class ListData(Data):
    """ implementation for a list of data.
    """
    def __init__(self, values=None, unit=None, abstract=''):
        """ initialization

        :param value: value of data contain
        :param abstract: name of the abstract type.
        :type abstract: str
        """
        if values is not None:
            if len(values) > 0 and isinstance(values[0], Data):
                value_tab = [value for value in values]
            else:
                value_tab = [make_data(value, unit) for value in values]
        else:
            value_tab = []
        Data.__init__(self, value_tab, abstract)
        #: type of data
        self._data_type = list
        self._current = 0

    def __str__(self):
        """ get a string representation.
        """
        return str([element for element in self.value])

    def __delitem__(self, key):
        """ call when you use **del x[key]

        :param key: index to delete
        :type key: integer
        """
        del self._value[key]

    def __iter__(self):
        """ iterator for Python 2 et 3
        """
        return self._value.__iter__()

    def __next__(self):
        """ next iterator for Python 3
        """
        return self._value.__next__()

    def __getitem__(self, key):
        """ return an element.

        :param key: name of the element to return
        :type key: integer
        """
        if (key < 0) or (key > (len(self._value) - 1)):
            raise KeyError("value " + str(key) + " is not in range")
        return self._value[key]

    def __setitem__(self, key, value):
        """ modify the value of one element.

        :param key: name of the element to return
        :type key: str
        :param value: new value of the element.
        """
        if (key < 0) or (key > (len(self._value) - 1)):
            raise KeyError("value not in range")
        if isinstance(self._value[key], QuantitiesData):
            unit = self._value[key].unit
        else:
            unit = None
        abstract = self._value[key].abstract_type
        composite = isinstance(self._value[key], CompositeData)
        self._value[key] = make_data(value, unit, abstract, composite)

    def insert(self, index, value):
        """ insert new value in tab
        """
        self._value.insert(index, value)

    def next(self):
        """ next iterator for Python 2
        """
        return self._value.next()

    def clear(self):
        """ clear all value
        """
        self._value = []

    @property
    def value(self):
        """getter for the value

        :param unit: unit wanted for the value.
        :type unit: pq.Quantity
        :return: value
        """
        return [value.value for value in self.real_value]

    def is_compatible(self, data):
        """ Test if data is compatible to another data.

        :param data: other data to determine if it is compatible.
        :type data: Data
        :return: true if data is compatible to self.
        :rtype: boolean
        """
        if not Data.is_compatible(self, data):
            return False
        for (i, element) in enumerate(self._value):
            try:
                if not element.is_compatible(data.real_value[i]):
                    return False
            except IndexError:
                pass
        return True

    def append(self, value):
        """ append a new value in the list

        :param value: new value to add in the list.
        :type value: Data
        """
        self._value.append(value)

    def to_xml(self, xml_doc, xml_parrent, name):
        """ add a new Data object in an XML document.

        :param xml_doc: document xml for adding data
        :type xml_doc: XMLDocument
        :param xml_parrent: parent XML element data
        :param name: of the adding data
        :type name: str
        """
        new_element = Data.to_xml(self, xml_doc, xml_parrent, name)
        i = 0
        for value in self._value:
            value.to_xml(xml_doc, new_element, unicode(i))
            i += 1
        xml_parrent.childNodes.append(new_element)

    def set_from_xml(self, xml_element):
        """ extract data from an xml element

        :param xml_element: xml element to extract data.
        """
        self._value = []
        for element in xml_element.childNodes:
            if element.attributes is not None:
                self._value.append(XMLDataFormat.from_xml(element))


def copy_data(data):
    """ copy a data object.

    :param data: data to copy
    :type data: Data
    """
    if data is None:
        return None
    destination = data.__class__()
    value = data.real_value
    if isinstance(data, QuantitiesData):
        return make_data(data.value, data.unit)
    elif isinstance(data, CompositeData):
        for key in list(value.keys()):
            destination.real_value[key] = copy_data(value[key])
        destination.showing_info = data.showing_info
    elif isinstance(data, ListData):
        destination.real_value = [copy_data(v) for v in value]
    else:
        return make_data(value, abstract=data.abstract_type)
    destination.finish_copy()
    destination.abstract_type = data.abstract_type
    return destination


def make_data(value=None, unit=None, abstract='', composite=False, copy=False):
    """ make a new data object of the good type.

    :param value: value of new Data object
    :param unit: unit of the value for the new Data object
    :type unit: pq.quantities
    :param abstract: name of the abstract type
    :type abstract: str
    :param composite: if Data must be a composite object
    :type composite: boolean
    """
    if isinstance(value, Data):
        if copy:
            return copy_data(value)
        else:
            return value
    if isinstance(value, dict):
        key_list = list(value.keys())
        if 'abstract' in key_list:
            abstract = value['abstract']
            del value['abstract']
        if 'composite' in key_list:
            composite = value['composite']
            del value['composite']
        if 'unit' in key_list:
            unit = value['unit']
            value = value['value']

    if isinstance(value, list):
        return ListData(value, unit, abstract)

    if composite:
        data = CompositeData(value, abstract)
    elif unit is not None:
        if value is None:
            value = 0
        data = QuantitiesData(value, unit, abstract)
    else:
        data = SimpleData(value, abstract)
    return data


class DataFormat(object):
    """ defining a new data format
    """
    __metaclass__ = ABCMeta

    #: define if the format is usable for all data
    IS_MAIN = False

    @abstractmethod
    def import_file(self, file_name):
        """ import from file

        :param file_name: name of the file to import.
        :type file_name: str
        :return: data from the file
        """

    @abstractmethod
    def export_data(self, file_name, data):
        """ export to file

        :param file_name: name of the file to export.
        :type file_name: str
        :param data: data to export
        :type data: Data
        """

    def is_main_format(self):
        """ define XMLDataFormat like a main format.

        :return: IS_MAIN
        :rtype: boolean
        """
        return self.IS_MAIN


class XMLDataFormat(DataFormat):
    """ implementation of XML load and save.
    """
    #: define if the format is usable for all data
    IS_MAIN = True

    @staticmethod
    def create_data_xml(data, name='main'):
        """ create an xml document from Data object.

        :param data: data to converte.
        :type data: Data
        :param name: name of the root element.
        :type name: str
        :return: the created xml document
        """
        result = minidom.Document()
        root_node = result.createElement("data_file")
        result.appendChild(root_node)
        data.to_xml(result, result.childNodes[0], name)
        return result

    @staticmethod
    def from_xml_string(xml_string):
        """ create a data object from xml string.

        :param xml_string: string XMl for creating data
        :return: dictionnary of data from xml
        :rtype: dict
        """
        xml_document = minidom.parseString(xml_string)
        data_list = {}
        for xml_element in xml_document.childNodes[0].childNodes:
            data = XMLDataFormat.from_xml(xml_element)
            if data is not None:
                data_list[xml_element.attributes['name'].value] = data
        return data_list

    @staticmethod
    def from_xml(xml_element):
        """ create a data object from xml element.

        :param xml_element: xml element to extract data.
        :return: data object create from the xml element.
        :rtype: paf.data.Data
        """
        dico_out = {}
        try:
            script_str = "import "
            script_str += xml_element.attributes['module_name'].value
            script_str += '\nd=' + xml_element.localName + '()'
            exec(script_str, dico_out)
            data_object = dico_out["d"]
            data_object.set_from_xml(xml_element)
            return data_object
        except TypeError as er:
            print(er)

    def export_data(self, file_name, data):
        """ export in xml file

        :param file_name: name of the file where exporting data.
        :type file_name: str
        :param data: data to export
        :type data: Data
        """
        xml_data = XMLDataFormat.create_data_xml(data)
        with codecs.open(file_name, "w", "utf-8") as file_open:
            xml_data.writexml(file_open, encoding='utf-8', indent=" ",
                              addindent=" ", newl="\n")

    def import_file(self, file_name):
        """ import from file

        :param file_name: name of file to import
        :type file_name: str
        :return: data from XML
        :rtype: Data
        """
        with codecs.open(file_name, "r", "utf-8") as file_open:
            file_content = file_open.read().encode("utf-8")
        
        # conversion of some \n and \t so that they are properly interpreted by minidom
        result = re.sub('value="#Parameter.*?>', characterRepl, file_content, 0, re.DOTALL) # .*? question mark means * is non-greedy (ie shortest match)
        return self.from_xml_string(result)


class DataIo(object):
    """ class for IO management of Data.
    """
    def __init__(self, main_data_format=XMLDataFormat()):
        """ initialization

        :param main_data_format: define the main data format
        :type main_data_format: DataFormat
        """
        #: main data format
        self._main_data_format = main_data_format
        #: data format map
        self._data_format_map = {}

    @property
    def main_data_format(self):
        """ return format object for default format
        """
        return self._main_data_format

    def file_to_data(self, file_name, format_key=None, data_format=None):
        """ create a data object from a file.

        :param file_name: name of the file to create
        :type file_name: str
        :param format_key: key in data format map to acces to the data format
        :return: data from the file
        :rtype: Data
        """
        list_format_key = list(self._data_format_map.keys())
        if data_format is None:
            if format_key is None:
                data_format = self._main_data_format
            elif format_key in list_format_key:
                data_format = self._data_format_map[format_key]
            else:
                raise TypeError("Format not defined for " + format_key)
        return data_format.import_file(file_name)

    def data_to_file(self, file_name, data, format_key=None, data_format=None):
        """ create a file with data object.

        :param data: data to record on a file
        :type data: paf.data.Data
        :param file_name: name of file to sauve
        :type file_name: str
        """
        list_format_key = list(self._data_format_map.keys())
        if data_format is None:
            if format_key is None:
                if data.abstract_type in list_format_key:
                    data_format = self._data_format_map[data.abstract_type]
                elif data.data_type in list_format_key:
                    data_format = self._data_format_map[data.data_type]
                else:
                    data_format = self._main_data_format
            elif format_key in list_format_key:
                data_format = self._data_format_map[format_key]
        data_format.export_data(file_name, data)
