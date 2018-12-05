# -*- coding: utf8 -*-
"""
Contain tools for calculating figure of merite.

    :platform: Unix, Windows
    :synopsis: optimisation filter to use GenX.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import numpy as np
import paf.data


# dataset to replace GenX DataSet
class DataSet(paf.data.CompositeData):
    """ represent a set of data
    """
    def __init__(self):
        """ initialization
        """
        self._x = np.array([])
        self._y = np.array([])
        self._error = np.array([])
        paf.data.CompositeData.__init__(self, {"x": self._x, "y": self._y,
                                               "error": self._error},
                                        "DataSet")

    def __delitem__(self, index):
        """ del item at index
        """
        self._x = np.delete(self._x, index)
        self._y = np.delete(self._y, index)
        self._error = np.delete(self._error, index)

    @property
    def x(self):
        """ getter for x
        """
        return self._x

    @x.setter
    def x(self, value):
        """ setter for x
        """
        self._x = value
        self["x"] = value

    @property
    def y(self):
        """ getter for y
        """
        return self._y

    @y.setter
    def y(self, value):
        """ setter for y
        """
        self._y = value
        self["y"] = value

    @property
    def error(self):
        """  getter for error bars
        """
        return self._error

    @error.setter
    def error(self, value):
        """ setter for error bars
        """
        self._error = value
        self["error"] = value

    def from_two_column(self, two_column_data):
        """ load data from a numpy two column data
        """
        self.x = two_column_data[:, 0]
        self.y = two_column_data[:, 1]
        self.error = np.sqrt(self.y)

    def load_file(self, file_name):
        """ load data from file
        """
        load_result = np.loadtxt(file_name, skiprows=1)
        self.from_two_column(load_result)

    def set_from_xml(self, xml_element):
        """ overwrite for reinitilizing self._x, self._y and self._error value.
        """
        paf.data.CompositeData.set_from_xml(self, xml_element)
        self._x = self["x"].value
        self._y = self["y"].value
        self._error = self["error"].value

    def copy(self, dataset):
        """ copy the dataset parameter
        """
        self.x = np.copy(dataset.x)
        self.y = np.copy(dataset.y)
        self.error = np.copy(dataset.error)

    def create_copy(self):
        """ create and return a copy the dataset parameter
        """
        new = DataSet()
        new.copy(self)
        return new


# FOM class
class FOM(object):
    """ generic figure of merit
    """

    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = []
        self._p = p

    def __call__(self, simulation, data):
        """ call FOM
        """
        simulation[np.isinf(simulation)] = 0

    @property
    def inf_error(self):
        """ access to list of element making FOM result equals to infinity
        """
        return self._inf_error

    def del_error_to_inf(self, data, sim=None):
        """ delete data cause FOM equals to infinity
        """
        nb = 0
        for index, x in enumerate(data.y):
            if x in self._inf_error:
                del data[index-nb]
                if sim is not None:
                    sim = np.delete(sim, index-nb)
                nb += 1
        if sim is not None:
            return sim
        else:
            return None


# simple FOM functions

# double
class log(FOM):
    """ log fom
    """
    def __init__(self, p=1):
        """ initialize

        :param p: number of parameter to fit for Uncertainty parameter
        :type p: int
        """
        self._inf_error = [0.]
        self._p = p

    def __call__(self, sim, data):
        """ Average absolute logarithmic difference
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1.0/((N-self._p)*1.)*np.sum(np.sum(np.abs(np.log10(data.y) -
                                                         np.log10(sim))))


