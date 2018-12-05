# -*- coding: utf-8 -*-
"""
@author: JANOUSOV
"""
import numpy as np
import xraylib
from pyxcel.engine.modeling.tools import wavelength_to_in_energy
from pyxcel.engine.modeling.tools import extract_elements
from pyxcel.engine.modeling.tools import extract_weight_fractions


def calc_XRF_CS(one_element, transition, inc_en_eV):
    find = xraylib.CS_FluorLine_Kissel_Cascade
    XRF_CS = find(xraylib.SymbolToAtomicNumber(str(one_element)), transition,
                  inc_en_eV/1000.)
    return XRF_CS


def stack_slicing(d, z_start=11.0, z_stop=-11.0, dz=2.0):
    # slicing in Angstrom
    # for the sake of simplicity both z_start and z_stop will be positive
    # but d_slicing[:-1] must go in positive direction (wavefield propagates
    # into the substrate
    # and into layers)
    # and d_slicing[-1] must go in negative (I want to see the wavefield
    # propagation into Ambient)
    # d is an array with layers thicknesses, d[-1] = ambient and d[0] =
    # substrate
    # thicknesses for d[-1] and d[0] are ignored and replaced by z_start and
    # z_stop
    # order of d values in the d array must be reversed
    # returns z_array ( including the interface points so points are NOT
    # equidistant)
    # and d_slicing: slicing within the individual layers: a list of arrays
    # for z_array (for plotting):
    # zero is defined at the substrate
    # positive z goes into the stack, 0 is at the substrate, negative goes to
    # the substrate
    # because of the way the layers are labeled (0 for substrate, mm for
    # ambient)

    # first check/change sign of z_start and z_stop:
    z_start = np.abs(z_start)
    z_stop = np.abs(z_stop)
    # find z values corresponding to interfaces
    z_interface = []
    pom = 0
    for layer in d:
        pom = pom + layer
        z_interface = np.append(z_interface, pom)

    # within layers we define distance from the last interface
    # d_slicing is a list of arrays
    # below the substrate (d_slicing[0]):
    # assumption: zero of z is always at the substrate
    d_slicing = [np.linspace(np.round(z_start/dz)*dz,
                             0, np.abs(np.round(z_start/dz))+1,
                             endpoint=True)]
    # in the stack:
    for d_layer in d[1:]:
        # going from the substrate upwards but the wavefield propagates
        # downwards:
        # number of slices in each layer
        d_num = np.int((d_layer)/dz)
        one_d = np.linspace(d_layer, d_layer-dz*d_num, d_num+1, endpoint=True)
        # z starts at the top interface
        d_slicing.append(one_d)
    # in the ambient (replace last one)
    d_slicing[-1] = np.linspace(0, -np.round(z_stop/dz)*dz,
                                np.abs(np.round(z_stop/dz))+1, endpoint=True)
    # z_array must have points at each interface, equidistant between them
    # start from the substrate:
    # z_slicing: the same as d_slicing but in the whole stack
    # z_slicing: also a list of arrays
    # first layers (substrate):
    z_array = np.linspace(-np.round(z_start/dz)*dz, 0,
                          np.abs(np.round(z_start/dz))+1, endpoint=True)
    # d[0]
    z_slicing = [np.linspace(-np.round(z_start/dz)*dz, 0,
                             np.abs(np.round(z_start/dz))+1, endpoint=True)]
    # d[0]
    # next ones:
    for lay_idx, d_layer in enumerate(d[1:-1]):
        d_num = np.int(d_layer/dz)
        one_z = np.linspace(d_layer-dz*d_num, d_layer, d_num+1, endpoint=True)
        pom_layer = one_z+z_interface[lay_idx]
        z_array = np.append(z_array, pom_layer)
        z_slicing.append(pom_layer)
    # and now ambient
    last_array = np.linspace(z_interface[-1], z_interface[-1] +
                             np.round(z_stop/dz) *
                             dz, np.abs(np.round(z_stop/dz))+1, endpoint=True)
    z_array = np.append(z_array, last_array)
    z_slicing.append(last_array)
    return z_array, d_slicing, z_slicing, z_interface


