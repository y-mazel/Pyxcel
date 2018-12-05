# -*- coding: utf8 -*-
"""
data treatement filter

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import numpy as np
import paf.data
MAKE_DATA = paf.data.make_data


class interval(paf.data.CompositeData):
    """ define an interval.
    """
    def __init__(self, inf=0., sup=1., ratio=1):
        """initialization
        """
        value = {"inf": inf, "sup": sup, "ratio": ratio}
        paf.data.CompositeData.__init__(self, value, abstract="interval")


class NbPointsFilter(paf.filter_base.Filter):
    """ filter to reduce point number in experimental data
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)
        self.add_expected_parameter("point_reduction", MAKE_DATA([interval()]),
                                    MAKE_DATA([interval()]))

    def run(self):
        """ running
        """
        data = self.get_data("main")
        for interval in self["point_reduction"].value:
            inf = interval['inf']
            sup = interval['sup']
            ratio = interval['ratio']
            int_mask = np.logical_and(data.x > inf, data.x < sup)
            inf_mask = np.logical_not(data.x > inf)
            sup_mask = np.logical_not(data.x < sup)
            int_x = data.x[int_mask][::ratio]
            inf_x = data.x[inf_mask]
            sup_x = data.x[sup_mask]
            data.x = np.concatenate((inf_x, int_x, sup_x))
            int_y = data.y[int_mask][::ratio]
            inf_y = data.y[inf_mask]
            sup_y = data.y[sup_mask]
            data.y = np.concatenate((inf_y, int_y, sup_y))
            int_error = data.error[int_mask][::ratio]
            inf_error = data.error[inf_mask]
            sup_error = data.error[sup_mask]
            data.error = np.concatenate((inf_error, int_error, sup_error))
        self.fill_port("main", MAKE_DATA(data))


class WindowsFilter(paf.filter_base.Filter):
    """ filter to select a windows.
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)
        self.add_expected_parameter("inf", MAKE_DATA(0.), MAKE_DATA(0.))
        self.add_expected_parameter("sup", MAKE_DATA(5.), MAKE_DATA(5.))

    def run(self):
        """ running
        """
        data = self.get_data("main")
        inf = self['inf'].value
        sup = self['sup'].value
        int_mask = np.logical_and(data.x > inf, data.x < sup)
        data.x = data.x[int_mask]
        data.y = data.y[int_mask]
        data.error = data.error[int_mask]
        self.fill_port("main", MAKE_DATA(data))
