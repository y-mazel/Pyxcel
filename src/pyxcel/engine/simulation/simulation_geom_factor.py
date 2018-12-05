# -*- coding: utf8 -*-
"""
calcul only geom factor.

    :platform: Unix, Windows
    :synopsis: XRR simulation using GenX.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import paf.filter_base as filters
from pyxcel.engine.gixrf.geom_factor import Detector_Collimator
from pyxcel.engine.gixrf.geom_factor import Exp_configuration
from pyxcel.engine.gixrf.geom_factor import GetGeometricCorrection
import numpy as np
import paf.data as data
import quantities as pq
MAKE_DATA = data.make_data


class GeomFactorSimulator(filters.Filter):
    def __init__(self):
        filters.Filter.__init__(self)
        self.add_expected_parameter("start_theta", MAKE_DATA(0.),
                                    MAKE_DATA(.01))
        self.add_expected_parameter("end_theta", MAKE_DATA(0.), MAKE_DATA(1.))
        self.add_expected_parameter("nb_of_point", MAKE_DATA(0),
                                    MAKE_DATA(100))
        self.add_expected_parameter("sample_len", MAKE_DATA(unit=pq.mm))
        self.add_expected_parameter("conf", MAKE_DATA('theta-2theta'),
                                    MAKE_DATA('theta-2theta'))

    def run(self):
        instrument = self.get_data("main")
        detector = instrument["detector"]
        width_parallel_s = detector["width_parallel_s"].value
        width_parallel_l = detector["width_parallel_l"].value
        pinhole_height = detector["pinhole_height"].value
        start_theta = self["start_theta"].value
        end_theta = self["end_theta"].value
        nb_of_point = self["nb_of_point"].value
        theta_array = np.array(np.linspace(start_theta, end_theta,
                                           nb_of_point))
        collimator = Detector_Collimator(width_parallel_s, width_parallel_l,
                                         pinhole_height)

        out_ang_deg = detector["det_angle_array"].value
        distance_det_window_to_sample = detector["dist"].value
        exp_configuration = Exp_configuration(theta_array, out_ang_deg,
                                              distance_det_window_to_sample,
                                              scattering_angle_deg=None,
                                              collimator=collimator,
                                              configuration=self["conf"].value,
                                              bfwhm=instrument["source"]
                                              ["beamw"].value)
        samplelen = self["sample_len"].value
        geometric_calc = GetGeometricCorrection()
        self._geom = geometric_calc(samplelen, exp_configuration)
        type_name = "geom"
        self.fill_port("main", MAKE_DATA({type_name: self._geom,
                                          "theta_array": theta_array,
                                          "composite": True},
                                         abstract="data_"+type_name))