def abso_layer(mass_dens, thickness, angle, mu_mass):
    # function to calculate absorption in a layer
    # either for the outgoing, then angle = inst.det_angle and
    # en_eV = line_en_eV
    # or incoming, then angle = inst.theta and en_eV = inc_en_eV
    # theoretically, the angles should be calculated from Parratt
    # (i.e. refraction)
    # need to transform units
    # thickness is in A
    return np.exp(-mu_mass*mass_dens*thickness*1e-8/np.sin((angle/180.*np.pi)))


class ElField:
    def __init__(self, theta, wavelength, n_array, d_array, sigma_array):
        # here only one number
        k = 2*np.pi/wavelength  # in A^-1
        # original GenX approach: remove "useless" layer properties
        sigma = sigma_array[:-1]

        nn = len(theta)
        mm = len(n_array)
        # original GenX layer sequence: 0: Substrate, -1: Ambient
        Xs = np.zeros((mm, nn), dtype=np.complex128)
        Xp = np.zeros((mm, nn), dtype=np.complex128)
        self.Er = np.zeros((mm, nn), dtype=np.complex128)
        self.Et = np.zeros((mm, nn), dtype=np.complex128)
        self.Hr = np.zeros((mm, nn), dtype=np.complex128)
        self.Ht = np.zeros((mm, nn), dtype=np.complex128)

        # initialize first layer (GenX)
        self.Et[-1] = np.ones(nn, dtype=np.complex128)
        self.Ht[-1] = np.ones(nn, dtype=np.complex128)

        # original layers order (like genx): 0th is Substrate, -1 is Ambient
        Qj = 2 * k * np.sqrt(n_array[:, np.newaxis] ** 2 -
                             (np.cos(theta*np.pi/180.)) ** 2)
        # original GenX ignores refraction from the Ambient
        # TODO: is this a reasonable assumption?
        # Calculates the wavevector in each layer
        Qj_eps = Qj / n_array[:, np.newaxis] ** 2
        self.njz = np.sqrt(n_array[:, np.newaxis] ** 2 -
                           (np.cos(theta*np.pi/180.)) ** 2)
        self.njz_eps = self.njz / n_array[:, np.newaxis] ** 2

        # Fresnel reflectivity for the interfaces
        # (Nevot-Croce) roughness already included:
        # TODO: separate roughness to be able to choose between Nevot-Croce and
        # Debye-Waller
        # TODO (check): Debye-Waller roughness
        # ps is the same as Ajs and Ajp above (I will need As to name something
        # else)
        # beware: d is a shorter array!
        # Ignoring the top and bottom layer for the calc.
        # For debugging
        # Setting up a matrix for the reduce function. Reduce only takes one
        # array as argument
        # Paratt's recursion formula
        def formula(rtot, rint):
            return (rint[0]+rtot*rint[1])/(1+rtot*rint[0]*rint[1])
        # Implement the recursion formula
        # TODO:
        # this may be wrong
        # I am not able to use the map/lambda/reduce/formula construct
        # let's define everything in loops
        # using genx layer convention: 0: substrate, -1: Ambient
        # GenX layers:
        Ajs = np.exp(1.0J*k*self.njz*d_array[:, np.newaxis])
        Ajp = np.exp(1.0J*k*self.njz_eps*d_array[:, np.newaxis])
        # attention: original GenX definition gives shorter arrays!
        rrs = (Qj[1:]-Qj[:-1])/(Qj[1:]+Qj[:-1])
        tts = 2.*Qj[1:]/(Qj[1:]+Qj[:-1])
        rrp = (Qj_eps[1:]-Qj_eps[:-1])/(Qj_eps[1:]+Qj_eps[:-1])
        ttp = 2*Qj_eps[1:]/(Qj_eps[1:]+Qj_eps[:-1])

        # add roughness (GenX)
        Ss_NC = np.exp(-1/2.*sigma[:, np.newaxis]**2*Qj[:-1]*Qj[1:])
        Sp_NC = np.exp(-1/2.*sigma[:, np.newaxis]**2*Qj_eps[:-1]*Qj_eps[1:])
        Ts_NC = np.exp(sigma[:, np.newaxis]**2 * k**2 *
                       (self.njz[:-1]-self.njz[1:])**2/2.0)
        Tp_NC = np.exp(sigma[:, np.newaxis]**2 * k**2 *
                       (self.njz_eps[:-1]-self.njz_eps[1:])**2/2.0)

        # the rest needs loops
        # in the GenX order:
        for kk in range(0, mm-1):
            Xs[kk] = ((rrs[kk] * Ss_NC[kk] + Ajs[kk]**2 * Xs[kk-1]) /
                      (1 + Ajs[kk]**2 * Xs[kk-1] * rrs[kk] * Ss_NC[kk]))
            Xp[kk] = ((rrp[kk] * Sp_NC[kk] + Ajp[kk]**2 * Xp[kk-1]) /
                      (1 + Ajp[kk]**2 * Xp[kk-1] * rrp[kk] * Sp_NC[kk]))
        for kk in range(mm-2, -1, -1):
            if kk == 0:  # if substrate
                self.Et[kk] = self.Et[kk+1] * Ajs[kk+1] * tts[kk]
                self.Ht[kk] = self.Ht[kk+1] * Ajp[kk+1] * ttp[kk]
            else:
                self.Et[kk] = (self.Et[kk+1] * Ajs[kk+1] * Ts_NC[kk] *
                               tts[kk] / (1 + Ajs[kk]**2 * Xs[kk-1] * rrs[kk] *
                                          Ss_NC[kk]))
                self.Ht[kk] = (self.Ht[kk+1] * Ajp[kk+1] * Tp_NC[kk] *
                               ttp[kk] / (1+Ajp[kk]**2 * Xp[kk-1] * rrp[kk] *
                                          Tp_NC[kk]))
        for kk in range(mm):
            self.Er[kk] = Ajs[kk]**2 * Xs[kk-1] * self.Et[kk]
            self.Hr[kk] = Ajp[kk]**2 * Xp[kk-1] * self.Ht[kk]

    def calcul_Ej(self, wavelength, d_array, z_start=-11, z_stop=11, dz=2):
        """
        """
        k = 2*np.pi/wavelength  # in A^-1
        mm = len(d_array)
        (self.z_array, d_slicing, self.z_slicing,
         self.z_interface) = stack_slicing(d_array, z_start, z_stop, dz)
        sh = np.shape(self.Er)
        lzs = np.size(self.z_array)
        sh = np.append(sh, lzs)
        Edj = np.zeros(sh, dtype=np.complex128)
        Euj = np.zeros(sh, dtype=np.complex128)
        self.Ej = np.zeros(sh, dtype=np.complex128)
        for lay_idx in range(mm):
            Edj[lay_idx, :, :np.size(d_slicing[lay_idx])] = self.Et[lay_idx][:, np.newaxis] * np.exp(1.J*k*self.njz[lay_idx][:,np.newaxis] * d_slicing[lay_idx][np.newaxis,:])
            Euj[lay_idx, :, :np.size(d_slicing[lay_idx])] = self.Er[lay_idx][:, np.newaxis] * np.exp(-1.J*k*self.njz[lay_idx][:,np.newaxis] * d_slicing[lay_idx][np.newaxis,:])
        self.Ej = Edj + Euj
        # now let's try to put the data from a list of arrays (Ej) to a single
        # array of dimensions no_of_angles x no_of_zsteps
        self.Ej_array = self.Ej[0, :, :np.size(d_slicing[0])].T
        Edj_array = Edj[0, :, :np.size(d_slicing[0])].T
        Euj_array = Euj[0, :, :np.size(d_slicing[0])].T
        for idx in range(mm-1):
            Edj_array = np.vstack((Edj_array, Edj[idx+1, :, :np.size(d_slicing[idx+1])].T))
            Euj_array = np.vstack((Euj_array, Euj[idx+1, :, :np.size(d_slicing[idx+1])].T))
            self.Ej_array = np.vstack((self.Ej_array, self.Ej[idx+1, :, :np.size(d_slicing[idx+1])].T))

    def el_field_int(self):
        """
        calculates electrical field intensity == XSW enhancement
        """
        field_int_array = np.abs(self.Ej_array*np.conj(self.Ej_array))
        return field_int_array


