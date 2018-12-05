# -*- coding: utf-8 -*-
"""
Created on 26/03/2015

@author: Rotella
"""
import numpy as np
from scipy.special import ellipk as F
from scipy.special import ellipkinc as F_inc
from scipy.special import ellipe as E
from scipy.special import ellipeinc as E_inc
from scipy.interpolate import interp1d


class Exp_configuration():
    def __init__(self, inc_ang_deg, out_ang_deg, distance_sample_det_window_cm,
                 scattering_angle_deg=None, collimator=None,
                 configuration='theta-theta', bfwhm=50.0,
                 detection_solid_angle_ratio=0.001):
        """
            configuration can be "theta-theta" or "theta-2theta";
            experimental configuration details
        """
        self.bfwhm = bfwhm  # um
        self.inc_ang_deg = np.asarray(inc_ang_deg)
        self.out_ang_deg = out_ang_deg
        if self.inc_ang_deg[0] == 0.0:
            self.inc_ang_deg[0] = 1e-10
        self.t_arr = self.inc_ang_deg * np.pi / 180.0
        self.scatt_ang_deg = scattering_angle_deg
        self.distance_sample_det_window_cm = distance_sample_det_window_cm
        self.collimator = collimator
        self.configuration = configuration
        self.detection_solid_angle_ratio = detection_solid_angle_ratio

    def set_angles(self, angles, array_type='deg'):
        """

        :param Array_type: 'rad' or 'deg': sample angle array
        """
        angles = np.array(angles)
        if array_type == 'rad':
            if angles[0] == 0.0:
                self.t_arr = angles
                self.t_arr[0] = 1e-12
                self.inc_ang_deg = (angles*180.0/np.pi)
            else:
                self.t_arr = angles
                self.inc_ang_deg = (angles*180.0/np.pi)

        elif array_type == 'deg':
            if angles[0] == 0.0:
                self.inc_ang_deg = angles
                self.inc_ang_deg[0] = 1e-10
                self.t_arr = (angles*np.pi/180.0) + np.finfo(float).tiny
            else:
                self.inc_ang_deg = angles
                self.t_arr = angles * np.pi / 180.0

        else:
            raise AttributeError('Angle unit Not Recognized')


class Detector_Collimator():
    def __init__(self, width_parallel_cm_s=0.504, width_parallel_cm_l=0.504,
                 pinhole_height_cm=0.274):
        """ collimator details
        """
        self._width_parallel_cm_s = width_parallel_cm_s
        self._width_parallel_cm_l = width_parallel_cm_l
        self._pinhole_height_cm = pinhole_height_cm

    @property
    def width_parallel_cm_s(self):
        """ property for access width_parallel_cm_s
        """
        return self._width_parallel_cm_s

    @property
    def width_parallel_cm_l(self):
        """ property for access width_parallel_cm_l
        """
        return self._width_parallel_cm_l

    @property
    def pinhole_height_cm(self):
        """ property for access pinhole_height_cm
        """
        return self._pinhole_height_cm


class GetGeometricCorrection(object):
    def __init__(self, cach_size=5):
        """ initialization
        """
        #: cahch of some result
        self._cach = [0] * cach_size
        #: cahch keys
        self._cach_keys = [(0,)*7] * cach_size
        #: cache size
        self._cach_size = cach_size
        #: current cach index
        self._cach_index = 0

    def __call__(self, sampleLength, exp_configuration, theta_array):
        """ Correction from ideal simulation
        """
        key = (exp_configuration.collimator.width_parallel_cm_s,
               exp_configuration.collimator.width_parallel_cm_l,
               exp_configuration.collimator.pinhole_height_cm,
               exp_configuration.out_ang_deg, exp_configuration.bfwhm,
               exp_configuration.scatt_ang_deg,
               exp_configuration.distance_sample_det_window_cm,
               theta_array.size)
        if key in self._cach_keys:
            return self._cach[self._cach_keys.index(key)]
        sini = np.sin(exp_configuration.t_arr)

        final_len, final_len_extr = getCollectionLength(sampleLength,
                                                        exp_configuration)

        acc_function = getSolidAngleAcceptanceFunction_new(final_len_extr,
                                                           exp_configuration)

        n_points = len(acc_function)
        x = np.linspace(-final_len_extr[0, 0], final_len_extr[1, 0], n_points)

        gau_beams = []
        for ii, sinii in enumerate(sini):
            gau_beams.append(gaussian(0.0, exp_configuration.bfwhm /
                                      (sinii*2.0*np.sqrt(2*np.log(2)))))

        corr = np.zeros(len(sini))
        for ii in range(len(sini)):
            gau = gau_beams[ii](x)
            int_func = gau * acc_function
            integral = np.trapz(int_func, x, dx=(x[1]-x[0]))
            corr[ii] = integral/(final_len[ii]*np.max(int_func))

            if np.isnan(corr[ii]):
                corr[ii] = 0.0

        if corr[0] == 0.0:
            corr[0] = corr[1]
        self._cach[self._cach_index] = corr
        self._cach_keys[self._cach_index] = key
        if self._cach_index < self._cach_size-1:
            self._cach_index += 1
        else:
            self._cach_index = 0
        return corr


