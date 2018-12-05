# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
To create a pipeline for cobined optimization from data data.

    :platform: Unix, Windows
    :synopsis: module for pump creation.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import numpy as np
import paf.data
import pyxcel.engine.pipeline
import pyxcel.engine.modeling.pumps as pumps
import pyxcel.engine.database
import pyxcel.engine.simulator.xrr_no_genx as xrr
import pyxcel.engine.optimization.generic as old_opti
import pyxcel.engine.modeling.entity as entity
import pyxcel.engine.simulator.xrf_no_genx as xrf
import pyxcel.engine.optimization.fom as fom
import pyxcel.engine.modeling.physical_parameter as phyp
import pyxcel.engine.centralizer
import pyxcel.engine.optimization.mo_combined as opti_mo
import pyxcel.engine.optimization.multi_combined as opti_multi
import pyxcel.engine.optimization.scipy_d_e_combined as opti_scipy
from paf.port import Port
from pyxcel.uni import uni
from pyxcel.controller import type_inst
MAKE_DATA = paf.data.make_data


def create_combine_inspyred():
    """ create a pipeline using inspyred
    """

    def add_spec(pipeline):
        """ add special element
        """
        pipeline.add_to_essential("optimization_filter", "algo",
                                  uni("Optimization algorithm"))
    operation = CombinedOptimization(opti_multi.OptimisationFilter())
    operation.config_special(add_spec)
    operation.fom_XRR = fom.log2d
    operation.fom_GiXRF = fom.chi2d
    return operation


def create_combine_inspyred_mo():
    """ create a pipeline using inspyred
    """

    def add_spec(pipeline):
        """ add special element
        """
        pipeline.add_to_essential("optimization_filter", "algo",
                                  uni("Optimization algorithm"))
    operation = CombinedOptimization(opti_mo.OptimisationFilter())
    operation.config_special(add_spec)
    operation.fom_XRR = fom.b_log_module
    operation.fom_GiXRF = fom.b_standart
    return operation


def create_combine_scipy():
    """ create a pipeline using inspyred
    """

    def add_spec(pipeline):
        """ add special element
        """
        pipeline.add_to_essential("optimization_filter", "polish",
                                  uni("Final refinement"))
    operation = CombinedOptimization(opti_scipy.OptimisationFilter())
    operation.config_special(add_spec)
    operation.fom_XRR = fom.log2d
    operation.fom_GiXRF = fom.chi2d
    return operation


class FomSelector(paf.data.CompositeData):
    """ composite data to select an FOM
    """
    def __init__(self, pipeline):
        """ initialization
        """
        dic = {}
        paf.data.CompositeData.__init__(self, dic)
        self._pipeline = pipeline
        self._setters = {}
        for name in pipeline.elements.keys():
            if name[:4] == "data":
                self.add_data(int(name[4:]))

    def __delitem__(self, index):
        """ del an item
        """
        del self._value[uni(index)]
        del self._setters[uni(index)]

    def __setitem__(self, key, value):
        """ set an item
        """
        paf.data.CompositeData.__setitem__(self, key, value)
        self._setters[key](value)

    def add_data(self, index):
        """ add fom setter attached to a data
        """
        self._value[uni(index)] = MAKE_DATA(self._pipeline.get_fom(index),
                                            abstract="fom_sel")
        self._setters[uni(index)] = self._pipeline.create_fom_setter(index)


