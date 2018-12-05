# -*- coding: utf8 -*-
"""
Contain the Filter to optimize data with inspyred evolution computing type
algorithm.

    :platform: Unix, Windows
    :synopsis: optimisation filter to use inspyred.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""


class param_generator(object):
    """ population generator for random adding the start
    """
    def __init__(self, start=None):
        """ initialization
        """
        self._start = start
        self._is_first = True

    def __call__(self, rand, args):
        """ execute generator
        """
        if self._is_first:
            self._is_first = False
            return self._start
        bounder = args["_ec"].bounder
        return [rand.uniform(lo, hi)
                for lo, hi in zip(bounder.lower_bound, bounder.upper_bound)]
