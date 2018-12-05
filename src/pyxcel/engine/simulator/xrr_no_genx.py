# -*- coding: utf8 -*-
"""
module for XRR simulator.

    :platform: Unix, Windows
    :synopsis: XRR simulation using GenX.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import pyxcel.engine.simulator.generic
import numpy as np
import paf.data
import sys
from scipy.special import erf
if sys.version_info[0] >= 3:
    from functools import reduce
MAKE_DATA = paf.data.make_data


def GaussIntensity(alpha, s1, s2, sigma_x):
    """ from GenX
    """
    sinalpha = np.sin(alpha*np.pi/180)
    return (erf(s2*sinalpha/np.sqrt(2.0)/sigma_x) +
            erf(s1*sinalpha/np.sqrt(2.0)/sigma_x)) / 2.0


def SquareIntensity(alpha, slen, beamwidth):
    """ from GenX
    """
    F = slen/beamwidth*np.sin(alpha*np.pi/180)
    return np.where(F <= 1.0, F, np.ones(F.shape))


def resolution_vector(Q, dQ, points, range_=3):
    """ calculate resolution vector
    """
    Qstep = 2*range_*dQ/points
    Qres = Q+(np.arange(points)-(points-1)/2)[:, np.newaxis]*Qstep
    weight = (1/np.sqrt(2*np.pi)/dQ *
              np.exp(-(np.transpose(Q[:, np.newaxis])-Qres)**2/(dQ)**2/2))
    Qret = Qres.flatten()
    return (Qret, weight)


def ConvoluteFast(Q, I, dQ, range_=3):
    """ from GenX :
        Fast convlution - constant resolution
        constant spacing between data!
    """
    Qstep = Q[1]-Q[0]
    resvector = np.arange(-range_*dQ, range_*dQ+Qstep, Qstep)
    weight = 1/np.sqrt(2*np.pi)/dQ*np.exp(-(resvector)**2/(dQ)**2/2)
    Iconv = (np.convolve(np.r_[np.ones(resvector.shape)*I[0], I,
                               np.ones(resvector.shape)*I[-1]],
                         weight/weight.sum(), mode=1)
             [resvector.shape[0]:-resvector.shape[0]])
    return Iconv


def ConvoluteResolutionVector(Qret, I, weight):
    """ from GenX:
        Include the resolution with Qret and weight calculated from
        ResolutionVector and I the calculated intensity at each point. returns
        the intensity
    """
    Qret2 = Qret.reshape(weight.shape[0], weight.shape[1])
    I2 = I.reshape(weight.shape[0], weight.shape[1])
    norm_fact = np.trapz(weight, x=Qret2, axis=0)
    Int = np.trapz(I2*weight, x=Qret2, axis=0)/norm_fact
    return Int


def ConvoluteFastVar(Q, I, dQ):
    """ From GenX :
        Fast convolution - varying resolution
        constant spacing between the dat.
    """
    weight = 1/np.sqrt(2*np.pi)/dQ*np.exp(-(Q[:, np.newaxis]-Q)**2/(dQ)**2/2)
    Itemp = I[:, np.newaxis]*np.ones(I.shape)
    norm_fact = np.trapz(weight, axis=0)
    Int = np.trapz(Itemp*weight, axis=0)/norm_fact
    return Int


def refl(theta, wavelength, n, d, sigma):
    """ calculate XRR
    """
    d = d[1:-1]
    sigma = sigma[:-1]
    # Length of k-vector in vaccum
    k = 2*np.pi/wavelength
    # Calculates the wavevector in each layer
    Qj = 2*n[-1]*k*np.sqrt(n[:, np.newaxis]**2/n[-1]**2 -
                           np.cos(theta*np.pi/180)**2)
    # Fresnel reflectivity for the interfaces
    rp = (Qj[1:]-Qj[:-1])/(Qj[1:]+Qj[:-1])*np.exp(-Qj[1:]*Qj[:-1]/2 *
                                                  sigma[:, np.newaxis]**2)
    p = np.exp(1.0j*d[:, np.newaxis]*Qj[1:-1])
    # Setting up a matrix for the reduce function. Reduce only takes one array
    # as argument
    rpp = np.array(list(map(lambda x, y: [x, y], rp[1:], p)))

    # Paratt's recursion formula
    def formula(rtot, rint):
        return (rint[0]+rtot*rint[1])/(1+rtot*rint[0]*rint[1])
    # Implement the recursion formula
    r = reduce(formula, rpp, rp[0])
    return abs(r)**2


def resolve_parameter(sample):
    """ equivalent to sample.resolveparameter
    """
    numpy_param_type = {"d": np.float64, "numerical_density": np.float64,
                        "f": np.complex64, "sigmar": np.float64}
    parameters = {}
    for key in sample["substrate"].keys():
        parameters[key] = [sample["substrate"][key].value]
        parameters[key] += [lay[key].value
                            for lay in reversed(sample["layers"])]
        parameters[key] += [sample["ambient"][key].value]
        if key in numpy_param_type.keys():
            parameters[key] = np.array(parameters[key],
                                       dtype=numpy_param_type[key])
    return parameters


def simulate(TwoThetaQz, parameters, instrument, samlen):
    """ simulate XRR using only mpyxcel
    """
    # access to value of parameter
    restype = instrument["detector"]["restype"].value
    res = instrument["detector"]["res"].value
    respoint = instrument["detector"]["respoints"].value
    resintrange = instrument["detector"]["resintrange"].value
    coords = instrument["source"]["coords"].value
    wavelength = instrument["source"]["wavelength"].value
    I0 = instrument["source"]["I0"].value

    # configure instrument parameter
    weight = 0
    if restype == 2:
        TwoThetaQz, weight = resolution_vector(TwoThetaQz[:], res, respoint,
                                               resintrange)
    theta = TwoThetaQz/2
    if coords == 0:
        theta = np.arcsin(TwoThetaQz/4/np.pi*wavelength)*180./np.pi

    # configure sample parameter
    re = 2.82e-13*1e2/1e-10
    n = 1 - (parameters['numerical_density']*re*wavelength**2/2/np.pi *
             parameters['f']*1e-4)

    # calculate reflectivity
    R = refl(theta, wavelength, n, parameters['d'], parameters['sigmar']) * I0

    # Footprint corrections
    foocor = 1.0
    footype = instrument["source"]["footype"].value
    beamw = instrument["source"]["beamw"].value
    Ibkg = instrument["detector"]["Ibkg"].value
    resintrange = instrument["detector"]["resintrange"].value
    if footype == 1:
        foocor = GaussIntensity(theta, samlen/2.0, samlen/2.0, beamw)
    elif footype == 2:
        foocor = SquareIntensity(theta, samlen, beamw)
    if restype == 0:
        R = R[:]*foocor
    elif restype == 1:
        R = ConvoluteFast(TwoThetaQz, R[:]*foocor, res, resintrange)
    elif restype == 2:
        R = ConvoluteResolutionVector(TwoThetaQz, R[:]*foocor, weight)
    elif restype == 3:
        R = ConvoluteFastVar(TwoThetaQz, R[:]*foocor, res)
    return R + Ibkg


class XRRGenXSimulator(pyxcel.engine.simulator.generic.Simulator):
    """ simulator for XRR
    """

    def __init__(self, theta_array=None, stack=None, parameter=None,
                 instrument=None):
        """ initialization
        """
        abstract = "simulator_XRR"
        pyxcel.engine.simulator.generic.Simulator.__init__(self, theta_array,
                                                           stack, instrument,
                                                           abstract)

    @property
    def model_parameters(self):
        """ accessing to parameters of the model
        """
        return self._parmeters

    @model_parameters.setter
    def model_parameters(self, value):
        """ setter for model parameters
        """
        self._parmeters = value

    def initialization(self, filter_):
        """ initializing XRR simulation.
        """
        pyxcel.engine.simulator.generic.Simulator.initialization(self, filter_)
        self._instrument = self["instrument"]
        self._samlen = self["parameter"]["samplen"].value
        self._parmeters = resolve_parameter(self._sample)
        self._stack_name_list = list(self._parmeters['name'])

    def simulate(self):
        """ simulate XRR.
        """
        # call parent function
        pyxcel.engine.simulator.generic.Simulator.simulate(self)

        # get theta array value
        theta_array = self["theta_array"].value
        return simulate(theta_array*2, self._parmeters,
                        self._instrument, self._samlen)
