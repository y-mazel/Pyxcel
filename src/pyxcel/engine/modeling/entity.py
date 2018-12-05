# -*- coding: utf8 -*-
"""
Implementation of class for describing model entity like stack...

    :platform: Unix, Windows
    :synopsis: Module for modeling an experiment.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta, abstractmethod
import re
import copy
import quantities as pq
import xraylib
import numpy as np
import pyxcel.engine.modeling.tools as tools
import paf.data
MAKE_DATA = paf.data.make_data


class PhysicalComputer(object):
    """ tool to calculate the structure factor and the index of refraction.
    """
    __metaclass__ = ABCMeta

    def __init__(self, wavelength=None, instrument=None, in_energy_eV=None):
        """ initialization

        :param wavelength: wavelength in Angstrom^(-1)
        :type wavelength: real
        :param instrument: instrument
        :param in_energy_eV: in_energy_eV
        """
        if wavelength is not None:
            self.wavelength = wavelength
        if instrument is not None:
            self.set_instrument(instrument)
        if in_energy_eV is not None:
            self._in_energy_eV = in_energy_eV

    @property
    def wavelength(self):
        """ property for accessing (and computing) wavelength.
        """
        return tools.in_energy_to_wavelength(self._in_energy_eV)

    @wavelength.setter
    def wavelength(self, wavelength):
        """ setter for the wavelength

        :param wavelength: wavelength in Angstrom^(-1)
        :type wavelength: real
        """
        self._in_energy_eV = tools.wavelength_to_in_energy(wavelength)

    @property
    def energy(self):
        """ property for energy
        """
        return self._in_energy_eV

    @energy.setter
    def energy(self, in_energy_eV):
        """ modify energy

        :param in_energy_eV: in_energy_eV
        """
        self._in_energy_eV = in_energy_eV

    def set_instrument(self, instrument):
        """ change energy by the energy in instrument
        """
        source = instrument["source"]
        wavelength = source["wavelength"].value
        self.wavelength = wavelength

    @abstractmethod
    def compute_f(self, material):
        """ compute structure factor
        """
        pass

    @abstractmethod
    def compute_n(self, material):
        """ compute index of refraction
        """
        pass


class NoneComputer(PhysicalComputer):
    """ don't compute anythings.
    """
    def compute_f(self, material):
        """ compute structure factor using genx
        """
        return None

    def compute_n(self, material):
        """ compute index of refraction using genx
        """
        return None


class XraylibPhysicalComputer(PhysicalComputer):
    """ tool to calculate the structure factor and the index of refraction
    using xraylib.
    """
    def compute_f(self, material):
        """ compute structure factor using xraylib

        :param material: material name
        :type material: str
        """
        f_xraylib = []
        in_energy_eV = self._in_energy_eV
        list_of_elements = tools.extract_elements(material)
        list_of_stoichios = tools.formula_to_stoichios_norm(material)
        mat_f_re = 0
        mat_f_im = 0
        for el_idx, el in enumerate(list_of_elements):
            # static structure factor can be calculated as an
            # Atomic_Factors(element,energy,q,DW)
            # where q is scattering vector: q = 0. for forward scattering
            # DW is a Debye-Waller factor: DW = 1.
            mat_f_re = (mat_f_re+list_of_stoichios[el_idx] *
                        np.sum(xraylib.
                               Atomic_Factors(xraylib.
                                              SymbolToAtomicNumber(el),
                                              in_energy_eV/1000., 0., 1.)
                               [0:2]))
            mat_f_im = (mat_f_im + list_of_stoichios[el_idx] * xraylib.
                        Atomic_Factors(xraylib.SymbolToAtomicNumber(el),
                                       in_energy_eV/1000., 0., 1.)[2])
        f_xraylib = np.append(f_xraylib, mat_f_re-1.0j*mat_f_im)
        return f_xraylib[0]

    def compute_n(self, material):
        """ compute index of refraction using xraylib
        """
        pass


class DensityTranslator(object):
    """ tool to transform numerical density to mass density
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def numeric_density(self, mass_density, chemical_formula):
        """ calculate numerical density from mass density

        :param mass_density: mass density
        :return: numeric density
        """
        pass

    @abstractmethod
    def mass_density(self, numeric_density, chemical_formula):
        """ calculate numerical density from mass density

        :param numeric_density: numeric density
        :return: mass density
        """
        pass


