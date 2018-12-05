# -*- coding: utf8 -*-
"""
Contain the Filter to do combined optimization data with Genx differential
evolution algorithm and using a simulator.

    :platform: Unix, Windows
    :synopsis: optimisation filter to use GenX.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from scipy.optimize import differential_evolution
import numpy as np
import paf.data
import pyxcel.engine.optimization.fom
from pyxcel.engine.pipeline import EvolutionReport
from pyxcel.engine.optimization.generic import AbstractOptimisationFilter
MAKE_DATA = paf.data.make_data


class Problem(paf.data.CompositeData):
    """ configurable object for computing problem to minimize by combining FOM
    """

    def __init__(self):
        """ initialization
        """
        paf.data.CompositeData.__init__(self, {}, 'Problem')
        #: list of array of theta array
        self._theta_array = []
        #: list of array of theta array length
        self._theta_array_len = []
        #: list of array of theta array length
        self._total_len = 0
        #: list of array of theta array born
        self._born = []
        #: list of figure of merit function for each simulation
        self._fom_function = []
        #: p not set
        self._p_setted = False
        #: factor for each fom
        self._factors = []
        #: fom normalizer
#         self._fom_normalizer = None
        #: dataset tab
        self._datas = None
        #: callback after each for
        self._callback = None

    def set_p(self, p):
        """ set the number of parameter to fit in fom
        """
        new_foms = [fom(p) for fom in self._fom_function]
        self._value["foms"] = MAKE_DATA(self._fom_function)
        self._fom_function = new_foms
        self._p_setted = True

    @property
    def callback(self):
        """ accessing to callback function
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """ modify callback
        """
        self._callback = callback

    @property
    def theta_array(self):
        """ getter for theta_array
        """
        return self._theta_array

    @theta_array.setter
    def theta_array(self, theta_array):
        """ setter for theta_array
        """
        self._theta_array = theta_array
        self._theta_array_len = [array_.size for array_ in theta_array]
        self._born = [(sum(self._theta_array_len[:i]),
                       sum(self._theta_array_len[:i+1]))
                      for i in range(len(theta_array))]
        self._total_len = sum(self._theta_array_len)

    @property
    def fom_func(self):
        """ accessing to individual fom function list
        """
        return self._fom_function

    @fom_func.setter
    def fom_func(self, fom_func):
        """ setter for individual fom function list
        """
        self._fom_function = fom_func

    @property
    def fom_factors(self):
        """ accessing to list of factor for each figure of merit
        """
        return self._factors

    @fom_factors.setter
    def fom_factors(self, fom_factors):
        """ setter for list of factor for each figure of merit
        """
        self._factors = fom_factors

    @property
    def born(self):
        """ list of born for each parameter
        """
        return self._born

    def combine(self, foms):
        """ combining each figure of merit
        """
        combined_fom = 0
        for index, fom in enumerate(foms):
            combined_fom += (fom * self._factors[index])
        return combined_fom

    def fom(self, simulation, datas):
        """ calculate combined figure of merit
        """
        if not self._p_setted:
            self.set_p(1)
        if self._datas is None:
            self._datas = [pyxcel.engine.optimization.fom.DataSet()
                           for _ in self._fom_function]
            for i, dataset in enumerate(self._datas):
                dataset.copy(datas)
                dataset.x = dataset.x[self._born[i][0]:self._born[i][1]]
                dataset.y = dataset.y[self._born[i][0]:self._born[i][1]]
                dataset.error = dataset.error[self._born[i][0]:
                                              self._born[i][1]]
        simulations = [simulation[self._born[i][0]:self._born[i][1]]
                       for i, _ in enumerate(self._fom_function)]
        for sim in simulations:
            sim[np.isinf(sim)] = 0
        foms = [fom(simulations[i], self._datas[i])
                for i, fom in enumerate(self._fom_function)]
        fom = self.combine(foms)
        if self._callback is not None:
            self._callback(fom, foms)
        return fom

    def to_xml(self, xml_doc, xml_parrent, name):
        if "foms" not in self._value.keys():
            self._value["foms"] = MAKE_DATA(self._fom_function)
        paf.data.CompositeData.to_xml(self, xml_doc, xml_parrent, name)

    def set_from_xml(self, xml_element):
        paf.data.CompositeData.set_from_xml(self, xml_element)
        self._fom_function = self._value["foms"].value