class log2n(FOM):
    """ create log2n fom
    """
    def __init__(self, p=1):
        """ initialize

        :param p: number of parameter to fit for Uncertainty parameter
        :type p: int
        """
        self._p = p
        self._inf_error = [1., 0.]

    def __call__(self, sim, data):
        """ Average absolute logarithmic square normalized difference
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1.0/((N-self._p)*1.)*np.sum((np.log10(data.y) -
                                            np.log10(sim))**2 /
                                           np.log10(data.y)**2)


class chi2n(FOM):
    """ create chi2n fom
    """
    def __init__(self, p=1):
        """ initialize

        :param p: number of parameter to fit for Uncertainty parameter
        :type p: int
        """
        self._p = p
        self._inf_error = [0.]

    def __call__(self, sim, data):
        """ simple chi 2
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1.0/((N-self._p)*1.)*np.sum((data.y - sim)**2/data.y**2)
# double


class chi2bars(FOM):
    """ create chi2bars fom
    """
    def __init__(self, p=1):
        """ initialization

        :param p: number of parameter to fit for Uncertainty parameter
        :type p: int
        """
        self._p = p
        self._inf_error = [0.]

    def __call__(self, sim, data):
        """ simple chi 2
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1.0/((N-self._p)*1.)*np.sum((data.y - sim)**2/data.error**2)


class chi2d(FOM):
    """ create chi2 fom
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = [0.]
        self._p = p

    def __call__(self, sim, data):
        """ simple chi 2
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        sim_z = sim != 0
        new_sim = sim[sim_z]
        new_data = data.y[sim_z]
        return (1.0/(((N-self._p)*1.)*np.max(new_data)) *
                np.sum((new_data - new_sim)**2/new_sim))


class log2d(FOM):
    """ create log2 fom
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = [0.]
        self._p = p

    def __call__(self, sim, data):
        """ simple chi 2 log
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        min_sim = np.min(sim)
        min_data = np.min(data.y)
        new_sim = sim
        new_data = data.y
        if min_data < 1 or min_sim < 1:
            if min_data < min_sim:
                min_ = min_data
            else:
                min_ = min_sim
            new_sim = sim/min_*2
            new_data = data.y/min_*2
        new_sim = np.log10(new_sim)
        new_data = np.log10(new_data)
        return (1.0/(((N-self._p)*1.)*np.max(new_data)) *
                np.sum((new_data - new_sim)**2/new_sim))


class theta4(FOM):
    """ create thta 4 fom
    """
    def __call__(self, sim, data):
        """ simple chi 2 theta 4
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        new_sim = sim * data.x**4
        new_data = data.y * data.x**4
        return (1.0/(((N-self._p)*1.)*np.max(new_data)) *
                np.sum((new_data - new_sim)**2/new_sim))


# b like fom function


class b_logarithmic(FOM):
    """ create a b like logarithmic function
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = [0.]
        self._p = p

    def __call__(self, sim, data):
        """ b like logarithmic fom
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1/((N-self._p)*1.)*np.sum((np.log10(data.y)-np.log10(sim))**2)


class b_normalized_logarithmic(FOM):
    """ create a b like logarithmic function
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = [1., 0.]
        self._p = p

    def __call__(self, sim, data):
        """ b like logarithmic fom
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1/((N-self._p)*1.)*np.sum(((np.log10(data.y)-np.log10(sim)) /
                                          np.log10(data.y))**2)


class b_normalized(FOM):
    """ create a b like logarithmic function
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = [0.]
        self._p = p

    def __call__(self, sim, data):
        """ b like logarithmic fom
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1/((N-self._p)*1.)*np.sum(((data.y-sim) / data.y)**2)


class b_standart(FOM):
    """ create a b like logarithmic function
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = []
        self._p = p

    def __call__(self, sim, data):
        """ b like logarithmic fom
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1/((N-self._p)*1.)*np.sum((data.y-sim)**2 / data.y)


class b_log_module(FOM):
    """ create a b like logarithmic function
    """
    def __init__(self, p=1):
        """ initialization
        """
        self._inf_error = [0.]
        self._p = p

    def __call__(self, sim, data):
        """ b like logarithmic fom
        """
        FOM.__call__(self, sim, data)
        N = len(data.y)
        return 1/((N-self._p)*1.)*np.sum(np.abs(np.log10(data.y)-np.log10(sim))
                                         )