class PeriodicTableTranslator(DensityTranslator):
    """ Use periodic table to translate
    """
    def numeric_density(self, mass_density, chemical_formula):
        """ calculate numerical density from mass density

        :param mass_density: mass density
        :return: numeric density
        """
        return tools.calc_num_density(mass_density, chemical_formula)

    def mass_density(self, numeric_density, chemical_formula):
        """ calculate numerical density from mass density

        :param numeric_density: numeric density
        :return: mass density
        """
        return tools.calc_mass_density(numeric_density, chemical_formula)


class LayerData(paf.data.CompositeData):
    """ Class for modeling a layer.
    """

    #: name of the library using for unit converting and management
    unit_tools = "quantities"

    def __init__(self, material='', name='', numerical_density=0.,
                 mass_density=0., d=0., sigmar=0.,
                 density_translator=PeriodicTableTranslator()):
        """ initialization

        :param material: chemical formula (Xraylib format)
        :type material: str
        :param name: just a name for this layer
        :type name: str
        :param numerical_density: numerical density in atoms by Angstrom cube
        :type numercal_density: real
        :param mass_density: mass density grams per centimeter cube
        :type mass_density: real
        :param d: thickness in Angstrom
        :type d: real
        :param sigmar: sigma r roughness RMS
        :type sigmar: real
        :param density_translator: class contain algorithm for convert density
        :type density_translator: DensityTranslator
        :param f: structure factor
        :type f: complex
        :param n: index of refraction
        :type n: complex
        """
        if LayerData.unit_tools == "quantities":
            angstrom = pq.angstrom
        dic = {'material': material, 'name': name,
               'd': {'value': d, 'unit': angstrom},
               'sigmar': {'value': sigmar, 'unit': angstrom},
               'f': 0.j, 'n': 0.j}
        self._mass_density = MAKE_DATA(mass_density, pq.CompoundUnit("g/cm**3"))
        self._numeric_density = MAKE_DATA(numerical_density)
        dic["numerical_density"] = self._numeric_density
        dic["mass_density"] = self._mass_density
        self._density_translator = density_translator
        paf.data.CompositeData.__init__(self, dic, abstract="layer")
        self.showing_info = [("name", 'Name'), ("material", 'Material'),
                             ("d", "Thickness"), ("mass_density",
                                                  "Mass density"),
                             ("numerical_density", "Atomic density"),
                             ("sigmar", "Roughness")]

    @property
    def stochio(self):
        """ property to access to stochio value

        :return: default value of all stochio with mass density
        """
        stochio_find = re.findall("_[0-9.]*", self["material"].value)
        stochio = [float(pv[1:]) for pv in stochio_find]
        return stochio

    @property
    def density_translator(self):
        """ property for density translator
        """
        return self._density_translator

    def __setitem__(self, key, value):
        """ redefine set item for automatically calculate density
        """
        paf.data.CompositeData.__setitem__(self, key, value)
        translator = self._density_translator
        material = self["material"].value
        if key == "mass_density":
            numerical_density = translator.numeric_density(value, material)
            self._value["numerical_density"].value = numerical_density
        elif key == "numerical_density":
            mass_density = translator.mass_density(value, material)
            self._value["mass_density"].value = mass_density
        elif key == "material":
            mass_density = self._value["mass_density"].value
            numerical_density = translator.numeric_density(mass_density, value)
            self._value["numerical_density"].value = numerical_density

    def set_from_xml(self, xml_element):
        """ set from xml
        """
        paf.data.CompositeData.set_from_xml(self, xml_element)
        self._value["material"] = MAKE_DATA(str(self._value["material"].value))


