# -*- coding: utf8 -*-
"""
Contain the Filter to do combined optimization data with Genx differential
evolution algorithm and using a simulator.

    :platform: Unix, Windows
    :synopsis: optimisation filter to use GenX.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import numpy as np
from random import Random
import inspyred.ec.evaluators
import inspyred.ec.generators
import inspyred.ec.terminators
import inspyred.ec.variators
import paf.data
import pyxcel.engine.optimization.fom
from pyxcel.engine.optimization.generator_inspyred import param_generator
from pyxcel.engine.pipeline import EvolutionReport
from pyxcel.engine.optimization.generic import AbstractOptimisationFilter
from pyxcel.engine.optimization.scipy_d_e_combined import Problem
MAKE_DATA = paf.data.make_data


class ParetoProblem(Problem):
    """ configurable object for computing problem to minimize
    """

    def __init__(self):
        """ initialization
        """
        Problem.__init__(self)

    def fom(self, simulation, datas, arc):
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
        fom = inspyred.ec.emo.Pareto(foms, maximize=True)
        if self._callback is not None:
            self._callback(foms, arc)
        return fom


class OptimisationFilter(AbstractOptimisationFilter):
    """ combine optimization filter uzing SciPy differnetial Evolution
    """
    def __init__(self):
        """ initialization
        """
        AbstractOptimisationFilter.__init__(self)
        self.add_expected_parameter("algo", MAKE_DATA(""), "NSGA2")
        self["FOM"] = ParetoProblem()

        #: fom count
        self._fom_count = 0
        self._best_foms = None
        self._fit_inst = False

    def create_fom(self, pyxcel_fom):
        """ creating fom for scipy
        """
        def new_scipy_fom(x, args):
            """ return a scipy fom to minimize
            """
            self._para_tab.apply_to_param(self._mod.script_dict, x)
            arc = args["_ec"].archive
            try:
                self._simu = self._mod.simulate()
                fom = pyxcel_fom(self._simu, self._data_set, arc)
            except UnboundLocalError:
                inspyred.ec.emo.Pareto([1e20
                                        for _ in range(len(self["fom_func"]))])
            return fom
        return new_scipy_fom

    def select_in_arc(self, arc):
        """ select one solution in pareto optimum
        """
        if len(arc) == 0:
            return None
        elif len(arc) == 1:
            return arc[0]
        nb_fom = len(self["fom_func"])

        def get_max(arc, index):
            """ get max of a fom in arc
            """
            max_value = 0
            for element in arc:
                if element.fitness[index] > max_value:
                    max_value = element.fitness[index]
            return max_value

        def get_min(arc, index):
            """ get max of a fom in arc
            """
            min_value = 1e1000
            for element in arc:
                if element.fitness[index] < min_value:
                    min_value = element.fitness[index]
            return min_value
        max_list = [get_max(arc, index) for index in range(nb_fom)]
        min_list = [get_max(arc, index) for index in range(nb_fom)]

        def get_min_fom(par_opt):
            """ return a value of one point in pareto solutions
            """
            fact = self["FOM"].fom_factors

            def fom_idv(idv):
                """ get fom in pareto optimum
                """
                def norm(x, max_, min_):
                    """ normalise 1 fom
                    """
                    if max_ != min_:
                        return (x-min_)/(max_-min_)
                    else:
                        return 0
                return sum([fact[index]*norm(idv.fitness[index],
                                             max_list[index],
                                             min_list[index])**2
                            for index in range(nb_fom)])
            best = None
            best_fom = 1e100
            for individu in par_opt:
                if best is None:
                    best = individu
                    best_fom = fom_idv(individu)
                    continue
                elif best_fom > fom_idv(individu):
                    best = individu
                    best_fom = fom_idv(individu)
            return best
        return get_min_fom(arc)

    def report(self, foms, arc):
        """ creating and sending report for fit evolution
        """
        self._fom_count += 1
        if len(arc) == 0:
            return
        if self._fom_count % self._refresh_speed == 0:
            best = self.select_in_arc(arc)
            self._x_best = list(best.candidate)
            self._para_tab.apply_to_param(self._mod.script_dict, self._x_best)
            simu = self._mod.simulate()
            simulations = [simu[self["FOM"].born[i][0]:self["FOM"].born[i][1]]
                           for i, _ in enumerate(best.fitness)]
            report = EvolutionReport()
            report["FOM"] = len(arc)
            report["FOMS"] = [best.fitness[idx]
                              for idx in range(len(best.fitness))]
            self._para_tab.x = self._x_best
            report["param"] = self._para_tab.string_value
            report["corr_header"] = self._para_tab.x_label
            for index, data_name in enumerate(self["data_names"].value):
                simulation = simulations[index]
                report["simulations"][data_name] = MAKE_DATA(simulation)
            self._report_notifier.signal.emit(report)

    def terminator(self, *args, **kw):
        """ terminate the fit when the filter is stop
        """
        return self._stop

    def get_optimizer(self, optimizer_name):
        """ get the optimizer
        """
        optimizer = None
        kwargs = {}
        if optimizer_name == "NSGA2":
            optimizer = inspyred.ec.emo.NSGA2(Random())
            optimizer.variator = [inspyred.ec.variators.blend_crossover,
                                  inspyred.ec.variators.gaussian_mutation]
        if optimizer is not None:
            optimizer.terminator = [inspyred.ec.terminators.
                                    evaluation_termination,
                                    self.terminator]

        return (optimizer, kwargs)

    def optimize(self):
        """ optimize
        """
        self._fom = inspyred.ec.evaluators.evaluator(self.
                                                     create_fom(self["FOM"].
                                                                fom))
        pop_size = self.pop_size
        max_evaluations = self["max_gen"].value * pop_size
        optimizer, kwarg = self.get_optimizer(self["algo"].value)
        min_ = [b for b, _ in self._para_tab.bounds]
        max_ = [b for _, b in self._para_tab.bounds]
        generator = param_generator(self._para_tab.x)
        generator = inspyred.ec.generators.diversify(generator)
        optimizer.evolve(generator=generator, evaluator=self._fom,
                         pop_size=pop_size,
                         bounder=inspyred.ec.Bounder(min_, max_),
                         maximize=False, max_evaluations=max_evaluations,
                         **kwarg)

        best = self.select_in_arc(optimizer.archive)
        self._x_best = best.candidate
        self._result = self._x_best
