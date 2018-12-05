# -*- coding: utf8 -*-
"""
Implementation of tools function and class.

    :platform: Unix, Windows
    :synopsis: Module for modeling an experiment.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import xraylib
import numpy as np
import periodictable
import paf.data

Avogadro_const = 6.02214129e23  # [mol=1]

el_q = 1.602176462E-19  # C
h_J = 6.62606876E-34  # s
speed_of_light = 2.99792458E+10  # cm/s

lambda_to_energy = (h_J/el_q)*speed_of_light  # for E to lambda conversion


def normalize(chem_formula):
    """ return normalized chemical formula
    """
    stoichios = formula_to_stoichios_norm(chem_formula)
    result = ""
    for idx, element in enumerate(extract_elements(chem_formula)):
        res = "{:f}".format(stoichios[idx])
        if stoichios[idx] <= 0.000001:
                res = '0.000001'
        result += element + res
    return result


def calc_num_density(mass_dens, chem_formula):
    """ transforms from mass density to atomic (number) density
    get natural abundance molecular mass from periodictable
    """
    chem_formula = normalize(clear_marker(chem_formula))
    try:
        molar_mass = periodictable.formula(chem_formula).mass
    except KeyError:
        # bug of periodic table library
        return calc_num_density(mass_dens, chem_formula)
    num_dens = mass_dens*1e-24*Avogadro_const/molar_mass
    return num_dens  # [g/cm3]


def calc_mass_density(atomic_dens, chem_formula):
    """ transforms from atomic (number) density to mass density
    get natural abundance molecular mass from periodictable
    """
    chem_formula = normalize(clear_marker(chem_formula))
    try:
        molar_mass = periodictable.formula(chem_formula).mass
    except KeyError:
        # bug of periodic table library
        return calc_mass_density(atomic_dens, chem_formula)
    mass_dens = atomic_dens*molar_mass*1e24/Avogadro_const
    return mass_dens  # [g/cm3]


def formula_to_stoichios(chemical_formula):
    """ uses xraylib and its CompoundParser
    """
    chemical_formula = clear_marker(chemical_formula)
    my_elements = xraylib.CompoundParser(chemical_formula)
#     print my_elements
    element = zip(my_elements['Elements'], my_elements['massFractions'])
    zz = sum([m/xraylib.AtomicWeight(Z) for Z, m in element])
    stoichios = [my_elements['nAtomsAll'] * m / xraylib.AtomicWeight(Z)/zz
                 for Z, m in element]
    return np.array(stoichios)

def extract_elements(chemical_formula):
    """ uses xraylib and its CompoundParser
    """
    chemical_formula = clear_marker(chemical_formula)
    my_elements = xraylib.CompoundParser(chemical_formula)
    elements_list = [xraylib.AtomicNumberToSymbol(e)
                     for e in my_elements['Elements']]
    return np.array(elements_list)


def in_energy_to_wavelength(in_energy_eV):
    """ gives wavelength (in Angstrom)
    """
    wavelength = lambda_to_energy / in_energy_eV  # in cm
    wavelength = wavelength * 1e8  # in Angstrom
    return wavelength


def wavelength_to_in_energy(wavelength):
    """ gives wavelength (in Angstrom)
    """
    in_energy_eV = wavelength / 1e8  # in Angstrom
    in_energy_eV = lambda_to_energy / in_energy_eV  # in cm
    return in_energy_eV


def clear_marker(material):
    """ clear _ in chemical formula
    """
    if isinstance(material, paf.data.Data):
        return material.value.replace("_", "")
    else:
        material = str(material)
        return material.replace("_", "")


def formula_to_stoichios_norm(chemical_formula):
    """ return normalized stoichio from a chemical formula
    """
    stoichios = formula_to_stoichios(chemical_formula)
    # normalization
    stoichios = stoichios/np.sum(stoichios)
    return stoichios


def extract_weight_fractions(chemical_formula):
    """ uses xraylib and its CompoundParser
    """
    chemical_formula = clear_marker(chemical_formula)
    my_elements = xraylib.CompoundParser(chemical_formula)
    return np.array(my_elements['massFractions'])