class ProfileComputer(paf.data.CompositeData):
    """ computing part of profile function
    """
    def __init__(self, material="", kwargs={}):
        """ initialization
        """
        self._kwargs = kwargs
        self._elements_dict = None
        self._stochio = None
        value = {"material": material,
                 "kwargs": MAKE_DATA(self._kwargs, composite=True)}
        paf.data.CompositeData.__init__(self, value)

    def __call__(self, x):
        """ compute profil

        :param x: vector of value for slicing
        :type x: numpy.ndarray
        """
        concs = [0] + self._func(x).tolist()
        point = np.array([self._stochio * conc for conc in concs])
        r_m_1 = point[:-1]
        r_p_1 = point[1:]
        res = (r_m_1 + r_p_1)/2.
        return res

    @property
    def kwargs(self):
        """ access to kwargs
        """
        return self._kwargs

    @property
    def kwargs_list(self):
        """ return list of key for kwargs argument
        """
        return list(self["kwargs"].keys())

    @property
    def element_list(self):
        """ return list of element in material
        """
        if self._elements_dict is None:
            self.create_elements_list()
        return self._elements_dict

    @property
    def stochio(self):
        """ return value of stocchio
        """
        if self._stochio is None:
            self.create_elements_list()
        return self._stochio

    def create_elements_list(self):
        """ create dictyonnarie of element
        """
        self._elements_dict = tools.extract_elements(self["material"].value)
        self._stochio = tools.formula_to_stoichios(self["material"].value)


class ProfileConc(paf.data.CompositeData):
    """ Represente a function for concentration profil
    """
    def __init__(self):
        """ initilization
        """
        dic = {'computers': []}
        paf.data.CompositeData.__init__(self, dic, abstract="profil_func")
        self._elements_dict = None
        self._listifier = []
        self._els = []

    def __call__(self, x):
        """ compute profil

        :param nb_sub: number of subdivising
        :type nb_sub: int
        """
        concs = [computer(x) for computer in self["computers"]]
        total_stoichio = []
        for el in self._listifier:
            sto = 0
            for x, y in el:
                sto += concs[x][:, y]
            total_stoichio.append(sto)
        total_stoichio = np.array(total_stoichio).T
        total_stoichio = [stoichio/np.sum(stoichio)
                          for stoichio in total_stoichio]
        result = []
        for layer in total_stoichio:
            line = ""
            for idx, sto in enumerate(layer):
                res = "{:f}".format(sto)
                if sto <= 0.000001:
                    res = '0.000001'
                line += self._els[idx] + res
            result.append(line)
        return result

    def add_computer(self, computer):
        """ add a new profile computer
        """
        self['computers'].append(computer)

    def remove_computer(self, index):
        """ remove coputer at  selected index

        :param index: index of computer to remove
        :type index: int
        """
        del self['computers'][index]

    def change_computer(self, index, value):
        """ change computer at index
        """
        self["computers"][index] = value

    def create_listifier(self):
        """ create structure to know how create final structure
        """
        self._els = []
        self._listifier = []
        element_lists = []
        for computer in self["computers"]:
            computer.create_elements_list()
            element_lists.append(computer.element_list)
        for idx1, element_list in enumerate(element_lists):
            for idx2, el in enumerate(element_list):
                if el in self._els:
                    el_index = self._els.index(el)
                    self._listifier[el_index].append((idx1, idx2))
                else:
                    self._els.append(el)
                    self._listifier.append([(idx1, idx2)])
        return self._listifier


class DensityProfile(paf.data.CompositeData):
    """ class for describing a density profile
    """
    def __init__(self, kwargs={}, type_='num'):
        """ initialization

        :param kwargs: key word arguments for density profile
        :type kwargs: dict
        :param type_: type of density describe by the profile *num or mass*
        :type type_: str
        """
        dic = {"type": type_}
        dic.update(kwargs)
        paf.data.CompositeData.__init__(self, dic, abstract="profil_func")

    def __call__(self, x):
        """ compute profil

        :param nb_sub: number of subdivising
        :type nb_sub: int
        """
        return [0] * len(x)