def getCollectionLength(sampleLength, Exp_configuration):
    """
    Returns the total length of the collection area. The limits can be given by
    the sample length or the inspected area.
    Since the area is asymmetric two different values are returned:
    A is the length of the projection on the detector side, B is the length of
    the projection on the x ray source side.
    Output:
    return [collectionAreaLength,A,B,coll_len_extr]
    collectionAreaLength -> Total length of the collection Area
    A -> length of the projection @ detector side
    B -> length of the projection @ x ray source side
    coll_len_extr -> extream points of the collection area, accounting shift
    given by possible z sample offset
    """
    possibleConfiguration = ['theta-theta', 'theta-2theta']

    if Exp_configuration.configuration in possibleConfiguration:
        if (Exp_configuration.out_ang_deg)*np.pi/180.0 > np.pi/2:
            det_ang = np.pi - Exp_configuration.out_ang_deg*np.pi/180.0
        else:
            det_ang = Exp_configuration.out_ang_deg*np.pi/180.0

        if Exp_configuration.configuration == 'theta-theta':

            d2 = Exp_configuration.collimator.pinhole_height_cm*10.0
            d = (Exp_configuration.distance_sample_det_window_cm)*10.0
            dp1 = Exp_configuration.collimator.width_parallel_cm_s*10.0
            dp2 = Exp_configuration.collimator.width_parallel_cm_l*10.0
            a = d2/(1+dp1/dp2)
            A = (a+d)/((a*2/dp2)*np.sin(det_ang) + np.cos(det_ang))
            # Detector side respect to center (opposite if theta>90)
            B = (a+d)/((a*2/dp2)*np.sin(det_ang) - np.cos(det_ang))
            # X-Ray source side respect to center (opposite if theta>90)

            if det_ang > np.pi / 2:
                coll_len_extr = np.array([A, B])
            else:
                coll_len_extr = np.array([B, A])

            coll_len_extr = np.transpose(np.array([B, A]))

            sample_limits = np.array([sampleLength/2.0, sampleLength/2.0])
            final_len_extr = np.minimum(coll_len_extr, sample_limits)
            final_len = final_len_extr.sum()

            final_len = np.ones(len(Exp_configuration.t_arr))*final_len
            final_len_extr = np.ones([len(Exp_configuration.t_arr),
                                      2])*final_len_extr

            return [final_len, final_len_extr]

        else:

            alpha = det_ang - Exp_configuration.t_arr*np.pi/180

            d2 = Exp_configuration.collimator.pinhole_height_cm*10.0
            d = (Exp_configuration.distance_sample_det_window_cm)*10.0
            dp1 = Exp_configuration.collimator.width_parallel_cm_s*10.0
            dp2 = Exp_configuration.collimator.width_parallel_cm_l*10.0
            a = d2/(1+dp1/dp2)
            A = (a+d)/((a*2/dp2)*np.sin(alpha) + np.cos(alpha))
            # Detector side respect to center (opposite if theta>90)
            B = (a+d)/((a*2/dp2)*np.sin(alpha) - np.cos(alpha))
            # X-Ray source side respect to center (opposite if theta>90

            if det_ang > np.pi / 2:
                coll_len_extr = np.array([A, B])
            else:
                coll_len_extr = np.array([B, A])

            coll_len_extr = np.transpose(np.array([B, A]))

            sample_limits = np.array([sampleLength/2.0, sampleLength/2.0])
            final_len_extr = np.minimum(coll_len_extr, sample_limits)
            final_len = final_len_extr.sum(axis=1)

            # final_len = np.ones(len(Exp_configuration.t_arr))*final_len
            final_len_extr = np.ones([len(Exp_configuration.t_arr),
                                      2])*final_len_extr

            return [final_len, final_len_extr]

    else:
        raise AttributeError('Configuration unknown: try theta-theta or \
theta-2theta')


