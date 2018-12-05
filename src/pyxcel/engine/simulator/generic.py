# -*- coding: utf8 -*-
"""
Filter for doing simulation with a simulator.

    :platform: Unix, Windows
    :synopsis: generic simulation using a simulator.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
from abc import ABCMeta, abstractmethod
import paf.data
import re
MAKE_DATA = paf.data.make_data


class Simulator(paf.data.CompositeData):
    """ class ancestor for every simulator
    """
    __metaclass__ = ABCMeta

    def __init__(self, theta_array, stack, instrument, abstract="simulator"):
        """ initialization
        """
        parameter = MAKE_DATA({}, composite=True)
        value = {"theta_array": theta_array, "instrument": instrument,
                 "stack": stack, "parameter": parameter}
        paf.data.CompositeData.__init__(self, value, abstract)
        self._stop = False
        self._fom_const = 0
        self._last_fom = 0.
        self._max_fom_const = 0
        self._regex_stochio = None
        self._parmeters = None
        self._profile_name = []
        self._all_prof = None
        self._sample = None

    @property
    def stop(self):
        """ property to acces to stopping status
        """
        return self._stop

    @stop.setter
    def stop(self, value):
        """ stop simulation
        """
        self._stop = value

    @abstractmethod
    def initialization(self, filter_):
        """ method call in start of simulation and at the first run of fitting.
        """
        self._sample = self["stack"]
        self._filter = filter_
        try:
            if self._filter["max_fom_const"].value != 0:
                self._max_fom_const = self._filter["max_fom_const"].value
                self.evaluate = self.evaluate_max_fom_const
        except KeyError:
            pass
        self._stop = False
        self._fit_stochio = False
        try:
            if filter_.fit_stochio:
                self._fit_stochio = True
                parameter = filter_.get_data("main").value
                find_layers = re.findall("stochio_[a-zA-Z0-9_]*", parameter)
                profile_layers = re.findall(".*Profile_[a-zA-Z0-9_]*", parameter)
                self._profile_name = list(set([x[:x.index('.')]
                                               for x in profile_layers]))
                self._layer_stochio = list([x[8:] for x in find_layers]) 
                # self._layer_stochio = list(set([x[8:] for x in find_layers])) # strips "stochio_" from list strings
                self.simulate = self.simulate_stochio
                self._regex_stochio = re.compile("_\d*\.?\d*")
                stack_data = self._sample

                # create list of materials
                stochio_name = self._layer_stochio
                all_mat = {lay["name"].value: lay["material"].value
                           for lay in stack_data["layers"]}
                self._mat = {item[0]: item[1] for item in all_mat.items()
                             if item[0] in stochio_name} # check for "_" in the _mat dictionary

#                 for key, value in self._mat.iteritems(): # does nothing
#                     self._mat[key].replace("_","")
                    
                # save calculator
                self._density_translator = stack_data.density_translator
                self._physical_computer = stack_data.physical_computer
        except AttributeError:
            pass

    @abstractmethod
    def simulate(self):
        """ doing the simulation.

        :rtype: np.array
        :return: result of the simulation.
        """
        self.evaluate()
#         if self._stop:
#             thread.exit()

    def evaluate(self):
        pass

    def evaluate_max_fom_const(self):
        """ doing the simulation.

        :rtype: np.array
        :return: result of the simulation.
        """
        if self._last_fom == self._filter.opt.best_fom:
            self._fom_const += 1
        else:
            self._fom_const = 0
            self._last_fom = self._filter.opt.best_fom
        if self._fom_const >= self._max_fom_const:
            self._filter.stop()

    def simulate_stochio(self):
        """ doing the simulation with stochio.

        :rtype: np.array
        :return: result of the simulation.
        """
#         print("pyxcel/engin/simulator/generic.py/Simulator.simulate_stochio")
#         print(".............................")
        if self._all_prof is None:
            self._all_prof = []
            for name in self._profile_name:
                index = self._parmeters["name"].index(name + "_end")
                last_name = name + "_end"
                while last_name != name + "_start":
                    last_name = self._parmeters["name"][index]
                    self._all_prof.append(last_name)
                    index += 1
        for name, mat in self._mat.items():
            fitted_value = self._filter.model.script_dict["stochio_" + name]
            for index, _ in enumerate(self._regex_stochio.findall(mat)):
                try:
                    value = fitted_value["stochio" + str(index)]
                except KeyError:
                    res = self._regex_stochio.search(mat)
                    value = mat[res.start()+1:res.end()]
                mat = self._regex_stochio.sub(str(value), mat, 1)
            f = self._physical_computer.compute_f(mat)
            index = self._stack_name_list.index(name)
            self._parmeters["f"][index] = f
            self._parmeters["material"][index] = mat
        for name in self._all_prof:
            index = self._stack_name_list.index(name)
            f = self._physical_computer.compute_f(self._parmeters["material"]
                                                  [index])
            self._parmeters["f"][index] = f
        return self.__class__.simulate(self)
