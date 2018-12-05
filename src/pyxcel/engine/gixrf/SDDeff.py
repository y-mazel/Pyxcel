# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 15:13:51 2014

Tested against IDL codes

Correct (to a ppm digit) with en_array = [277.,525.,677,1487.,1554.,1740.]
@author: BD237097
"""
from scipy.interpolate import interp1d
import xraylib
import numpy as np


def diode_interp(energy_array):
    # makes sure we are dealing with an array, not a list
    Enax = [50, 55, 60, 65, 70, 75, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
            91, 92, 93, 94, 95, 99, 100, 101, 102, 103, 104, 105, 106, 107,
            108, 109, 110, 111, 112, 114, 116, 118, 120, 122, 124, 126, 128,
            130, 132, 134, 136, 138, 140, 150, 160, 170, 180, 200, 220, 240,
            260, 320, 340, 360, 380, 400, 450, 500, 550, 600, 650, 700, 750,
            800, 850, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700,
            1800, 1830, 1840, 1850, 1900]
    Response = [0.1426, 0.1672, 0.1904, 0.2025, 0.2095, 0.2168, 0.2231, 0.2241,
                0.225, 0.2258, 0.2265, 0.2271, 0.2276, 0.228, 0.2284, 0.2287,
                0.2291, 0.2295, 0.2298, 0.2303, 0.2307, 0.2311, 0.232, 0.1891,
                0.1534, 0.1696, 0.1737, 0.1763, 0.176, 0.1693, 0.1638, 0.1588,
                0.1581, 0.1581, 0.1549, 0.1518, 0.1483, 0.141, 0.1343, 0.1315,
                0.129, 0.1284, 0.1279, 0.1276, 0.1286, 0.1264, 0.128, 0.1329,
                0.136, 0.1362, 0.1368, 0.1379, 0.1389, 0.1541, 0.1639, 0.1725,
                0.183, 0.1934, 0.2134, 0.2205, 0.2254, 0.2307, 0.2291, 0.2391,
                0.2399, 0.2442, 0.2485, 0.2533, 0.2563, 0.2584, 0.2605, 0.2622,
                0.2637, 0.2659, 0.267, 0.2669, 0.2653, 0.2613, 0.2553, 0.2463,
                0.2344, 0.2181, 0.2189, 0.25, 0.2475, 0.2515]

    f = interp1d(np.array(Enax, dtype=np.float64), Response)
    diode = []
    for one_energy in energy_array:
        diode = np.append(diode, f(one_energy))
    return diode


def eff_sdd1_09_kw49(energy_array):
    # in eV
    # makes sure we are dealing with an array, not a list
    energy_array = np.array(energy_array)
    sdd_mu = []
    for one_energy in energy_array:
        sdd_mu = np.append(sdd_mu, xraylib.
                           CS_Total(xraylib.SymbolToAtomicNumber('Si'),
                                    one_energy / 1000.))

    sdd_rho = xraylib.ElementDensity(xraylib.SymbolToAtomicNumber('Si'))
    sdd_thickness = 0.04  # There are measurements on the KMC, which result in
    # a SDD efficiency of 0.91 at 10.5 keV ...
    sdd_abs = 1 - np.exp(-sdd_mu * sdd_rho * sdd_thickness)
    elements = ['O', 'Al', 'Si', 'Au']  # determined empirically -> describe
    # good SDD efficiency curve from HNS_09_kw49
    mysize = np.size(elements)
    front_rho = []
    front_thickness = np.zeros(mysize)
    front_mu = np.zeros((mysize, np.size(energy_array)))
    for el_idx, element in enumerate(elements):
        mu = np.array([])
        for one_energy in energy_array:
            mu = np.append(mu, xraylib.
                           CS_Total(xraylib.SymbolToAtomicNumber(element),
                                    one_energy / 1000.))
        front_mu[el_idx, :] = np.array(mu)
        front_rho.append(xraylib.
                         ElementDensity(xraylib.SymbolToAtomicNumber(element)))

    # the SDD efficiency curve from HNS_09_kw49 fitted (CurveFit):
    # lead to an order of magnitude different start values ​​for deviations in
    # the result <1%
    # all y-values ​​equal weighting
    front_thickness[0] = 3.0384771e-06  # thickness of Oxid-Schicht 30nm
    front_thickness[1] = 3.8169987e-06  # thickness of Aluminium-Schicht 40nm
    front_thickness[2] = 1.0255867e-06  # thickness of Silizium-Totschicht 10nm
    front_thickness[3] = 2.4680169e-07  # thickness of Gold-Schicht 2.5nm
    front_abs = 1.
    for el_idx, element in enumerate(elements):
        front_abs = front_abs * np.exp(-front_mu[el_idx, :] *
                                       front_rho[el_idx] *
                                       front_thickness[el_idx])
    sdd_eff = np.array(sdd_abs * front_abs)

    return sdd_eff