def getSolidAngleAcceptanceFunction_new(final_len_extr, Exp_configuration):
    """
    """

    n_points = 300
    dp1 = Exp_configuration.collimator.width_parallel_cm_s*10.0
    dp2 = Exp_configuration.collimator.width_parallel_cm_l*10.0
    tot_len = np.abs(final_len_extr[0][0])+final_len_extr[1][0]
    x = np.linspace(0, tot_len, n_points)
    y = np.zeros(n_points)

    d2 = Exp_configuration.collimator.pinhole_height_cm*10.0
    d1 = (Exp_configuration.distance_sample_det_window_cm)*10.0
    dpd = np.sqrt(((dp1+dp2)/2.0)**2 + d2**2)
    d = d1 + d2

    l1 = np.sqrt(d1**2 + (np.abs(final_len_extr[0][0])-dp2/2)**2)

    a = lambda xx, l: (final_len_extr[0][0]-xx)*dpd/l
    b = lambda xx, l: np.sqrt((dp2/2)**2 -
                              ((2*(dp2/2) -
                                ((final_len_extr[0][0]-xx)*dpd/l)) / 2.0)**2)
    # Is already the semiaxes

    x = x - x[-1]/2.0
    x_mid = x[(np.array(x >= (-dp2/2)) & np.array(x <= dp2/2))]

    acc_func_mid = getSolidAngle(np.abs(x_mid), dp2/2, d)

    y[np.array(x >= (-dp2/2)) & np.array(x <= dp2/2)] = np.array(acc_func_mid)

    x1 = x[x < (-dp2/2)]
    acc_func1 = getSolidAngle_ellipse(np.abs(x1), b(np.abs(x1), l1),
                                      a(np.abs(x1), l1)/2.0, d)
    y[x < (-dp2/2)] = acc_func1

    l2 = np.sqrt(d1**2 + (np.abs(final_len_extr[1][0])-dp2/2)**2)

    x2 = x[x > dp2/2]
    acc_func2 = getSolidAngle_ellipse(np.abs(x2), b(np.abs(x2), l2),
                                      a(np.abs(x2), l2)/2.0, d)

    y[x > (dp2/2)] = acc_func2

    y[0] = 0.0
    y[-1] = 0.0

    no_nan_y = y[~np.isnan(y)]
    x_no_nan = x[~np.isnan(y)]

    interp_curv = interp1d(x_no_nan, no_nan_y, kind='slinear')

    return interp_curv(x)


def getSolidAngle(r0, rm, L):
    """
    r0 is the distance from the detector center to the projection of the
    considered point into the plane of the detector
    rm is the detector radius in mm
    d is the distance of the detector windows to the sample in mm
    """
    k = np.sqrt((4.0*r0*rm)/(L**2 + (r0+rm)**2.0))
    xi = np.arctan(L/np.abs(r0-rm))
    Rmax = np.sqrt(L**2.0+(r0+rm)**2.0)

    solid_ang = np.zeros(len(r0))
    sup = r0 < rm
    eq = r0 == rm
    inf = r0 > rm
    if solid_ang[sup] != []:
        Lam0 = Heumans_Lambda_func(xi[sup], k[sup])
        solid_ang[sup] = (2.0*np.pi - (2.0*L/Rmax[sup])*F(k[sup]*k[sup]) -
                          np.pi*Lam0)
    if solid_ang[eq] != []:
        solid_ang[eq] = np.pi - (2.0*L/Rmax[eq])*F(k[eq]*k[eq])
    if solid_ang[inf] != []:
        Lam0 = Heumans_Lambda_func(xi[inf], k[inf])
        solid_ang[inf] = -2.0*L*F(k[inf]*k[inf])/Rmax[inf] + np.pi*Lam0
    return solid_ang


def getSolidAngle_ellipse(r0, a, b, L):
    """
    r0 is the distance from the detector center to the projection of the
    considered point into the plane of the detector
    rm is the detector radius in mm
    d is the distance of the detector windows to the sample in mm
    """

    k = np.sqrt((a*a - 2*b*b - L*L - r0*r0 +
                 np.sqrt((r0*r0 - a*a)**2 + 2*L*L*(r0*r0+a*a)+L**4)) /
                 (2*np.sqrt((r0*r0 - a*a)**2 + 2*L*L*(r0*r0 + a*a) + L**4)))

    xi = np.arcsin(np.sqrt((L*L + r0*r0 - a*a +
                            np.sqrt((r0*r0 - a*a)**2 + 2*L*L*(r0*r0 + a*a) +
                                    L**4)) /
                           (2*b*b + L*L+r0*r0-a*a + np.sqrt((r0*r0-a*a)**2 +
                                                            2*L*L*(r0*r0+a*a) +
                                                            L**4))))
    Lam0 = Heumans_Lambda_func(xi, k)

    return 2.0*np.pi*(1-Lam0)


def Heumans_Lambda_func(xi, k):
    """ Heuman's delta function evaluation
    """

    k1 = np.sqrt(1.0-k**2.0)
    return (2.0/np.pi)*(E(k*k)*F_inc(xi, k1*k1)+F(k*k)*E_inc(xi, k1*k1) -
                        F(k*k)*F_inc(xi, k1*k1))


def gaussian(xc, w, y_offset=0.0, height=None):
    "(1.0/(w*sqrt(pi/2.0)))*exp(-2.0*((x-xc)/w)**2)   w>0"
    f = lambda xx: (y_offset + (1.0/(w*np.sqrt(2.0*np.pi))) *
                    np.exp(-0.5*((xx-xc)/w)**2.0))
    return f