class LayerProfileData(LayerData):
    """ Layer data with concentration profile
    """
    def __init__(self, name='', numerical_density=0., mass_density=0., d=10.,
                 sigmar=0., step_size=.1, x=None, nb_lay=None):
        """ initialization

        :param name: name of layer
        :type name: str
        :param d: depth
        :type d: float
        :param sigmar: sigma r roughness RMS
        :type sigmar: float
        """
        LayerData.__init__(self, "", name, numerical_density,
                           mass_density, d, sigmar)
        d_layer = self["d"].value
        self._profil_func = ProfileConc()
        self._value["materials"] = self._profil_func
        self._value["densities"] = DensityProfile()
        self._value["linespace"] = MAKE_DATA(x is None)
        if x is None:
            if nb_lay is not None:
                step_size = d_layer * nb_lay
            x = np.linspace(0, d_layer, int(d_layer/step_size)+1)
            x = x[1:]
            self._value["step_size"] = MAKE_DATA(step_size)
        else:
            self._value["step_size"] = MAKE_DATA(None)
        self._x = x
        self._value["x"] = MAKE_DATA(self._x)
        self._phy_cmp = None
        self._old_d = d_layer
        self._d = None
        self.cmp_d()

    def __setitem__(self, key, value):
        """ overide for setting self._x in same time of self["x"]
        """
        LayerData.__setitem__(self, key, value)
        if key == "x":
            if isinstance(value, paf.data.Data):
                value = value.value
            self._x = value
        elif key == "d":
            if isinstance(value, paf.data.Data):
                value = value.value
            self._old_d = value
            if self["linespace"].value:
                self['x'] = np.linspace(0, self["d"].value,
                                        int(self["d"].value / self["step_size"]
                                            .value))[1:]
            self.cmp_d()

    @property
    def nb_lay(self):
        """ access to number of layer
        """
        return len(self._x)

    @nb_lay.setter
    def nb_lay(self, value):
        """ set number of layer
        """
        self["x"] = np.linspace(0, self["d"].value, value+1)[1:]
        self["step_size"] = len(self._x)

    @staticmethod
    def creat_from_layer(layer_data):
        """ create layer profile from a layer
        """
        new_layer_profile = LayerProfileData(d=layer_data["d"].value)
        new_layer_profile["name"] = layer_data["name"]
        new_layer_profile["sigmar"] = layer_data["sigmar"]
        return new_layer_profile

    @property
    def x(self):
        """ accessing to slicing vector
        """
        return self._x

    @x.setter
    def x(self, value):
        """ setter for slicing vector
        """
        self._x = value
        self["x"] = value

    @property
    def phy_cmp(self):
        """ access to physical computer
        """
        return self._phy_cmp

    @phy_cmp.setter
    def phy_cmp(self, value):
        """ set physical computer
        """
        self._phy_cmp = value

    @property
    def d(self):
        """ accessing to depth
        """
        self.cmp_d()
        return self._d

    @d.setter
    def d(self, value):
        """ set new d value
        """
        if isinstance(value, paf.data.Data):
            value = value.value
        self._value["d"] = MAKE_DATA(value)
        norm_x = self._x / self._old_d
        self["x"] = norm_x * value
        self._old_d = value
        self.cmp_d()

    def cmp_d(self):
        """ compute depths
        """
        self._d = self._x - np.array([0] + list(self._x[:-1]))

    def finish_copy(self):
        """ initialize self._x at the end of the copy
        """
        self._x = self["x"].value
        self.cmp_d()
        self._old_d = self["d"].value

    def add_computer(self, computer):
        """ add a new profile computer to prfile
        """
        self['materials'].add_computer(computer)

    def remove_computer(self, index):
        """ remove coputer at  selected index

        :param index: index of computer to remove
        :type index: int
        """
        self['materials'].remove_computer(index)

    def change_computer(self, index, value):
        """ change computer at index
        """
        self['materials'].change_computer(index, value)

    def element_conc(self):
        """ return dictionnary with for each element in key give numpy array
        of concentration in each sublayers
        """
        materials = self["materials"](self._x)
        materials_dict = {key: [tools.formula_to_stoichios(formula)[idx]
                                for formula in materials]
                          for idx, key in
                          enumerate(tools.extract_elements(materials[0]))}
        for key, mat in materials_dict.items():
            materials_dict[key] = np.array(mat)
        return materials_dict

    def to_stack(self):
        """ return stack representing current layer
        """
        materials = self["materials"](self._x)
        densities = self["densities"](self._x)
        res = []
        for idx, mat in enumerate(materials):
            name = self["name"].value
            sigmar = 0.
            if idx == 0:
                sigmar = self["sigmar"].value
                name += "_start"
            elif idx+1 == len(materials):
                name += "_end"
            else:
                name += "_" + str(idx)
            new_layer = LayerData(material=mat, name=name,
                                  numerical_density=densities[idx],
                                  d=self._d[idx], sigmar=sigmar)
            if self.phy_cmp is not None:
                new_layer['f'] = self._phy_cmp.compute_f(new_layer['material'])
            res.append(new_layer)
        return res

    def to_one_layer(self):
        """ recreate a layre
        """
        x = np.array([self["d"].value])
        material = self["materials"](x)[0]
        density = self["densities"](x)[0]
        new_layer = LayerData(material=material, name=self["name"].value,
                              numerical_density=density,
                              d=self["d"].value, sigmar=self["sigmar"].value)
        return new_layer

    def to_param(self):
        """ return a dictionnary with key "material" and "mass_density" or
        "numeric_density" (depend on type fo profile density)
        """
        materials = self["materials"](self._x)
        if self["densities"]["type"].value == "num":
            num_densities = self["densities"](self._x)
            mass_densities = [tools.calc_mass_density(num_density,
                                                      materials[idx])
                              for idx, num_density in enumerate(num_densities)]
            mass_densities = np.array(mass_densities)
        else:
            mass_densities = self["densities"](self._x)
            num_densities = [tools.calc_num_density(num_density,
                                                    materials[idx])
                             for idx, num_density in enumerate(num_densities)]
            num_densities = np.array(num_densities)
        return {"d": self._d, "materials": materials,
                "num_densities": num_densities,
                "mass_densities": mass_densities}


