# -*- coding: utf8 -*-
"""
Contain tools for calculating figure of merite.

    :platform: Unix, Windows
    :synopsis: optimisation filter to use GenX.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""


# GenX FOM to simple FOM
def genx_to_medepy(genx_fom):
    """ create a fonction to traansform genx fom to mpyxcelfom

    :param genx_fom: figure of merite for genx
    :type genx_fom: function
    :return: mpyxcelfom
    :rtype: function
    """
    def create_medepy_fom(p):
        """ create a mpyxcelfom

        :param p: number of parameter to fit
        """
        def medepy_fom(sim, data):
            """ mpyxcelfigure of merite
            """
            return genx_fom([sim], [data])
        return medepy_fom
    return create_medepy_fom


# FOM to genx fom
def medepy_to_genx(medepy_fom, p=1):
    """ create a genx fom from mpyxcelfom

    :param medepy_fom: FOM mpyxcel
    :param p: number of parameter to fit
    """
    def new_genx_fom(simulations, datas):
        """ new genx fom
        """
        return medepy_fom(p)(simulations[0], datas[0])
    return new_genx_fom
