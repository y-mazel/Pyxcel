# -*- coding: utf8 -*-
"""
Contain the configuration element.

    :platform: Unix, Windows
    :synopsis: centralizer

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import os.path
import numpy as np
import operation.simulation_xsw
import paf.data
import directory
import operation.basic_simulation as basic_sim
import operation.combined
import operation.data_treatement
import pyxcel.engine.simulation.generic as simu
import pyxcel.engine.modeling.physical_parameter as phyp
import pyxcel.engine.simulator.xrf_no_genx as xrf
import pyxcel.engine.simulator.xrr_no_genx as xrr
import pyxcel.engine.optimization.fom as fom
import pyxcel.engine.modeling.profile as profile
import pyxcel.view.widget.tools.xrf_tools as xrf_tools

from pyxcel.view.cute import QLocale, QTranslator
MAKE_DATA = paf.data.make_data


registered_operations = {"scipy combiner":
                         operation.combined.create_combine_scipy,
                         "simulation XSW":
                         operation.simulation_xsw.simulation_xsw_build,
                         "inspyred combiner":
                         operation.combined.create_combine_inspyred,
                         "inspyred NSGA2 combiner":
                         operation.combined.create_combine_inspyred_mo
                         }

data_treatment = {"select_window": operation.data_treatement.select_windows}

default_order = ["simulation XSW", "inspyred combiner", "scipy combiner",
                 "inspyred NSGA2 combiner"]

FOM_DICT = {"d_log2": fom.log2d, "g_chi2bars": fom.chi2bars,
            "d_theta_4": fom.theta4, "b_logarithmic": fom.b_logarithmic,
            "b_normalized_logarithmic": fom.b_normalized_logarithmic,
            "b_normalized": fom.b_normalized, "b_standart": fom.b_standart,
            "b_log_module": fom.b_log_module, "d_chi2": fom.chi2d}

PROFILE_DICT = {"gaussian_interface": profile.GaussianInterface,
                "gaussian": profile.Gaussian,
                "anti_gaussian_interface":
                profile.AntiGaussianInterface,
                "anti_gaussian": profile.AntiGaussian}

PROFILE_DENS_DICT = {"lineaire": profile.LinearDensityProfile}

TOOLS_DICT = {"XFR tools": xrf_tools.XrfTools}


class Options(paf.data.CompositeData):
    """ object in charge of option support
    """

    def __init__(self):
        """ initialization
        """
        self._basic_simulator = {}
        i18n_directory = os.path.join(directory.get_base_dir(), "i18n")
        self._translator = QTranslator()
        value = {"default_sample_len": 50,
                 "default_operation": registered_operations,
                 "default_operation_order": default_order,
                 "fom_dict": FOM_DICT, "max_len": 80,
                 "pop_size": 200, "max_gen": 60,
                 "i18n_directory": i18n_directory, "composite_auto": True,
                 "local": QLocale.system().name(), "ui_dir": "",
                 "data_treatment": data_treatment, "doc_dir": "",
                 "profile_dict": PROFILE_DICT, "tools_dict": TOOLS_DICT,
                 "profile_dens_dict": PROFILE_DENS_DICT}
        paf.data.CompositeData.__init__(self, value)
        self.local = self.local

    @property
    def profile_dens_dict(self):
        """ return density profile dictionnary
        """
        return self["profile_dens_dict"].value

    @property
    def tools_dict(self):
        """ return dictionnary of tools wi
        """
        return self["tools_dict"].value

    @property
    def profile_list(self):
        """ return list of profile sorted
        """
        return sorted(list(self.profile_dict.keys()))

    @property
    def profile_dict(self):
        """ access to profile dictionnary.
        """
        return self["profile_dict"].value

    @property
    def data_treatment(self):
        """ directory containing all localisation files
        """
        return self["data_treatment"].value

    @data_treatment.setter
    def data_treatment(self, value):
        """ directory containing all localisation files
        """
        self["data_treatment"] = value

    @property
    def i18n_directory(self):
        """ directory containing all localisation files
        """
        return self["i18n_directory"].value

    @i18n_directory.setter
    def i18n_directory(self, value):
        """ directory containing all localisation files
        """
        self["i18n_directory"] = value

    @property
    def fom_dict(self):
        """ access to fom dictionnary
        """
        return self["fom_dict"].value

    @fom_dict.setter
    def fom_dict(self, value):
        """ setter for fom dictionnary
        """
        self["fom_dict"] = value

    @property
    def composite_auto(self):
        """ access to composite auto validate option
        """
        return self["composite_auto"].value

    @composite_auto.setter
    def composite_auto(self, value):
        """ setter for composite auto validate option
        """
        self["composite_auto"] = value

    @property
    def ui_dir(self):
        """ access to ui directory
        """
        return self["ui_dir"].value

    @ui_dir.setter
    def ui_dir(self, value):
        """ setter for ui directory
        """
        self["ui_dir"] = value

    @property
    def doc_dir(self):
        """ access to ui directory
        """
        return self["doc_dir"].value

    @doc_dir.setter
    def doc_dir(self, value):
        """ setter for ui directory
        """
        self["doc_dir"] = value

    @property
    def default_max_gen(self):
        """ accessing to default max_gen value
        """
        return self["max_gen"].value

    @property
    def default_pop_size(self):
        """ accessing to default pop_size value
        """
        return self["pop_size"].value

    @property
    def max_len(self):
        """ accessing to the max len of a line
        """
        return self["max_len"].value

    @property
    def default_operation(self):
        """ accessing to list of default operation
        """
        return self["default_operation"].value

    @property
    def default_operation_order(self):
        """ accessing to list of default operation order
        """
        return self["default_operation_order"].value

    @property
    def local(self):
        """ access to local name
        """
        return self["local"].value

    @local.setter
    def local(self, value):
        """ set a new value to local
        """
        self["local"] = value
        self._translator.load(value + ".qm", self.i18n_directory)

    @property
    def translator(self):
        """ accessing to translator
        """
        return self._translator

    def get_operation(self, name):
        """ get an operation if is accessible. Create it if not.
        """
        try:
            return self._basic_simulator[name]
        except KeyError:
            self._create_basic_simulator(name)
            return self._basic_simulator[name]

    def set_from_xml(self, xml_element):
        paf.data.CompositeData.set_from_xml(self, xml_element)
        self.local = self["local"].value

    def _create_basic_simulator(self, name):
        """ create a basic simulator for each simulator.
        """
        if name == "XRR":
            simulator = simu.GenericGenXSimulatorFilter()
            simulator["parameter"] = MAKE_DATA({"samplen": 50}, composite=True)
            simulator["simulator"] = xrr.XRRGenXSimulator()
            model_creator = phyp.ApplyPhysicalParameter()
            pipeline = basic_sim.basic_simulator_build(simulator,
                                                       model_creator)
        elif name == "XRF":
            simulator = simu.GenericGenXSimulatorFilter()
            value = {'config': 'theta-2theta', "line": xrf.Line(),
                     "samplen": 50}

            simulator["parameter"] = MAKE_DATA(value, composite=True)
            simulator["theta_array"] = MAKE_DATA(np.linspace(0.01, 7.5, 100))
            simulator["simulator"] = xrf.XRFGenXSimulator()
            model_creator = phyp.ApplyPhysicalParameter()
            pipeline = basic_sim.basic_simulator_build(simulator,
                                                       model_creator)
        self._basic_simulator[name] = pipeline
