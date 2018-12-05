# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Contain code defined for all active (pump, sink and filter) element of a
pipeline.


   :platform: Unix, Windows
   :synopsis: A base to create sink on a pipeline

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta
import paf.parameter
import paf.runnable


class Element(paf.runnable.Runnable, paf.parameter.Parametrable):
    """ Abstract base class to defined any element.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ initialization
        """
        paf.runnable.Runnable.__init__(self)
        paf.parameter.Parametrable.__init__(self)