class SourceData(paf.data.CompositeData):
    """ abstract class for mark data as a source.
    """
    __metaclass__ = ABCMeta


class XRaySourceData(SourceData):
    """ Class for modeling an XRay source.
    """
    def __init__(self, coords='tth', footype=2, wavelength=1., beamw=0.01,
                 I0=1., in_energy=1.):
        """ initialization

        :param coords: (tth or qz)
        :type coords: str
        :param footype: footprint type
        :type footype: integer
        :param wavelength: wavelength in Angstrom^(-1)
        :type wavelength: real
        :param beamw: beam width in mm
        :type beamw: real
        :param I0: incident beam intensity
        :type I0: real
        """
        dic = {'footype': footype, 'beamw': {"value": beamw, "unit": pq.mm},
               'wavelength': {"value": wavelength, "unit": pq.angstrom},
               'coords': coords, 'I0': I0, "in_energy": {"value": in_energy,
                                                         "unit": pq.eV}}
        paf.data.CompositeData.__init__(self, dic, abstract="XRaySource")
        self.showing_info = [("wavelength", "Wavelength"),
                             ("in_energy", "Energy"), ("I0", "I0"),
                             ("beamw", "Beam size"),
                             ("footype", "Beam shape")]

    def __setitem__(self, key, value):
        """ for modification wavelength
        """
        paf.data.CompositeData.__setitem__(self, key, value)
        if key == "wavelength":
            SourceData.__setitem__(self, "in_energy",
                                   tools.wavelength_to_in_energy(value))
        if key == "in_energy":
            SourceData.__setitem__(self, "wavelength",
                                   tools.in_energy_to_wavelength(value))


class DetectorData(paf.data.CompositeData):
    """ abstract class for mark data as a detector.
    """
    __metaclass__ = ABCMeta


class XRRDetectorData(DetectorData):
    def __init__(self, res=0.0001, respoints=5, Ibkg=0., restype=2,
                 resintrange=2, taylor_n=1.):
        """ initialization

        :param res: angular resolution in degrees
        :type res: real
        :param respoints: number of resolution points for convolution
        :type respoints: integer
        :param Ibkg: background signal intensity
        :type Ibkg: real
        :param restype: resolution convolution type
        :type restype: integer
        :param resintrange: range for resolution in convolution
        :type resintrange: integer
        :param taylor_n: degree of Taylor expansion
        :type taylor_n: integer
        """
        dic = {'res': {"value": res, "unit": pq.deg}, 'respoints': respoints,
               'Ibkg': Ibkg, 'restype': restype, 'resintrange': resintrange,
               'taylor_n': taylor_n}
        paf.data.CompositeData.__init__(self, dic, abstract="XRRDetector")
        self.showing_info = [("restype", 'Resolution convolution type'),
                             ("res", "Instrumental resolution"),
                             ("resintrange", "Number of standard deviations to integrate the resolution function"), 
                             ("respoints", "Number of points to include in the resolution calculation"), 
                             ("taylor_n", "Degree of the Taylor expansion used for the correlation function"), 
                             ("Ibkg", "Background intensity")]

