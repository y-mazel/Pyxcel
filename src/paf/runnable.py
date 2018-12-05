# -*- coding: utf8 -*-
"""
For all thread option.


   :platform: Unix, Windows
   :synopsis: A base to create sink on a pipeline

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta, abstractmethod


class Runnable(object):
    """ Abstract class to inherit for create a pump class
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ initialization
        """
        self.reinit()
        self._is_stop = False
        self._is_finished = False

    @abstractmethod
    def reinit(self):
        """ initialize the thread again.
        """
        pass

    @property
    def is_finish(self):
        """ return True if the element is stoped and can't rerun (all connected
        pump is finish too).
        """
        if self._is_finished:
            return True
        else:
            if self._is_stop:
                self._is_finished = True
            return self._is_stop

    @is_finish.setter
    def is_finish(self, value):
        """ set is finish value
        """
        self._is_finished = value

    @property
    def running(self):
        """ property to know if the runnable thread is alive.
        """
        return not self._is_stop

    def stop(self):
        """ stop the execution.
        """
        try:
            if self._runner.is_alive():
                self._runner.join()
            else:
                self._is_stop = True
        except:
            pass

    @abstractmethod
    def run(self):
        """ Abstract method to define the pumping
        """