class CombinedOptimization(pyxcel.engine.pipeline.Pipeline):
    """ class of pipeline for creating combine analysis
    """
    def __init__(self, opti_filter, state_saving=True):
        """ initialization

        :param opti: optimization package
        """
        pyxcel.engine.pipeline.Pipeline.__init__(self, state_saving)
        self.index = 0
        self.pump_name_list = []
        self.instrument_names = []
        self.num_connec = None
        self.nb_data_max = None
        self.clear_inf = []
        self._fom_XRR = fom.log
        self._fom_GiXRF = fom.chi2bars
        self._fom_selector = FomSelector(self)

        # add pump
        stack = pumps.EntityPump(entity.StackData)
        self.add_element("stack", stack)

        # adding parameter pump
        pam_pump = old_opti.ParameterPump()
        self.add_element('pam_pump', pam_pump, [], True)
        self.add_to_essential("pam_pump", "tab_data",
                              uni("Parameter to optimize"))

        experimental_data_filter = old_opti.ToList()
        self.add_element("experimental_data_filter", experimental_data_filter)

        # adding optimization filter
        optimization_filter = opti_filter
        optimization_filter["fom_func"] = MAKE_DATA([])
        optimization_filter["parameters"] = MAKE_DATA([])
        optimization_filter["simulators"] = MAKE_DATA([])
        optimization_filter["fom_factors"] = MAKE_DATA([])
        self.add_element("optimization_filter", optimization_filter,
                         ["end_data", "best_sim_table", "samples",
                          "instruments", "best_history", "best_result"], True)
        self.add_to_essential("optimization_filter", "pop_size",
                              uni("Population size"))
        self.add_to_essential("optimization_filter", "max_gen",
                              uni("Max generations"))
        self.add_to_essential("optimization_filter", "refresh_speed",
                              uni("Refresh rate"))

        # add sample cloner
        sample_clonner = old_opti.Clone()
        self.add_element("sample_clonner", sample_clonner)

        GenXiffierSampleLister = old_opti.ToList()
        self.add_element("GenXiffierSampleLister", GenXiffierSampleLister)
        GenXiffierInstrument = old_opti.ToList()
        self.add_element("GenXiffierInstrument", GenXiffierInstrument)

        # connecting fix element
        self.connect("stack", "sample_clonner")

        # connection on optimization filter
        self.connect('pam_pump', "optimization_filter")
        self.connect('GenXiffierSampleLister', "optimization_filter", "list",
                     "samples")
        self.connect('GenXiffierInstrument', "optimization_filter", "list",
                     "instruments")
        self.connect('experimental_data_filter', "optimization_filter", "list",
                     "experiments_datas")

    @property
    def fom_XRR(self):
        """ get fom for XRR
        """
        return self._fom_XRR

    @fom_XRR.setter
    def fom_XRR(self, value):
        """ set FOM for XRR
        """
        self._fom_XRR = value

    @property
    def fom_GiXRF(self):
        """ get fom for GiXRF
        """
        return self._fom_XRR

    @fom_GiXRF.setter
    def fom_GiXRF(self, value):
        """ set FOM for GiXRF
        """
        self._fom_GiXRF = value

    @property
    def foms(self):
        """ get list of all FOM names
        """
        opti = self.get_element("optimization_filter")
        resultat = []
        for index in range(len(opti["fom_func"].value)):
            resultat.append(self.get_fom(index))
        return resultat

    def create_fom_setter(self, index):
        """ create a new fom setter
        """
        def fom_setter(new_fom_name):
            """ new fom setter
            """
            fom_dict = pyxcel.engine.centralizer.Centralizer().option.fom_dict
            if new_fom_name in fom_dict.keys():
                opti = self.get_element("optimization_filter")
                opti["fom_func"][index] = fom_dict[new_fom_name]
                self.clear_inf[index] = (fom_dict[new_fom_name]().
                                         del_error_to_inf)
        return fom_setter

    def get_fom(self, index):
        """ get a figure of merite name
        """
        opti = self.get_element("optimization_filter")
        fom_at = opti["fom_func"][index].value
        fom_dict = pyxcel.engine.centralizer.Centralizer().option.fom_dict
        for name, fom in fom_dict.items():
            if fom_at == fom:
                return name
        return ""

    def config_special(self, spec):
        """ add special config
        """
        spec(self)

    def get_link(self, index):
        """ get list of linked instrument
        """
        links = self.get_element("optimization_filter")["links"].value
        for link in links:
            if index in link:
                return [idx for idx in link if idx != index]
        return []

    def create_links(self):
        """ recreate links from pipeline instrument name
        """
        links = []
        done = []
        for name in self.instrument_names:
            if name not in done:
                link = []
                for oth_idx, oth_name in enumerate(self.instrument_names):
                    if name == oth_name:
                        link.append(oth_idx)
                if len(link) > 1:
                    links.append(link)
                done.append(name)
        return MAKE_DATA(links)

    def load_dataset(self, name):
        """ load dataset from data file
        """
        db = pyxcel.engine.centralizer.Centralizer().database
        dataset = fom.DataSet()
        data_name = self.get_element(name)["el_name"].value
        experimental_data = db[data_name]
        instrument_name = experimental_data['Instrument_name'].value
        instrument = db[instrument_name]["default_value"]
        file_name = experimental_data["file_name"].value
        if type_inst(instrument) == "XRF":
            try:
                all_GIXRF_data = np.loadtxt(file_name, skiprows=1)
                temp_name = name + "_col"
                data_column = self.temporary_data[temp_name]
                column = data_column.value
                dataset.x = all_GIXRF_data[:, 0]
                dataset.y = all_GIXRF_data[:, column]
                dataset.error = np.sqrt(dataset.y)
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)                
        elif type_inst(instrument) == "XRR":
            try:
                load_result = np.loadtxt(file_name)
                dataset.from_two_column(load_result)
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)         
        if experimental_data["2_Theta"].value:
            dataset.x = dataset.x / 2
        self.temporary_data.real_value[name + "_dataset"] = dataset

    def add_data(self, name):
        """ new validation function
        """
        pyxcel.engine.pipeline.Pipeline.add_data(self, name)

        # accessing data
        num = self.index
        db = pyxcel.engine.centralizer.Centralizer().database
        self.pump_name_list.append("data" + str(num))

        # create element in pipeline
        data_pump = pumps.EntityPump(pyxcel.engine.database.ExperimentalData)
        data_pump["el_name"] = name
        self.add_element("data" + str(num), data_pump)
        self.get_element("GenXiffierSampleLister").new_input()
        self.get_element("GenXiffierInstrument").new_input()
        self.get_element("experimental_data_filter").new_input()
        self.get_element("sample_clonner").new_output()
        GenXiffier = phyp.ApplyPhysicalParameter()
        self.add_element("GenXiffier" + str(num), GenXiffier)

        # configure instrument type
        element = db[name]
        opti = self.get_element("optimization_filter")
        opti["fom_factors"].append(MAKE_DATA(1.))
        opti["data_names"].append(MAKE_DATA("data" + str(num)))
        instrument_name = element['Instrument_name'].value
        instrument = db[instrument_name]["default_value"]
        self.instrument_names.append(instrument_name)
        if type_inst(instrument) == "XRF":
            self.clear_inf.append(self._fom_GiXRF().del_error_to_inf)
            opti["fom_func"].append(MAKE_DATA(self._fom_GiXRF))
            value = {'config': 'theta-2theta', "line": xrf.Line(),
                     "samplen": 50}
            opti["parameters"].append(MAKE_DATA(value, composite=True))
            opti["simulators"].append(xrf.XRFGenXSimulator())
            opti["links"] = self.create_links()
        elif type_inst(instrument) == "XRR":
            self.clear_inf.append(self.fom_XRR().del_error_to_inf)
            opti["fom_func"].append(MAKE_DATA(self.fom_XRR))
            opti["parameters"].append(MAKE_DATA({"samplen": 50},
                                                composite=True))
            opti["simulators"].append(xrr.XRRGenXSimulator())
        experimental_data_filter = old_opti.ExperimentalDataFilter()
        experimental_data_filter["pump_name"] = uni("data" + str(num))
        self.add_element("experimental_data_filter" + str(num),
                         experimental_data_filter)

        # making connexion
        sink_prot = "element" + str(num)
        self.connect("data" + str(num), "experimental_data_filter" +
                     str(num))
        self.connect("experimental_data_filter" + str(num),
                     "experimental_data_filter", "experiment_data", sink_prot)
        self.connect("experimental_data_filter" + str(num), "GenXiffier" +
                     str(num), sink_port="instrument")
        self.connect("sample_clonner", "GenXiffier" + str(num), "output" +
                     str(num))
        self.connect("GenXiffier" + str(num), "GenXiffierInstrument",
                     "instrument", sink_prot)
        self.connect("GenXiffier" + str(num), "GenXiffierSampleLister",
                     "sample_name", sink_prot)

        if self.num_connec is None:
            self.connect('GenXiffier' + str(num), "optimization_filter",
                         "main", "stack_data")
            self.num_connec = num

        self.essential.add_element(self.get_element("optimization_filter")
                                   ["fom_factors"], num,
                                   uni("FOM factor " + str(num)))
        self._fom_selector.add_data(num)
        self.essential.add_element(self._fom_selector, uni(num),
                                   uni("FOM " + str(num)))

        # increment index
        self.index += 1

        # return pump name
        return "data" + str(num)

    def delete_data(self, pump_name):
        """ new delete data function
        """
        pyxcel.engine.pipeline.Pipeline.delete_data(self, pump_name)
        num = self.pump_name_list.index(pump_name)
        del self.instrument_names[num]
        del self.pump_name_list[num]
        del self.clear_inf[num]
        opti = self.get_element("optimization_filter")
        del opti["fom_func"][num]
        del opti["parameters"][num]
        del opti["simulators"][num]
        del opti["fom_factors"][num]
        del self.essential[num]
        del self.essential[uni(num)]
        del self._fom_selector[uni(num)]
        del opti["data_names"][num]
        p_name = "element" + str(num)
        del self.get_element("GenXiffierSampleLister").input_port[p_name]
        del self.get_element("GenXiffierInstrument").input_port[p_name]
        del self.get_element("experimental_data_filter").input_port[p_name]
        p_name = "output" + str(num)
        del self.get_element("sample_clonner").output_port[p_name]
        self.del_element(pump_name)
        self.del_element("experimental_data_filter" + str(num))
        self.del_element("GenXiffier" + str(num))
        if "line" + str(num) in self.essential.keys():
            del self.essential.real_value["line" + str(num)]
            index = self.essential.showing_info.index(("line" + str(num),
                                                       "line" + str(num)))
            del self.essential.showing_info[index]

        if self.num_connec == num:
            opti = self.get_element("optimization_filter")
            del opti.input_port["stack_data"].pipes[0]
            self.num_connec = None

    def recreate_pipline_part(self, name, data_name):
        """ recrate pipeline part
        """
        # configure specific port
        num = int(name[4:])
        if self.index <= num:
            # reincrement index
            self.index = num + 1

        # adding port
        p_name = "element" + str(num)
        sampleLister = self.get_element("GenXiffierSampleLister")
        sampleLister.input_port[p_name] = Port()
        instrument = self.get_element("GenXiffierInstrument")
        instrument.input_port[p_name] = Port()
        data_filter = self.get_element("experimental_data_filter")
        data_filter.input_port[p_name] = Port()
        p_name = "output" + str(num)
        sample_clonner = self.get_element("sample_clonner")
        sample_clonner.output_port[p_name] = Port()

        # recreate all element
        data_pump = pumps.EntityPump(pyxcel.engine.database.ExperimentalData)
        data_pump["el_name"] = data_name
        self.add_element(name, data_pump)

        db = pyxcel.engine.centralizer.Centralizer().database
        element = db[data_name]
        GenXiffier = phyp.ApplyPhysicalParameter()
        self.add_element("GenXiffier" + str(num), GenXiffier)
        for _ in range(num+1-len(self.clear_inf)):
            self.clear_inf.append(None)
            self.pump_name_list.append(None)
        self.pump_name_list[num] = name
        instrument_name = element['Instrument_name'].value
        instrument = db[instrument_name]["default_value"]
        self.instrument_names.append(instrument_name)
        if type_inst(instrument) == "XRF":
            self.clear_inf[num] = self.fom_GiXRF().del_error_to_inf
        elif type_inst(instrument) == "XRR":
            self.clear_inf[num] = self.fom_XRR().del_error_to_inf
        experimental_data_filter = old_opti.ExperimentalDataFilter()
        experimental_data_filter["pump_name"] = name
        self.add_element("experimental_data_filter" + str(num),
                         experimental_data_filter)

        # making connexion
        sink_prot = "element" + str(num)
        self.connect("data" + str(num), "experimental_data_filter" + str(num))
        self.connect("experimental_data_filter" + str(num),
                     "experimental_data_filter", "experiment_data", sink_prot)
        self.connect("experimental_data_filter" + str(num), "GenXiffier" +
                     str(num), sink_port="instrument")
        self.connect("sample_clonner", "GenXiffier" + str(num), "output" +
                     str(num))
        self.connect("GenXiffier" + str(num), "GenXiffierInstrument",
                     "instrument", sink_prot)
        self.connect("GenXiffier" + str(num), "GenXiffierSampleLister",
                     "sample_name", sink_prot)

        if self.num_connec is None:
            self.connect('GenXiffier' + str(num), "optimization_filter",
                         "main", "stack_data")
            self.num_connec = num

    def recreate_pipeline(self, element_config):
        """ new version for recreating dynamic part of the pipeline
        """
        for name, data in element_config.items():
            if name[:4] == "data":
                self.recreate_pipline_part(name, data['el_name'].value)
                self.load_dataset(name)

    def reinit_essential(self):
        """ add fom factor after reinitilization of the pipeline
        """
        pyxcel.engine.pipeline.Pipeline.reinit_essential(self)

        for name in self._pump_only:
            if name[:4] == "data":
                num = int(name[4:])
                self.essential.add_element(self.get_element
                                           ("optimization_filter")
                                           ["fom_factors"], num,
                                           uni("FOM factor " + str(num)))
                self._fom_selector.add_data(num)
                self.essential.add_element(self._fom_selector, uni(num),
                                           uni("FOM " + str(num)))
