# -*- coding: utf8 -*-
"""
for cx_frozen
"""
import os
import sys
import inspect


def get_base_dir():
    """ get director just parent of current executable
    """
    if getattr(sys, "frozen", False):
        # If this is running in the context of a frozen (executable) file,
        # we return the path of the main application executable
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
#         return os.path.abspath(os.path.join(exe_dir, os.pardir))
        return os.path.abspath(exe_dir)
    else:
        # If we are running in script or debug mode, we need
        # to inspect the currently executing frame. This enable us to always
        # derive the directory of main.py no matter from where this function
        # is being called
        this_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(os.path.join(this_dir, os.pardir))