class FluoYield:
    """
    write documentation
    """
    #: cache line for each element
    line_energy_cach = {}

    def __init__(self, inst, n_array, mass_dens_array, mat_array):
        self.gam = 2*(np.real(n_array))*np.imag(n_array)
        # n_layers (without substrate and ambient)
        self._mm = np.size(n_array)
        self._elfield = None
        self._mass_dens_array = mass_dens_array
        self._mat_array = mat_array
        
#         # cleans mat_array from "_"
#         for idx, each in enumerate(self._mat_array):
#             self._mat_array[idx] = each.replace("_","")
#                 # "_" removal in mat_array
#         for idx, each in enumerate(mat_array):
#             self._mat_array[idx] = each.replace("_","")
                        
        self._inst = inst
        self._theta_array = None
        self.As = None
        self.Ap = None
        self.b = None
        self.Et = None
        self.Er = None

        self.mu_inc_lin = np.zeros(self._mm)
        # calculate mu_mass for all elements in all layers (just in case we
        # need them)

        all_elements = []
        # cleans "_" from material array mat_array
        for material in mat_array:
            all_elements = np.append(all_elements, extract_elements(material))
        # take only unique elements
        all_elements = list(set(all_elements)) # removes doubles in all_elements ndarray (unicity is implied in python sets)
        self.mu_mass_array = {}
        self.concentrations = {}
        for material in mat_array:
            self.mu_mass_array[material] = {}
            self.concentrations[material] = {}
            for one_element in all_elements:
                self.mu_mass_array[material][one_element] = {}
                line_energy = self.calculate_line_energy(one_element)
                for one_transition, line_en_keV in line_energy.items():
                    mu_mass_array = xraylib.CS_Total_CP(material, line_en_keV)
                    self.mu_mass_array[material][one_element][one_transition] = mu_mass_array
            for one_element in extract_elements(material):
                self.concentrations[material][one_element] = {}
                Zs = extract_elements(material)
                el_idx = np.where(Zs == one_element)
                self.concentrations[material][one_element] = extract_weight_fractions(material)[el_idx]

        # initialize
        self.abso_over_layers = {}

    def calculate_line_energy(self, one_element):
        """ calculating all line enregie for one element
        """
        #print('entering calculate_line_energy')
        if one_element in FluoYield.line_energy_cach.keys():
            return FluoYield.line_energy_cach[one_element]
        result = {}
        for one_transition in range(-256, 256):
            atomic_number = xraylib.SymbolToAtomicNumber(one_element)
            line_en_keV = xraylib.LineEnergy(atomic_number, one_transition)
            if line_en_keV != 0:
                result[one_transition] = line_en_keV
        FluoYield.line_energy_cach[one_element] = result
        return result

    def set_theta_array(self, value):
        self._theta_array = value
        nn = np.size(value)
        mm = self._mm
        ll = 3
        self.As = np.zeros((ll, mm, nn), dtype=np.complex128)
        self.Ap = np.zeros((ll, mm, nn), dtype=np.complex128)
        self.b = np.zeros((ll, mm, nn), dtype=np.complex128)

    def set_elfield(self, value):
        self._elfield = value
        elfield = value
        self.Et = elfield.Et
        self.Er = elfield.Er
        mass_dens_array = self._mass_dens_array
        mat_array = self._mat_array
        
        # clean mat_array from "_"
        
        
        inst = self._inst
        wavelength = inst["source"]["wavelength"].value
        inc_en_eV = wavelength_to_in_energy(wavelength)
        for lay_idx in range(self._mm):
            # TODO:
            # do not calculate everything again!
            mu_inc = xraylib.CS_Total_CP(mat_array[lay_idx],
                                         inc_en_eV/1000.)
            # calculate lin. absorption coeff:
            self.mu_inc_lin[lay_idx] = mu_inc*mass_dens_array[lay_idx]
            # [cm-1]
            k = 2*np.pi/wavelength
            # As and bs need to be in the same units as mu_inc, i.e. cm-1
            self.As[0, lay_idx, :] = (k * 1e8 * (self.gam[lay_idx] /
                                                 self.mu_inc_lin[lay_idx]) *
                                      (np.absolute(elfield.Et[lay_idx]) *
                                       np.absolute(elfield.Et[lay_idx])))
            self.As[1, lay_idx, :] = (k * 1e8 * (self.gam[lay_idx] /
                                                 self.mu_inc_lin[lay_idx]) *
                                      (np.absolute(elfield.Er[lay_idx]) *
                                       np.absolute(elfield.Er[lay_idx])))
            self.As[2, lay_idx, :] = (2 * k * 1e8 *
                                      (self.gam[lay_idx] /
                                       self.mu_inc_lin[lay_idx]) *
                                      (elfield.Et[lay_idx]) *
                                      np.conj(elfield.Er[lay_idx]))
            self.Ap[0, lay_idx, :] = (2 * k * 1e8 *
                                      (np.imag(elfield.njz[lay_idx]) /
                                       self.mu_inc_lin[lay_idx]) *
                                      np.real(elfield.njz_eps[lay_idx]) *
                                      (np.absolute(elfield.Ht[lay_idx]) *
                                       np.absolute(elfield.Ht[lay_idx])))
            self.Ap[1, lay_idx, :] = (2 * k * 1e8 *
                                      (np.imag(elfield.njz[lay_idx]) /
                                       self.mu_inc_lin[lay_idx]) *
                                      np.real(elfield.njz_eps[lay_idx]) *
                                      (np.absolute(elfield.Hr[lay_idx]) *
                                       np.absolute(elfield.Hr[lay_idx])))
            self.Ap[2, lay_idx, :] = (4 * k * 1e8 *
                                      (np.real(elfield.njz[lay_idx]) /
                                       self.mu_inc_lin[lay_idx]) *
                                      np.imag(elfield.njz_eps[lay_idx]) *
                                      elfield.Ht[lay_idx] *
                                      np.conj(elfield.Hr[lay_idx]))
            self.b[0, lay_idx, :] = 2 * k * 1e8 * np.imag(elfield.njz[lay_idx])
            self.b[1, lay_idx, :] = -2*k*1e8*np.imag(elfield.njz[lay_idx])
            self.b[2, lay_idx, :] = -2*k*1e8*1.0j*np.real(elfield.njz[lay_idx])

    def fluo_int(self, det_angle_array, n_array, d_array,
                 sigma_array, mass_dens_array, mat_array, one_element,
                 transition, XRF_CS):
        mm = np.size(mat_array)  # number of strata
        nn = np.size(self._theta_array)  # number of angular points
        # TODO
        # polarization
        sf = .5  # unpolarized
        pf = 1.0 - sf
        abso_over_layers = np.ones((mm, nn))
        for i in range(mm-2, -1, -1):  # I need to calculate absorption in all
            # layers just in case my element is present everywhere
            abso_out_above = abso_layer(mass_dens_array[i+1], d_array[i+1],
                                        det_angle_array,
                                        self.mu_mass_array[mat_array[i+1]]
                                        [one_element][transition])
            abso_over_layers_lay = abso_over_layers[i+1] * abso_out_above
            abso_over_layers[i, :] = abso_over_layers_lay
        fluo_intensity = 0.0
        for j_layer in range(mm):
            # to sum contributions for the same element+transition from several
            # layers
            tot_intensity = 0.0
            if one_element in extract_elements(mat_array[j_layer]):
                # calculate lin. absorption coeff:
                muja_over_sin_ang_det = (mass_dens_array[j_layer] *
                                         self.mu_mass_array[mat_array[j_layer]]
                                         [one_element][transition] /
                                         np.sin(det_angle_array/180.*np.pi))
                dj = d_array[j_layer]*1e-8  # [cm]
                three_comp = np.complex(0, 0)
                for ii in range(3):
                    arg_abs = self.b[ii, j_layer, :] + muja_over_sin_ang_det
                    if j_layer == 0:  # sub
                        three_comp = three_comp + (sf *
                                                   self.As[ii, j_layer, :] +
                                                   pf * self.Ap[ii, j_layer, :]
                                                   ) / arg_abs
                    else:
                        three_comp = three_comp + (sf *
                                                   self.As[ii, j_layer, :] +
                                                   pf * self.Ap[ii, j_layer, :]
                                                   ) * (1.0 - np.exp
                                                        (-dj * arg_abs)
                                                        ) / arg_abs
                intensity = XRF_CS*np.real(three_comp)
                tot_intensity = (intensity * abso_over_layers[j_layer+1] *
                                 mass_dens_array[j_layer] *
                                 self.concentrations[mat_array[j_layer]]
                                 [one_element])
            fluo_intensity = fluo_intensity + tot_intensity
        return fluo_intensity

    def fluo_thin_layer(self, theta_array, det_angle_array, n_array, d_array,
                        sigma_array, mass_dens_array, mat_array, one_element,
                        transition, XRF_CS, inst):
        mm = np.size(mat_array)  # number of strata
        nn = np.size(theta_array)  # number of angular points
        # TODO
        # polarization
        abso_over_layers = np.ones((mm, nn))
        for i in range(mm-2, -1, -1):
            # I need to calculate absorption in all layers
            # just in case my element is present everywhere
            # abso_over_layers[j_layer] means absorption for signal (with E =
            # transition energy) originating in j_layer
            abso_out_above = abso_layer(mass_dens_array[i+1], d_array[i+1],
                                        det_angle_array,
                                        self.mu_mass_array[mat_array[i+1]]
                                        [one_element][transition])
            abso_over_layers_lay = abso_over_layers[i+1] * abso_out_above
            abso_over_layers[i, :] = abso_over_layers_lay
        fluo_intensity = 0.0
        for j_layer in range(mm):
            # to sum contributions for the same element+transition from several
            # layers
            intensity = 0.
            if one_element in extract_elements(mat_array[j_layer]):
                XSW_enhancement = (np.abs(self.Et[j_layer] +
                                          self.Er[j_layer])) ** 2
                dj = d_array[j_layer] * 1e-8  # [cm]
                intensity = (self.gam[j_layer] / self.mu_inc_lin[j_layer] *
                             inst.k * 1e8 * XRF_CS * XSW_enhancement *
                             abso_over_layers[j_layer+1] * dj *
                             abso_over_layers[j_layer+1] *
                             mass_dens_array[j_layer] *
                             self.concentrations[mat_array[j_layer]]
                             [one_element])
            fluo_intensity = fluo_intensity + intensity
        return fluo_intensity


def fluo_quanti(fluo_intensity, inc_flux, inst, det_efficiency,
                inc_angle_array):
    """ add instrumental correction
    """
    quanti_intensity = (fluo_intensity * inc_flux * inst * det_efficiency)
    return quanti_intensity
