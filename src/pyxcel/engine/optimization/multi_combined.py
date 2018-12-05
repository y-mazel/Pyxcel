# -*- coding: utf8 -*-
"""
Contain the Filter to do combined optimization data with inspyred differential
evolution or particule swarm algorithm and using a simulator.

    :platform: Unix, Windows
    :synopsis: optimisation filter to use GenX.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from random import Random
import inspyred.ec.evaluators
import inspyred.ec.terminators
import paf.data
from pyxcel.engine.optimization.scipy_d_e_combined import Problem
from pyxcel.engine.pipeline import EvolutionReport
from pyxcel.engine.optimization.generic import AbstractOptimisationFilter
from pyxcel.engine.optimization.generator_inspyred import param_generator
MAKE_DATA = paf.data.make_data


class OptimisationFilter(AbstractOptimisationFilter):
    """ combine optimization filter uzing Inspyred differnetial Evolution
    """
    def __init__(self):
        """ initialization
        """
        AbstractOptimisationFilter.__init__(self)
        self["FOM"] = Problem()
        self.add_expected_parameter("algo", MAKE_DATA(""), "DEA")

        #: fom count
        self._fom_count = 0
        self._old_fom = -1
        self._old_foms = []
        self._fit_inst = False

    def create_fom(self, pyxcel_fom):
        """ creating fom for scipy
        """
        def new_scipy_fom(x, args):
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
        return inspyred.ec.evaluators.evaluator(new_scipy_fom)

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
            self._best_history[num_iter, :-1] = self._x_best
            self._best_history[num_iter, -1] = self._old_fom
            report = EvolutionReport()
            report["FOM"] = self._old_fom
            report["FOMS"] = self._old_foms
            self._para_tab.x = self._x_best
            self.calculate_error_bar()
            report["param"] = self._para_tab.string_value
            report["corr"] = self.create_corr_matrix()
            report["corr_header"] = self._para_tab.x_label
            self._para_tab.apply_to_param(self._mod.script_dict, self._x_best)
            simu = self._mod.simulate()
            simulations = [simu[self["FOM"].born[i][0]:self["FOM"].born[i][1]]
                           for i, _ in enumerate(foms)]
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
        if optimizer_name == "DEA":
            optimizer = inspyred.ec.DEA(Random())
        elif optimizer_name == "PSO":
            optimizer = inspyred.swarm.PSO(Random())
            kwargs["neighborhood_size"] = 5
            optimizer.topology = inspyred.swarm.topologies.ring_topology
        elif optimizer_name == "GA":
            optimizer = inspyred.ec.GA(Random())
            kwargs["num_elites"] = 1
        elif optimizer_name == "ES":
            optimizer = inspyred.ec.ES(Random())
        elif optimizer_name == "SA":
            optimizer = inspyred.ec.SA(Random())
        elif optimizer_name == "EDA":
            optimizer = inspyred.ec.EDA(Random())
            kwargs["num_selected"] = 500
            kwargs["num_offspring"] = 1000
            kwargs["num_elites"] = 1
        if optimizer is not None:
            optimizer.terminator = [inspyred.ec.terminators.
                                    evaluation_termination,
                                    self.terminator]
        return (optimizer, kwargs)

    def optimize(self):
        """ optimize
        """
        pop_size = self.pop_size
        max_evaluations = self["max_gen"].value * pop_size
        optimizer, kwarg = self.get_optimizer(self["algo"].value)
        min_ = [b for b, _ in self._para_tab.bounds]
        max_ = [b for _, b in self._para_tab.bounds]
        generator = param_generator(self._para_tab.x)
        generator = inspyred.ec.generators.diversify(generator)
        optimizer.evolve(generator=generator,
                         evaluator=self._fom,
                         pop_size=pop_size,
                         bounder=inspyred.ec.Bounder(min_, max_),
                         maximize=False, max_evaluations=max_evaluations,
                         **kwarg)
        self._result = self._x_best
