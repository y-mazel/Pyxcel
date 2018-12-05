# -*- coding: utf8 -*-
"""
all necessary tools to perform FFT.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import numpy as np


def next_pow2(n):
    """return the value of next power of 2
    """
    return 2**np.ceil(np.log2(n))


def select_data(dataset, critical_angle, Imin):
    """ select data for I > Imin and Angle > Critical_Angle
    """
    del_all = False
    for idx, theta in enumerate(dataset.x):
        if theta < critical_angle or del_all:
            del dataset[idx]
        if dataset.y < Imin:
            del dataset[idx]
            del_all = True


def diff_log(dataset, dw):
    """ Differentiate logarithm of the raw data *very good way to eliminate
    background and keep the Kiessing fringes*

    :param dataset: dataset
    :param dw: Differentiating Window size: *even number expected*
    """
    # TODO:
    pass