class XRFDetectorData(DetectorData):
    def __init__(self, res=0.0005, dist=0., det_angle_array=90., resintrange=2,
                 respoints=5, restype=2, taylor_n=1., width_parallel_s=0.5,
                 width_parallel_l=0.5, pinhole_height=0.5):
        """ initialization

        :param dist: distance from sample to XRF detector window in cm
        :type dist: real
        :param inc_angle_array: array of incidence angle (theta_deg)
        :type inc_angle_array: np.array
        :param width_parallel_s: first colimator window close to the detector
        :type width_parallel_s: real
        :param width_parallel_l: seconde colimator window far to the detector
        :type width_parallel_l: real
        :param pinhole_height: colimator lenth
        :type pinhole_height: real
        """
        dic = {'res': {"value": res, "unit": pq.deg}, 'respoints': respoints,
               'restype': restype, 'taylor_n': taylor_n,
               'dist': {"value": dist, "unit": pq.cm},
               'width_parallel_s': {"value": width_parallel_s, "unit": pq.cm},
               'width_parallel_l': {"value": width_parallel_l, "unit": pq.cm},
               'pinhole_height': {"value": pinhole_height, "unit": pq.cm},
               'det_angle_array': det_angle_array, 'resintrange': resintrange,
               "void": True}
        paf.data.CompositeData.__init__(self, dic, abstract="XRFDetector")


class InstrumentData(paf.data.CompositeData):
    def __init__(self, source=None, detector=None, type_instrument=""):
        """ initialization

        :param source: data for the source
        :type source: SourceData
        :param detector: data for the detector
        :type detector: DetectorData
        :param type_instrument: name for instrument type
        :type type_instrument: str
        """
        dic = {'source': source, 'detector': detector, 'name': 'inst'}
        paf.data.CompositeData.__init__(self, dic, abstract=type_instrument +
                                        "Instrument")


class SubStack(paf.data.CompositeData):
    """ class to represent list of layers
    """
    def __init__(self, start=0, stop=1, repetition=1):
        """ initialization
        """
        dic = {"repetition": repetition, "start": start, "stop": stop}
        paf.data.CompositeData.__init__(self, value=dic, abstract="stack")