class OptimisationFilter(AbstractOptimisationFilter):
    """ combine optimization filter using SciPy differnetial Evolution
    """
    def __init__(self):
        """ initialization
        """
        AbstractOptimisationFilter.__init__(self)
        self["FOM"] = Problem()

        # add special parameter
        self.add_expected_parameter("polish", MAKE_DATA(False), False)

        #: fom count
        self._fom_count = 0
        self._old_foms = []
        self._fit_inst = False

    def create_fom(self, pyxcel_fom):
        """ creating fom for scipy
        """
        def new_scipy_fom_error(x):
            """ return a scipy fom to minimize
            """
            self._x = x
            self._para_tab.apply_to_param(self._mod.script_dict, x)
            try:
                self._simu = self._mod.simulate()
                fom = pyxcel_fom(self._simu, self._data_set)
                if fom < self.worst_error_fom:
                    self.set_worst_error(x, fom)
            except UnboundLocalError:
                fom = 1e20
            return fom

        def new_scipy_fom(x):
            """ return a scipy fom to minimize
            """
            self._x = x
            self._para_tab.apply_to_param(self._mod.script_dict, x)
            try:
                self._simu = self._mod.simulate()
                fom = pyxcel_fom(self._simu, self._data_set)
            except UnboundLocalError:
                fom = 1e20
            return fom
        if self["polish"].value:
            return new_scipy_fom
        else:
            return new_scipy_fom_error

    def report(self, fom, foms):
        """ creating and sending report for fit evolution
        """
        self._fom_count += 1
        if (self._old_fom > fom) or (self._old_fom == -1):
            self._old_fom = fom
            self._old_foms = foms
            self._x_best = self._x
            self._simu_best = self._simu
        if self._fom_count % self._refresh_speed == 0:
            num_iter = self._fom_count / self._refresh_speed - 1
            if num_iter < self["max_gen"].value+1:
                self._best_history[num_iter, :-1] = self._x_best
                self._best_history[num_iter, -1] = self._old_fom
            report = EvolutionReport()
            report["FOM"] = self._old_fom
            report["FOMS"] = self._old_foms
            report["corr"] = self.create_corr_matrix()
            report["corr_header"] = self._para_tab.x_label
            self._para_tab.x = self._x_best
            self.calculate_error_bar()
            report["param"] = self._para_tab.string_value
            self._para_tab.apply_to_param(self._mod.script_dict, self._x_best)
            simu = self._mod.simulate()
            simulations = [simu[self["FOM"].born[i][0]:self["FOM"].born[i][1]]
                           for i, _ in enumerate(foms)]
            for index, data_name in enumerate(self["data_names"].value):
                simulation = simulations[index]
                report["simulations"][data_name] = MAKE_DATA(simulation)
            self._report_notifier.signal.emit(report)

    def callback(self, *args, **kw):
        """ callback for scipy optimization
        """
        if self._stop:
            self._fom(args[0])
        return self._stop

    def optimize(self):
        """ optimize
        """
        self._old_fom = -1

        pop_size = self["pop_size"].value
        maxiter = self["max_gen"].value
        polish = self["polish"].value
        self._fom(self._para_tab.x)
        result = differential_evolution(self._fom,
                                                       self._para_tab.bounds,
                                                       popsize=pop_size,
                                                       maxiter=maxiter,
                                                       polish=polish,
                                                       atol=0.,
                                                       tol=0.,
                                                       callback=self.callback)
        self._result = result.x
