# -*- coding: utf8 -*-
"""
To create a pipeline for combined XRR then combined XRR and GiXRF.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import paf.filter_base as filter_
import paf.data
import paf.port as port
import pyxcel.engine.pipeline as pipeline
import pyxcel.engine.optimization.fom as fom
from pyxcel.engine.optimization.generic import ParaTab
import pyxcel.engine.modeling.pumps as pumps
import pyxcel.engine.modeling.entity as entity
import pyxcel.engine.optimization.generic as old_opti
from pyxcel.uni import uni
import pyxcel.engine.optimization.scipy_d_e_combined as opti_scipy
from operation.combined import FomSelector
MAKE_DATA = paf.data.make_data


class TabEditor(filter_.Filter):
    """ filter to edit fit parameter table
    """
    def __init__(self, treatment_func):
        """ initialization
        """
        self._treatment_func = treatment_func

    def run(self):
        para_tab = ParaTab()
        para_tab.string_value = self.get_data("main").value
        new_tab = self._treatment_func(para_tab)
        self.fill_port("main", MAKE_DATA(new_tab))


class SelectData(filter_.Filter):
    """ select data on data list
    """
    def __init__(self, selector=None):
        """ initialization
        """
        if selector is None:
            selector = self.only_XRR
        self._selector = selector
        filter_.Filter.__init__(self)
        del self.input_port["main"]

        # add input port
        self.input_port["samples"] = port.Port(MAKE_DATA([]))
        self.input_port["instruments"] = port.Port(MAKE_DATA([]))
        self.input_port["experiments_datas"] = port.Port(MAKE_DATA([]))

        # add output port
        self.output_port["samples"] = port.Port(MAKE_DATA([]))
        self.output_port["instruments"] = port.Port(MAKE_DATA([]))
        self.output_port["experiments_datas"] = port.Port(MAKE_DATA([]))

    def only_XRR(self, instruments):
        """ selection of XRR-only data and exclude non-XRR data.
        """
        resultat = [False] * len(instruments)
        for idx, instrument in enumerate(instruments):
            if instrument.abstract_type == "XRRInstrument":
                resultat[idx] = True
        return resultat

    def run(self):
        """ Select some data
        """
        def select_part(data, part):
            """ select a list of data

            :param datas: list of all data
            :param part: list of boolean with true value for data to select
            """
            return [d for idx, d in enumerate(data.real_value) if part[idx]]
        part_to_select = self._selector(self.get_data("instruments"))
        samples = select_part(self.get_data("samples"), part_to_select)
        instruments = select_part(self.get_data("instruments"), part_to_select)
        experiments_datas = select_part(self.get_data("experiments_datas"),
                                        part_to_select)
        self.fill_port("samples", MAKE_DATA(samples))
        self.fill_port("instruments", MAKE_DATA(instruments))
        self.fill_port("experiments_datas", MAKE_DATA(experiments_datas))


class XRRThenCombinePipeline(pipeline.Pipeline):
    """ creating a pipeline for XRR before GiXRF and XRR
    """
    def __init__(self):
        """ initialization
        """
        pipeline.Pipeline.__init__(self, True)
        self.index = 0
        self.pump_name_list = []
        self.instrument_names = []
        self.num_connec = None
        self.nb_data_max = None
        self.clear_inf = []
        self._fom_XRR = fom.log2d
        self._fom_GiXRF = fom.chi2d
        self._fom_selector = FomSelector(self)

        # add pump
        stack = pumps.EntityPump(entity.StackData)
        self.add_element("stack", stack)

        # adding parameter pump
        pam_pump = old_opti.ParameterPump()
        self.add_element('pam_pump', pam_pump)
        self.add_to_essential("pam_pump", "tab_data",
                              uni("Parameter to optimize"))

        experimental_data_lister = old_opti.ToList()
        self.add_element("experimental_data_lister", experimental_data_lister)

        # adding first tab editor to remove stochio for XRR
        def remove_stochio_from_tab(tab):
            """ remove stochio from a tab
            """
            string_value = tab.string_value.split("\n")[1:-1]
            string_result = ""
            for line in string_value:
                line = line.split()
                try:
                    data_name, _ = line[0].split(".")
                except IndexError:
                    continue
                if data_name[:7] == "stochio":
                    line[2] = "False"
                string_result += '\n' + '\t'.join(line)
            return string_result

        first_tab_editor = TabEditor(remove_stochio_from_tab)
        self.add_element("first_tab_editor", first_tab_editor)

        # adding second tab editor to use XRR result
        def use_XRR_result(tab):
            """ remove stochio from a tab
            """

        second_tab_editor = TabEditor(use_XRR_result)
        self.add_element("second_tab_editor", second_tab_editor)

        # adding optimization XRR filter
        optimization_filter_XRR = opti_scipy.OptimisationFilter()
        optimization_filter_XRR["fom_func"] = MAKE_DATA([])
        optimization_filter_XRR["parameters"] = MAKE_DATA([])
        optimization_filter_XRR["simulators"] = MAKE_DATA([])
        optimization_filter_XRR["fom_factors"] = MAKE_DATA([])
        self.add_element("optimization_filter_XRR", optimization_filter_XRR,
                         ["end_data", "best_sim_table", "samples",
                          "instruments", "best_history", "best_result"])
        self.add_to_essential("optimization_filter_XRR", "pop_size",
                              uni("XRR population size"))
        self.add_to_essential("optimization_filter_XRR", "max_gen",
                              uni("XRR max generations"))
        self.add_to_essential("optimization_filter_XRR", "refresh_speed",
                              uni("XRR refresh rate"))

        # adding optimization combined filter
        optimization_filter_combined = opti_scipy.OptimisationFilter()
        optimization_filter_combined["fom_func"] = MAKE_DATA([])
        optimization_filter_combined["parameters"] = MAKE_DATA([])
        optimization_filter_combined["simulators"] = MAKE_DATA([])
        optimization_filter_combined["fom_factors"] = MAKE_DATA([])
        self.add_element("optimization_filter_combined",
                         optimization_filter_combined,
                         ["end_data", "best_sim_table", "samples",
                          "instruments", "best_history", "best_result"])
        self.add_to_essential("optimization_filter_combined", "pop_size",
                              uni("Combiner population size"))
        self.add_to_essential("optimization_filter_combined", "max_gen",
                              uni("Combiner max generations"))
        self.add_to_essential("optimization_filter_combined", "refresh_speed",
                              uni("Combiner refresh rate"))

        # add sample cloner
        sample_clonner = old_opti.Clone()
        self.add_element("sample_clonner", sample_clonner)

        # add lister
        sample_lister = old_opti.ToList()
        self.add_element("sample_lister", sample_lister)
        instrument_lister = old_opti.ToList()
        self.add_element("instrument_lister", instrument_lister)

        # add XRR selector
        XRR_selector = SelectData()
        self.add_element("XRR_selector", XRR_selector)

        # connect clonner
        self.connect("stack", "sample_clonner")

        # connect lister to optimizer
        self.connect('sample_lister', "XRR_selector", "list",
                     "samples")
        self.connect("XRR_selector", "optimization_filter_XRR", "samples",
                     "samples")
        self.connect('sample_lister', "optimization_filter_combined", "list",
                     "samples")

        self.connect('instrument_lister', "XRR_selector", "list",
                     "instruments")
        self.connect("XRR_selector", "optimization_filter_XRR", "instruments",
                     "instruments")
        self.connect('instrument_lister', "optimization_filter_combined",
                     "list", "instruments")

        self.connect('experimental_data_lister', "XRR_selector", "list",
                     "experiments_datas")
        self.connect("XRR_selector", "optimization_filter_XRR",
                     "experiments_datas", "experiments_datas")
        self.connect('experimental_data_lister',
                     "optimization_filter_combined", "list",
                     "experiments_datas")


# auto open methode
final_pipeline = XRRThenCombinePipeline()

# dictionnary methode :
# def final_pipeline():
#     return XRRThenCombinePipeline()