class StackData(paf.data.CompositeData):
    """ Class for modeling a sample.
    """
    def __init__(self, name="", ambient=None, substrate=None, layers=None,
                 order=None, physical_computer_type=XraylibPhysicalComputer):
        """ initialization

        :param ambient: ambient
        :type ambient: Layer
        :param substrate: substrate
        :type substrate: Layer
        :param layers: list of all possible layers
        :type layers: list
        """
        if isinstance(order, list):
            temp = []
            for layer_name in order:
                temp.append(copy.deepcopy(layers[layer_name]))
            layers = temp
        dic = {"repetition": []}
        self._physical_computer_type = physical_computer_type
        self._physical_computer = None
        paf.data.CompositeData.__init__(self, value=dic, abstract="stack")
        if ambient is not None:
            self._value["ambient"] = ambient
            self._value["layers"] = MAKE_DATA(layers)
            self._value["substrate"] = substrate
            self._value["name"] = MAKE_DATA(name)

    def __getitem__(self, key):
        """ new getitem for adding repetition in layers
        """
        if key == "layers":
            layers = self._value["layers"].real_value
            starts = []
            in_sub = []
            stops = []
            for sub in self["repetition"]:
                starts.append(sub["start"].value)
                stops.append(sub["stop"].value)
                in_sub += range(sub["start"].value, sub["stop"].value)
            result = []
            for index, layer in enumerate(layers):
                if index in starts:
                    index_in_rep = starts.index(index)
                    repetition = (self["repetition"][index_in_rep]
                                  ["repetition"].value)
                    sub = layers[starts[index_in_rep]:stops[index_in_rep]]
                    result += sub * repetition
                elif index in in_sub:
                    pass
                elif isinstance(layer, LayerProfileData):
                    layer["materials"].create_listifier()
                    result += layer.to_stack()
                else:
                    result.append(layer)
            return MAKE_DATA(result)
        return paf.data.CompositeData.__getitem__(self, key)

    def del_substack(self, index):
        """ del repetition for the index
        """
        rep_range = [range(sub["start"].value, sub["stop"].value)
                     for sub in self["repetition"]]
        for current_index, range_ in enumerate(rep_range):
            if index in range_:
                del self["repetition"][current_index]

    def create_substack(self, start, stop, repetition):
        """ transform layer start to stop in a sublayer
        """
        stop += 1
        for index in range(start, stop):
            self.del_substack(index)
        if repetition != 1:
            self["repetition"].append(SubStack(start, stop, repetition))

    def set_from_xml(self, xml_element):
        paf.data.CompositeData.set_from_xml(self, xml_element)
        if isinstance(self["repetition"], paf.data.SimpleData):
            self["repetition"] = []

    def apply_rep(self, index):
        """ apply repetition starting at index
        """
        def copy_lays(lays):
            """ copy layer stack
            """
            return [paf.data.copy_data(lay) for lay in lays]
        layers = self._value["layers"].real_value
        sub = self["repetition"][index]
        start = sub["start"].value
        in_sub = range(sub["start"].value, sub["stop"].value)
        stop = sub["stop"].value
        result = []
        repetition = (sub["repetition"].value)
        for current, layer in enumerate(layers):
            if current == start:
                sub = layers[start:stop]
                for sufix in range(repetition):
                    new_lays = copy_lays(sub)
                    for lay in new_lays:
                        lay["name"] = lay["name"].value + "_" + str(sufix)
                    result += new_lays
            elif current in in_sub:
                pass
            else:
                result.append(layer)
        del self["repetition"][index]
        for rep in self["repetition"]:
            if rep["start"].value > start:
                diff = (stop - start) * (repetition - 1)
                rep["start"] = rep["start"].value + diff
                rep["stop"] = rep["stop"].value + diff
        self._value["layers"] = MAKE_DATA(result)

    @property
    def density_translator(self):
        """ property for density translator access
        """
        return self["ambient"].density_translator

    @property
    def physical_computer_type(self):
        """ property to access to physical computer type
        """
        return self._physical_computer_type

    @physical_computer_type.setter
    def physical_computer_type(self, value):
        """ setter for physical computer type
        """
        self._physical_computer_type = value
        if self._physical_computer is not None:
            self._physical_computer = self._physical_computer_type()

    @property
    def physical_computer(self):
        """ property to access physical computer
        """
        if self._physical_computer is None:
            self._physical_computer = self._physical_computer_type()
        return self._physical_computer

    @property
    def wavelength(self):
        """ property to change wavelength
        """
        if self._physical_computer is None:
            return 0
        else:
            return self._physical_computer.wavelength

    @wavelength.setter
    def wavelength(self, wavelength):
        """ setter for wavelength property
        """
        phy_comp = self.physical_computer
        phy_comp.wavelength = wavelength
        for layer in self._value["layers"]:
            if isinstance(layer, LayerProfileData):
                layer.phy_cmp = phy_comp
            else:
                f = phy_comp.compute_f(layer['material'])
                layer['f'] = f
        self["substrate"]['f'] = (self._physical_computer.
                                  compute_f(self["substrate"]['material']))
        self["ambient"]['f'] = (self._physical_computer.
                                compute_f(self["ambient"]['material']))

    @property
    def stochio(self):
        """ property to create a dict of all layer stochio
        """
        stochio = {}
        for layer in self["layers"]:
            layer_stochio = layer.stochio
            if len(layer_stochio) >= 1:
                stochio["stochio_" + layer["name"].value] = layer_stochio
        return stochio
