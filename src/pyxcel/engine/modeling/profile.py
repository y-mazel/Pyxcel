# -*- coding: utf8 -*-
"""
Implementation of class for describing concentration profile...

    :platform: Unix, Windows
    :synopsis: concentration profile

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from scipy.special import erf
import numpy as np
import paf.data
from pyxcel.engine.modeling.entity import ProfileComputer, DensityProfile
MAKE_DATA = paf.data.make_data

# concentration profile


class GaussianInterface(ProfileComputer):
    """ to compute a gaussian interface profile
    """
    def __init__(self, material=""):
        """ initialization
        """
        kwargs = {"amplitude": 0.3, "center_of_mass": 7.,
                  "distribution_width": 3.}
        ProfileComputer.__init__(self, material, kwargs)

    def _func(self, x):
        """ function
        """
        amplitude = self["kwargs"]["amplitude"].value
        center_of_mass = self["kwargs"]["center_of_mass"].value
        distribution_width = self["kwargs"]["distribution_width"].value
        return amplitude/2*(1+erf((x-center_of_mass /
                                                 distribution_width)))


class Gaussian(ProfileComputer):
    """ to compute a gaussian interface profile
    """
    def __init__(self, material=""):
        """ initialization
        """
        kwargs = {"amplitude": 0.3, "center_of_mass": 7.,
                  "distribution_width": 3.}
        ProfileComputer.__init__(self, material, kwargs)

    def _func(self, x):
        """ function
        """
        amplitude = self["kwargs"]["amplitude"].value
        center_of_mass = self["kwargs"]["center_of_mass"].value
        distribution_width = self["kwargs"]["distribution_width"].value
        d1 = -np.power(x-center_of_mass, 2.)
        d2 = 2*np.power(distribution_width, 2.)
        return amplitude*np.exp(d1/d2)

# anti profile class factory


def anti_prof(prof):
    """ create a profile returning 1 - profile
    """
    class AntiProf(prof):
        """ anti-profile
        """
        def _func(self, x):
            """ function
            """
            return 1 - prof._func(self, x)
    return AntiProf


class AntiGaussianInterface(anti_prof(GaussianInterface)):
    """
    """

class AntiGaussian(anti_prof(Gaussian)):
    """
    """

# density profile


class LinearDensityProfile(DensityProfile):
    """ lineare density profile
    """
    def __init__(self, start=0.02, end=0.022, type_='num'):
        """ initialization

        :param start: starting value
        :type start: float
        :param end: ending value
        :type end: float
        :param type_: type of density describe by the profile *num or mass*
        :type type_: str
        """
        kwargs = {"start": start, "end": end}
        DensityProfile.__init__(self, kwargs, type_)
        self._start = start
        self._end = end

    def __setitem__(self, key, value):
        """ new set item for start and end
        """
        paf.data.CompositeData.__setitem__(self, key, value)
        if key == "start":
            self._start = value
        elif key == "end":
            self._end = value

    def __call__(self, x):
        """ execute profile
        """
        # x minus one
        x_m_1 = np.array([0] + list(x[:-1]))
        a = (self._end - self._start)/x[-1]
        return ((a * x_m_1 + self._start)+(a * x + self._start))/2

    def finish_copy(self):
        """ initialize start and end after copy
        """
        self._start = self["start"].value
        self._end = self["end"].value
