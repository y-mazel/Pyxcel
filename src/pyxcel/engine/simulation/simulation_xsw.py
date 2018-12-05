# -*- coding: utf8 -*-
"""
The simulator for XSW only.

    :platform: Unix, Windows
    :synopsis: XRR simulation using GenX.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import numpy as np
from pyxcel.engine.simulator.xrr_no_genx import resolve_parameter
from pyxcel.engine.gixrf import el_field_no_genx
import paf.filter_base as filters
import paf.data as data
import paf.port as port
MAKE_DATA = data.make_data


class resultat_XSW(data.CompositeData):
    """ result of XSW simulation
    """
    def __init__(self, xsw=None, theta_array=None, z_array=None,
                 z_interface=None):
        """ initialization
        """
        value = {"XSW": xsw, "theta_array": theta_array, "z_array": z_array,
                 "z_interface": z_interface}
        data.CompositeData.__init__(self, value, "data_XSW")


class GenXSWFSimFilter(filters.Filter):
    """ filter to simulate XSW
    """
    def __init__(self):
        """ initialization
        """
        filters.Filter.__init__(self)
        temp_port = port.Port(MAKE_DATA())
        self.input_port["instrument"] = temp_port
        self.add_expected_parameter("start_theta", MAKE_DATA(0.),
                                    MAKE_DATA(.01))
        self.add_expected_parameter("end_theta", MAKE_DATA(0.), MAKE_DATA(1.))
        self.add_expected_parameter("nb_of_point", MAKE_DATA(0),
                                    MAKE_DATA(100))
        self.add_expected_parameter("dz", MAKE_DATA(0.), MAKE_DATA(.1))
        temp_port = port.Port(MAKE_DATA(np.array([0])))
        self.output_port["theta_array"] = temp_port
        temp_port = port.Port(MAKE_DATA(np.array([0])))
        self.output_port["z_array"] = temp_port
        temp_port = port.Port(MAKE_DATA(np.array([0])))
        self.output_port["z_interface"] = temp_port
        temp_port = port.Port(resultat_XSW())
        self.output_port["XSW"] = temp_port

    def run(self):
        """ running
        """
        wavelength = self.get_data("instrument")["source"]["wavelength"].value
        parameters = resolve_parameter(self.get_data("main"))
        dens = np.array(parameters['numerical_density'], dtype=np.float64)
        f_array = np.array(parameters['f'], dtype=np.complex64)
        re = 2.8179403267e-5  # classical electron radius in Angstrom
        n_array = 1 - dens * re * wavelength**2/2/np.pi*f_array
        d_array = np.array(parameters['d'], dtype=np.float64)
        sigma_array = np.array(parameters['sigmar'], dtype=np.float64)
        start_theta = self["start_theta"].value
        end_theta = self["end_theta"].value
        nb_of_point = self["nb_of_point"].value
        theta_array = np.array(np.linspace(start_theta, end_theta,
                                           nb_of_point))
        genx_elfield = el_field_no_genx.ElField(theta_array, wavelength,
                                                n_array, d_array, sigma_array)
        genx_elfield.calcul_Ej(wavelength, d_array, dz=self["dz"].value)
        XSW = genx_elfield.el_field_int()
        self.fill_port("main", MAKE_DATA(XSW))
        self.fill_port("theta_array", MAKE_DATA(theta_array))
        self.fill_port("z_array", MAKE_DATA(genx_elfield.z_array))
        self.fill_port("z_interface", MAKE_DATA(genx_elfield.z_interface))
        self.fill_port("XSW", resultat_XSW(XSW, theta_array,
                                           genx_elfield.z_array,
                                           genx_elfield.z_interface))
