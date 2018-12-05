# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Module use to parameter a pipeline element.

    :platform: Unix, Windows
    :synopsis: Module use to parameter a pipeline element.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta
import paf.data
MAKE_DATA = paf.data.make_data


class Parametrable(object):
    """ Abstract class for implementing all parameter utilities.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ initialization
        """
        #: self parameter
        self._parameter = {}
        #: dictionary of expected parameter with type
        self._expected_parameter = {}
        #: list of name of fixed parameter
        self._fixed = []
        #: composite data representation
        self._data_composite = None
        #: showing info when it tranforms into Composite data
        self._showing_info = []

    def __getitem__(self, name):
        """ parameter getter.

        :param name: name of the parameter
        :type name: str
        :returns: parameter in Data format
        """
        return self._parameter[name]

    def __setitem__(self, name, value):
        """ parameter setter.

        :param name: name of the parameter
        :type name: str
        :param value: new value for the parameter
        :raises: TypeError, KeyError
        """
        if isinstance(value, paf.data.Data):
            if isinstance(value, paf.data.QuantitiesData):
                value.unit = self._expected_parameter[name].unit
            data = value
        else:
            composite = isinstance(self._expected_parameter[name],
                                   paf.data.CompositeData)
            abstract = self._expected_parameter[name].abstract_type
            if isinstance(self._expected_parameter[name],
                          paf.data.QuantitiesData):
                unit = self._expected_parameter[name].unit
                data = MAKE_DATA(value, unit, composite, abstract)
            else:
                data = MAKE_DATA(value, composite=composite, abstract=abstract)
        self._parameter[name] = data

    @property
    def parameter_list(self):
        """ getter for the list of all parameter name.

        :returns: list of all parameter name.
        :rtype: list of str
        """
        return list(self._parameter.keys())

    def add_expected_parameter(self, name, data_type, default_value=None,
                               showing_info=None, show=True):
        """ add an expected parameter

        :param name: name of the new parameter
        :type name: str
        :param data_type: type of expected parameter
        :type data_type: paf.data.Data
        """
        self._expected_parameter[name] = data_type
        self[name] = default_value
        if show:
            if showing_info is None:
                self._showing_info.append((name, name))
            else:
                self._showing_info.append((name, showing_info))

    def get_expected_data_type(self, name):
        """ get the data type of a parameter

        :param name: name of the expected parameter
        :type name: str
        :return: data type of a parameter
        :rtype: paf.data.Data
        """
        return self._expected_parameter[name]

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

    def to_composite_data(self):
        """ transform the parameter in a composite data. *modify the default
        setter to set parameter.*

        :return: the composite data
        :rtype: paf.data.CompositeData
        """
        class CompositeParameter(paf.data.CompositeData):
            """ composite data observable for represent parameters
            """
            def __init__(self, parametrable, value=None, abstract='',
                         default_showing=True):
                """ initialization
                """
                paf.data.CompositeData.__init__(self, value, abstract,
                                                default_showing)
                self._parametrable = parametrable

            def __setitem__(self, key, value):
                """ new method for __setitem__
                """
                self._parametrable[key] = value
                paf.data.CompositeData.__setitem__(self, key, value)

            def to_xml(self, xml_doc, xml_parrent, name):
                """ converte to xml
                """
                type_name = "paf.data.CompositeData"
                module_name = "paf.data"
                new_element = xml_doc.createElement(type_name)
                new_element.attributes['name'] = name
                new_element.attributes['module_name'] = module_name
                new_element.attributes['abstract'] = self.abstract_type
                for key in self._value.keys():
                    value = self._value[key]
                    value.to_xml(xml_doc, new_element, key)
                xml_parrent.childNodes.append(new_element)

        if self._data_composite is None:
            self._data_composite = (CompositeParameter(self, self._parameter))
            self._data_composite.showing_info = self.showing_info

        return self._data_composite

    @property
    def composite_value(self):
        """ return a composite value for the parameter without link.
        """
        data_composite = paf.data.CompositeData(self._parameter)
        data_composite.showing_info = self.showing_info
        return data_composite

    @composite_value.setter
    def composite_value(self, value):
        """ set all value from composite data
        """
        for name, data in value.items():
            self[name] = data
        self._data_composite = None
