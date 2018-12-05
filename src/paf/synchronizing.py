# -*- coding: utf8 -*-
"""
To help to synchronize thread.

   :platform: Unix, Windows
   :synopsis: module To help to synchronize thread.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""


def synchronized(function):
    """ Synchronization decorator

    must be used on methods in a class with class member lock.
    """
    def new_function(self, *args, **kw):
        """ function to guarantee the function to call only once.
        """
        with self.lock:
            return function(self, *args, **kw)
    return new_function
