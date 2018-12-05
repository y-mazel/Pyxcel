# -*- coding: utf8 -*-
"""
use unicode for python 2 or 3

    :platform: Unix, Windows
    :synopsis: Controller module for modeling.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import sys

if sys.version_info[0] < 3:
    def uni(string_value):
        if isinstance(string_value, str):
            return unicode(string_value.decode("UTF-8"))
        else:
            return unicode(string_value)
else:
    uni = str
