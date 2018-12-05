"""
Created on 17 nov. 2015

@author: GPICOT00
"""
from models.utils import fp
import numpy as np
from pyxcel.engine.modeling.tools import in_energy_to_wavelength
from pyxcel.engine.modeling.tools import extract_elements
from pyxcel.engine.modeling.tools import formula_to_stoichios_norm


def calc_f_from_genx(materials, in_energy_eV):
    """ function to retrieve scattering factors from genx (fp utilities)
    input: list with material names
    """
    fp.set_wavelength(in_energy_to_wavelength(in_energy_eV))
    f_genx = np.zeros(np.size(materials), dtype=np.complex64)
    for lay_idx, material in enumerate(materials):
        list_of_elements = extract_elements(material)
        list_of_stoichios = formula_to_stoichios_norm(material)
        mat_f = 0j
        for el_idx, el in enumerate(list_of_elements):
            mat_f = mat_f+list_of_stoichios[el_idx]*eval('fp.'+el)
        f_genx[lay_idx] = mat_f
    return f_genx


def calc_f_from_genx_wavelength(materials, wavelength):
    """ function to retrieve scattering factors from genx (fp utilities)
    input: list with material names
    """
    fp.set_wavelength(wavelength)
    f_genx = np.zeros(np.size(materials), dtype=np.complex64)
    for lay_idx, material in enumerate(materials):
        list_of_elements = extract_elements(material)
        list_of_stoichios = formula_to_stoichios_norm(material)
        mat_f = 0j
        for el_idx, el in enumerate(list_of_elements):
            mat_f = mat_f+list_of_stoichios[el_idx]*eval('fp.'+el)
        f_genx[lay_idx] = mat_f
    return f_genx
