# -*- coding: utf8 -*-
"""
module for XRF simulator.

    :platform: Unix, Windows
    :synopsis: XRF simulation.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import numpy as np
import xraylib
import paf.data
import pyxcel.engine.simulator.generic
import pyxcel.engine.gixrf.el_field_no_genx as el_field
import pyxcel.engine.modeling.tools as tools
from pyxcel.engine.gixrf import SDDeff
from pyxcel.engine.gixrf.geom_factor import Detector_Collimator
from pyxcel.engine.gixrf.geom_factor import Exp_configuration
from pyxcel.engine.gixrf.geom_factor import GetGeometricCorrection
from pyxcel.engine.simulator.xrr_no_genx import resolve_parameter
MAKE_DATA = paf.data.make_data


def ResolutionVector(Q, dQ, points, range_=3):
    """ copy of genx resolution vector
    """
    Qstep = 2 * range_ * dQ / points
    Qres = Q + (np.arange(points)-(points-1)/2)[:, np.newaxis]*Qstep
    weight = (1/np.sqrt(2*np.pi)/dQ *
              np.exp(-(np.transpose(Q[:, np.newaxis])-Qres)**2/(dQ)**2/2))
    Qret = Qres.flatten()
    return (Qret, weight)


# Include the resolution with Qret and weight calculated from ResolutionVector
# and I the calculated intensity at each point. returns the intensity
def ConvoluteResolutionVector(Qret, I, weight):
    """ copy from GenX
    """
    Qret2 = Qret.reshape(weight.shape[0], weight.shape[1])
    I2 = I.reshape(weight.shape[0], weight.shape[1])
    norm_fact = np.trapz(weight, x=Qret2, axis=0)
    Int = np.trapz(I2*weight, x=Qret2, axis=0)/norm_fact
    return Int


class Line(paf.data.CompositeData):
    """ composite data to contain line and material
    """

    def __init__(self):
        """ initialization
        """
        value = {"line": "xraylib.LA1_LINE", "material": "Hf"}
        paf.data.CompositeData.__init__(self, value=value, abstract="line")


class XRFGenXSimulator(pyxcel.engine.simulator.generic.Simulator):
    """ simulator for XRF
    """
    geometric_calc = GetGeometricCorrection()

    def __init__(self, theta_array=None, stack=None, instrument=None):
        """ initialization
        """
        abstract = "simulator_XRF"
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
        """ initializing XRF simulation.

        :param filter_: filter using simulator
        """
        pyxcel.engine.simulator.generic.Simulator.initialization(self, filter_)
        self._parmeters = resolve_parameter(self["stack"])
        self._samlen = self["parameter"]["samplen"].value

        # load parameter
        self._detector = self["instrument"]['detector'].value
        self._theta_array = self["theta_array"].value
        self._instrument = self["instrument"]
        self._line = eval(self["parameter"]["line"]["line"].value)
        self._material = self["parameter"]["line"]["material"].value # first assignment to self.material, if corrupted, modify just after
        try:
            self._fit_inst = filter_.fit_inst
        except AttributeError:
            self._fit_inst = False

        # configure for ambient d = dist
        if not self._instrument["detector"]["void"].value:
            self.simulate = self.simulate_ambiant(self.simulate)

        # convolution
        self._theta_array_orig = self._theta_array
        twotheta_array = self._theta_array*2.
        range_ = self._instrument["detector"]["resintrange"].value
        res = self._instrument["detector"]["res"].value
        respoints = self._instrument["detector"]["respoints"].value
        (twoThetaQz, weight) = ResolutionVector(twotheta_array, res, respoints,
                                                range_)
        self._det_angle_array = 90.-twoThetaQz/2.
        self._twoThetaQz = twoThetaQz
        self._theta_array = self._twoThetaQz / 2
        self._weight = weight

        # load instrumental parameter
        self.calculate_inst()
        
        # extract genx parameter and create FluoYield object
        parameters = self._parmeters
        # cleans parameters['material'] from "_" characters introduced in material formula to indicate stoichiometry fitting
        for idx, each in enumerate(parameters['material']):
            parameters['material'][idx] = each.replace("_","")

        self._f_array = np.array(parameters['f'], dtype=np.complex64)
        energy = xraylib.LineEnergy(xraylib.
                                    SymbolToAtomicNumber(str(self._material)),
                                    self._line)
        self._det_efficiency = SDDeff.eff_sdd1_09_kw49([energy*1000.])
        self._my_fluo = self.create_my_fluo(parameters) # PARAMETERS CONTAINS UNCORRECTLY FORMATTED MATERIAL NAME WHEN STOCHIO SYNTAX "_" IS USED
        self._my_fluo.set_theta_array(self._theta_array)
        self._stack_name_list = list(self._parmeters['name'])

    def calculate_inst(self):
        """ calculate instrument correction
        """
        twotheta_array = self._theta_array_orig*2.
        range_ = self._instrument["detector"]["resintrange"].value
        res = self._instrument["detector"]["res"].value
        respoints = self._instrument["detector"]["respoints"].value
        (twoThetaQz, weight) = ResolutionVector(twotheta_array, res, respoints,
                                                range_)
        self._det_angle_array = 90.-twoThetaQz/2.
        self._twoThetaQz = twoThetaQz
        self._theta_array = self._twoThetaQz / 2
        self._weight = weight
        inst = self._instrument
        width_parallel_s = inst["detector"]["width_parallel_s"].value
        width_parallel_l = inst["detector"]["width_parallel_l"].value
        pinhole_height = inst["detector"]["pinhole_height"].value
        collimator = Detector_Collimator(width_parallel_s, width_parallel_l,
                                         pinhole_height)
        config = self["parameter"]["config"].value
        out_ang_deg = self._detector["det_angle_array"]
        exp_configuration = Exp_configuration(self._theta_array, out_ang_deg,
                                              inst["detector"]["dist"].value,
                                              scattering_angle_deg=None,
                                              collimator=collimator,
                                              configuration=config,
                                              bfwhm=inst["source"]["beamw"].
                                              value)
        self._geom = self.geometric_calc(self._samlen, exp_configuration,
                                         self._theta_array)

    def create_my_fluo(self, parameters):
        """ create my fluo object
        """
        wavelength = self._instrument["source"]["wavelength"].value
        dens = np.array(parameters['numerical_density'], dtype=np.float64)
        re = 2.8179403267e-5  # classical electron radius in Angstrom
        n_array = (1 - dens * re * wavelength**2 / 2 / np.pi * self._f_array)
        material_array = np.array(parameters['material'])
        for idx, each in enumerate(material_array):
            material_array[idx] = each.replace("_","")
        mass_dens_array = [tools.calc_mass_density(dens[lay_idx], mat) # edit material_array so that no "_" is in the array
                           for lay_idx, mat in enumerate(material_array)]
        return el_field.FluoYield(self._instrument, n_array, mass_dens_array,
                                  material_array)

    def simulate(self):
        """ simulate XRF.
        """
        # call parent function
        pyxcel.engine.simulator.generic.Simulator.simulate(self)

        # instrument fitting
        if self._fit_inst:
            self.calculate_inst()

        # load saved value
        # my_fluo = self._my_fluo
        line = self._line
        inc_flux = self._instrument["source"]["I0"].value
        theta_array = self._theta_array
        det_angle_array = self._detector["det_angle_array"]
        wavelength = self._instrument["source"]["wavelength"].value

        # load parameter
        parameters = self._parmeters
        
        for idx, each in enumerate(parameters['material']):
            parameters['material'][idx] = each.replace("_","")
            
        material_array = parameters['material']

        if self._fit_stochio:
            #print("fit stochio - pyxcel/engin/simulator/xrf_no_genx/XRFGenXSimulator.simulate")
            self._f_array = parameters['f']
        my_fluo = self.create_my_fluo(parameters)
        my_fluo.set_theta_array(self._theta_array)
        re = 2.8179403267e-5  # classical electron radius in Angstrom
        d_array = parameters['d']
        dens = parameters['numerical_density']
        n_array = (1 - dens * re * wavelength**2/2/np.pi*self._f_array)

        # calculate some value
        sigma_array = parameters['sigmar']
        mass_dens_array = parameters['mass_density']

        XRF_CS = el_field.calc_XRF_CS(self._material, line,
                                      tools.wavelength_to_in_energy(wavelength)
                                      )

        # calculate fluo
        elfield = el_field.ElField(theta_array, wavelength, n_array, d_array,
                                   sigma_array)
        my_fluo.set_elfield(elfield)
        fluo = my_fluo.fluo_int(det_angle_array-theta_array, n_array, d_array,
                                sigma_array, mass_dens_array, material_array,
                                self._material, line, XRF_CS)

        # instrumental correction
        fluo = el_field.fluo_quanti(fluo, inc_flux, self._geom,
                                    self._det_efficiency, theta_array)

        # convolution
        fluo = ConvoluteResolutionVector(self._twoThetaQz, fluo[:],
                                         self._weight)
        return fluo

    def simulate_ambiant(self, func):
        """ rewrite simulation for use ambiant
        """
        dist = self._instrument["detector"]["dist"].value
        self._parmeters["d"][-1] = dist * 1e8
        simu = func(self)
        self._parmeters["d"][-1] = 0
        return simu

    def simulate_stochio(self):
        """ doing the simulation with stochio.

        :rtype: np.array
        :return: result of the simulation.
        """
        for name, mat in self._mat.items():
            index = self._stack_name_list.index(name)
            self._parmeters["material"][index] = mat
#             print("pyxcel/engin/simulator/xrf_no_genx/XRFGenXSimulator.simulate_stochio, mat = "+mat+"\n")
#             print("!!!!!!!!!!!!!!!!!!!!!")
        return pyxcel.engine.simulator.generic.Simulator.simulate_stochio(self)
