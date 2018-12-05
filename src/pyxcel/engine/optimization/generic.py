# -*- coding: utf8 -*-
"""
Contain the Filter to do combined optimization data using a simulator.

    :platform: Unix, Windows
    :synopsis: optimisation filter

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import re
import copy
import numpy as np
import pyxcel.engine.centralizer
import paf.filter_base
import paf.data
import paf.port as port
import pyxcel.engine.optimization.fom
import pyxcel.engine.modeling.tools as tools
from pyxcel.engine.pipeline import EvolutionReport
from pyxcel.view.cute import QObject, pyqtSignal
from pyxcel.controller import type_inst
from pyxcel.engine.modeling.entity import StackData
import cmd
from cmd import Cmd
MAKE_DATA = paf.data.make_data


class ExperimentalDataFilter(paf.filter_base.Filter):
    """ filter to extract instrument and experimental data from database
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)
        temp_port = port.Port(MAKE_DATA())
        self.output_port["experiment_data"] = temp_port
        self.add_expected_parameter("pump_name", MAKE_DATA(""), "data")
        self.add_expected_parameter("temporary_data", MAKE_DATA(), MAKE_DATA())

        # editing showing info
        del self.showing_info[-1]

    def run(self):
        """ running
        """
        # initialize data
        experimental_data = self.get_data("main").value
        file_name = experimental_data["file_name"]
        pump_name = self["pump_name"].value

        # send data
        data = self["temporary_data"][pump_name + "_dataset"]
        self.fill_port("experiment_data", MAKE_DATA(data))

        # send instrument
        db = pyxcel.engine.centralizer.Centralizer().database
        experimental_data = db[file_name]
        instrument_name = experimental_data['Instrument_name'].value
        if type_inst(db[instrument_name]["default_value"]) == "XRF":
            temp_name = pump_name + "_col"
            data_column = self["temporary_data"][temp_name]
            column = data_column.value
            GIXRF_file_header = open(file_name).readline().split()
            column_name = GIXRF_file_header[column]
            instrument_name += "_" + column_name
        instrument = self["temporary_data"][instrument_name]
        instrument["name"] = instrument_name
        self.fill_port("main", instrument)


class ParaTab(object):
    """ represent a parameter tab
    """
    def __init__(self):
        """ initialization
        """
        self._source_elements = ["I0"]
        self._detector_elements = ["dist", "pinhole_height",
                                   "width_parallel_l", "width_parallel_s",
                                   "res", "Ibkg"]
        #: boundary off each parameter formated for scipy
        self._bounds = []
        #: list of parameter to fit
        self._params = []
        #: contain the groupe list
        self._groups = []
        #: stirng value formated for GenX.
        self._string_value = ""
        #: actual value of parameter
        self._x = []
        #: error bars of the parameter
        self._error = []
        #: list of name of each layer for the stack model
        self._stack_name_list = None
        #: regular expression for finding stochio
        self._regex_stochio = re.compile("_\d*\.?\d*")

    def _apply_column(self, index, value):
        """ apply a value vector to a column
        """
        lines = self._string_value.split("\n")
        new_string_value = lines[0]
        tab_lines = lines[1:]
        dic_group = {}
        group_list = self.groups
        diff_idx = 0
        for idx, tab_line in enumerate(tab_lines):
            if len(tab_line) < 5:
                continue
            new_tabline = tab_line.split()
            idx_value = idx - diff_idx
            if new_tabline[-1] != "None":
                if new_tabline[-1] in group_list:
                    group_list.remove(new_tabline[-1])
                    dic_group[new_tabline[-1]] = idx_value
                else:
                    diff_idx += 1
                    idx_value = dic_group[new_tabline[-1]]
            new_tabline[index] = str(value[idx_value])
            if eval(new_tabline[2]):
                new_string_value += '\n' + '\t'.join(new_tabline)
            else:
                diff_idx += 1
                new_string_value += '\n' + '\t'.join(tab_line)
        self._string_value = new_string_value

    @property
    def layer_rank(self):
        """ accessing to layer rank
        """
        return self._layer_rank

    @property
    def bounds(self):
        """ accessing to bounds
        """
        return self._bounds

    @property
    def params(self):
        """ accessing to fitted parameter list
        """
        return self._params

    @property
    def x_label(self):
        """ return the params with all member of groups replace by first member
        named by group name
        """
        x_label = copy.copy(self.params)
        group_list = []
        diff_idx = 0
        for idx, groupe in enumerate(self.groups):
            if groupe != "None":
                if groupe in group_list:
                    del x_label[idx-diff_idx]
                    diff_idx += 1
                else:
                    x_label[idx-diff_idx] = groupe
        return x_label

    @property
    def x(self):
        """ accesssing to x vector
        """
        return self._x

    @x.setter
    def x(self, value):
        """ setter for x value
        """
        self._x = list(value)
        self._apply_column(1, value)

    @property
    def error(self):
        """ accessing to error bar
        """
        return self._error

    @error.setter
    def error(self, value):
        """ setter for error value
        """
        self._error = list(value)
        self._apply_column(5, value)

    @property
    def groups(self):
        """ return list of groups *only one by name*
        """
        list_groups = list(set(self._groups))
        list_groups.remove("None")
        return list_groups

    @property
    def string_value(self):
        """ acces to the string value
        """
        return self._string_value

    @string_value.setter
    def string_value(self, value):
        """ load from a string value

        :param value: string value
        :type value: str
        """
        self._string_value = value
#         print("value " + value)             ###
        tab = value.split("\n")[1:-1]
#         for t in tab:                       ###
#             print("tab " + t)               ###
        self._bounds = []
        self._params = []
        self._x = []
        self._error = []
        self._groups = []
        group_list = []
        for tab_line in tab:                
#             print("tab_line " + tab_line)   ###
            line = tab_line.split()
#             for l in line:                  ###
#                 print("line " + l)          ###
            if eval(line[2]):
                self._params.append(line[0])
                self._groups.append(line[-1])
                if line[-1] != "None":
                    if line[-1] in group_list:
                        continue
                    else:
                        group_list.append(line[-1])
                self._bounds.append((float(line[3]), float(line[4])))
                self._x.append(float(line[1]))
                try:
                    self._error.append(float(line[5]))
                except ValueError:
                    self._error.append(0.)

    def load_from_file(self, file_name):
        """ load parameter tab from file

        :param file_name: name of the file
        :type file_name: str
        """
        with open(file_name, "r") as f:
            tab_string = f.read()
            self.string_value = tab_string

    def apply_to_genx_dict(self, genx_dict, x=None):
        """ apply to a dictionary of genx element
        """
        if x is None:
            x = self.x
        for idx, param in enumerate(self.params):
            str_statement = param + '(' + str(x[idx]) + ')'
            exec(str_statement, genx_dict)
        self.x = x

    def get_data_to_modify(self, pyxcel_dict, data_name, key):
        """ get the data to modify
        """
        to_edit = None
        if key in self._source_elements:
            to_edit = pyxcel_dict[data_name]['source']
        elif key in self._detector_elements:
            to_edit = pyxcel_dict[data_name]['detector']
        else:
            list_stack = []
            for temporary_element_name in pyxcel_dict.keys():
                temporary_element = (pyxcel_dict[temporary_element_name])
                if isinstance(temporary_element, StackData):
                    if temporary_element_name[-4:] != "save":
                        list_stack.append(temporary_element)
            stack = list_stack[0]
            if stack['ambient']["name"].value == data_name:
                to_edit = stack['ambient']
            elif stack['substrate']["name"].value == data_name:
                to_edit = stack['substrate']
            else:
                stack = stack['layers']
                for layer in stack:
                    if layer['name'].value == data_name:
                        to_edit = layer

        return to_edit

    @staticmethod
    def get_var_name(line):
        """ get variable name from line
        """
        key_name_up = line[0].split(".")[1][3:]
        key_name = key_name_up[0].lower() + key_name_up[1:]
        maj_list = ["I0", "Ibkg"]
        if key_name_up in maj_list:
            key_name = key_name_up
        return key_name

    def apply_stochio(self, pyxcel_dict, line):
        """ apply stochio to mpyxceldict
        """
        data_name = line[0].split(".")[0][8:]
        index = int(line[0].split(".")[1][10:])
        to_edit = self.get_data_to_modify(pyxcel_dict, data_name, "material")
        mat = to_edit['material'].value
        actual = 0
        value = line[1]
        for idx, _ in enumerate(self._regex_stochio.findall(mat)):
            if idx == index:
                # value is rounded to 3 digits
                mat = self._regex_stochio.sub(str(round(float(value),2)), mat, 1)
                break
            else:
                res = self._regex_stochio.search(mat)
                actual += res.end()
                mat = mat[res.end():]
        to_edit['material'] = to_edit['material'].value[:actual] + mat

    def apply_to_dict(self, pyxcel_dict, x=None):
        """ apply to a dictionary of element
        """
        if x is not None:
            self.x = x
        tab_string = self.string_value
        tab_lines = tab_string.split("\n")[1:]
        tab_lines.sort(reverse=True) # circumvent multiple stoichiometric coefficients fitting on the same material
        for tab_line in tab_lines:
            line = tab_line.split()
            try:
                data_name, var_name = line[0].split(".")
            except IndexError:
                return
            if data_name[:7] == "stochio":
                self.apply_stochio(pyxcel_dict, line)
                continue
            elif var_name[:11] == "setProfile_":
                self.apply_to_profile(pyxcel_dict, line)
                continue
            key_name = self.get_var_name(line)
            to_edit = self.get_data_to_modify(pyxcel_dict, data_name, key_name)
            if key_name == "numerical_density":
                oth_dens = tools.calc_mass_density(float(line[1]),
                                                   to_edit["material"])
                to_edit["mass_density"] = oth_dens
            if key_name == "mass_density":
                oth_dens = tools.calc_num_density(float(line[1]),
                                                  to_edit["material"])
                to_edit["numerical_density"] = oth_dens
            to_edit[key_name] = float(line[1])

    def apply_to_profile(self, pyxcel_dict, line):
        """ apply a line to profile
        """
        data_name, var_name = line[0].split(".")
        var_name = var_name[11:]
        stack = None
        profile = None
        for name in pyxcel_dict.keys():
            element = pyxcel_dict[name]
            if isinstance(element, StackData):
                if name[-4:] != "save":
                    stack = element
                    break
        for lay in stack.real_value["layers"]:
            if lay["name"].value == data_name:
                profile = lay["materials"]
                layer = lay
                break
        if var_name == "d":
            layer.d = float(line[1])
        elif var_name == "sigmar":
            if "parameters" in pyxcel_dict.keys():
                parameters = pyxcel_dict["parameters"]
                index = list(parameters["name"]).index(data_name + "_start")
                parameters["sigmar"][index] = float(line[1])
            else:
                layer["sigmar"] = float(line[1])
        else:
            try:
                idx = int(var_name[:var_name.index("_")])
                var_name = var_name[var_name.index("_")+1:]
                profile["computers"][idx]["kwargs"][var_name] = float(line[1])
            except ValueError:
                var_name = var_name[var_name.index("_")+1:]
                layer["densities"][var_name] = float(line[1])

    def recalculate_profile(self, pyxcel_dict, profile_name):
        """ recalculate profile
        """
        stack = None
        profile = None
        for name in pyxcel_dict.keys():
            element = pyxcel_dict[name]
            if isinstance(element, StackData):
                if name[-4:] != "save":
                    stack = element
                    break
        for lay in stack.real_value["layers"]:
            if lay["name"].value == profile_name:
                profile = lay
        parameters = pyxcel_dict["parameters"]
        if self._stack_name_list is None:
            self._stack_name_list = list(parameters['name'])
        start = self._stack_name_list.index(profile_name + "_start")
        end = self._stack_name_list.index(profile_name + "_end")
        new_param = profile.to_param()
        parameters["material"][end:start+1] = new_param["materials"][::-1]
        parameters["d"][end:start+1] = new_param["d"][::-1]
        num_dens = parameters["numerical_density"]
        num_dens[end:start+1] = new_param["num_densities"][::-1]
        mass_dens = parameters["mass_density"]
        mass_dens[end:start+1] = new_param["mass_densities"][::-1]

    def apply_to_other(self, pyxcel_dict, line):
        """ apply instrument or stochio line to pyxcel dict
        """
        key = self.get_var_name(line)
        data_name = line[0].split(".")[0]
        # to_edit = 0.  # {key: 0.}
        if key in self._source_elements:
            to_edit = pyxcel_dict[data_name]['source']
        elif key in self._detector_elements:
            to_edit = pyxcel_dict[data_name]['detector']
        else:
            to_edit = pyxcel_dict[data_name]
        to_edit[key] = float(line[1])

    def apply_to_param(self, pyxcel_dict, x=None):
        """ apply tab on model parameter
        """
        recalculate_profile = []
        parameters = pyxcel_dict["parameters"]
        if x is not None:
            self.x = x
        if self._stack_name_list is None:
            self._stack_name_list = list(parameters['name'])
        tab_string = self.string_value
        tab_lines = tab_string.split("\n")[1:]
        for tab_line in tab_lines:
            line = tab_line.split()
            try:
                data_name, var_name = line[0].split(".") ### plante car line [0]==instru+intitulécolonne+param, si pas de header colonne, intitulé == xxx.yyy (nombre) => 2 points dans string
            except IndexError:
                return
            if self._stack_name_list.count(data_name) > 0:
                actual_index = 0
                for _ in range(self._stack_name_list.count(data_name)):
                    index = (self._stack_name_list[actual_index:]
                             .index(data_name) + actual_index)
                    actual_index = index
                    key_name = self.get_var_name(line)
                    if key_name == "numerical_density":
                        mat = parameters["material"][index]
                        oth_dens = tools.calc_mass_density(float(line[1]), mat)
                        parameters["mass_density"][index] = oth_dens
                    if key_name == "mass_density":
                        mat = parameters["material"][index]
                        oth_dens = tools.calc_num_density(float(line[1]), mat)
                        parameters["numerical_density"][index] = oth_dens
                    parameters[key_name][index] = float(line[1])
            elif var_name[:11] == "setProfile_":
                self.apply_to_profile(pyxcel_dict, line)
                recalculate_profile.append(data_name)
            else:
                self.apply_to_other(pyxcel_dict, line)
        if len(recalculate_profile) > 0:
            recalculate_profile = list(set(recalculate_profile))
            for profile in recalculate_profile:
                self.recalculate_profile(pyxcel_dict, profile)


class ReportNotifier(QObject):
    """ notifier object
    """
    #: notifier signal
    _signal = pyqtSignal(EvolutionReport)

    @property
    def signal(self):
        """ property for accessing signal
        """
        return self._signal


class ParameterPump(paf.pump_base.Pump):
    """ pump for parameter to fit list
    """
    def __init__(self):
        """ initialization
        """
        paf.pump_base.Pump.__init__(self)
        self.add_expected_parameter("tab_data",
                                    MAKE_DATA({"text": ""}, composite=True,
                                              abstract='tab_data'),
                                    MAKE_DATA({"text": ""}, composite=True,
                                              abstract='tab_data'))
        self.add_expected_parameter("temporary_data",
                                    pyxcel.engine.pipeline.TemporaryData(),
                                    pyxcel.engine.pipeline.TemporaryData())

    def run(self):
        """ running pump
        """
        input_value = self["tab_data"]["text"]
        if input_value._value != '':
            self.fill_port("main", input_value)
        else:
            raise AttributeError("Parameter table is empty!")

    def to_composite_data(self):
        """ rewrite to update before access to tab_data value
        """
        try:
            self["tab_data"] = self["temporary_data"]['new_tab']
        except:
            pass
        return paf.pump_base.Pump.to_composite_data(self)

    def stop(self):
        """ stoping pump
        """
        paf.pump_base.Pump.stop(self)
        try:
            self["temporary_data"]["old_tab"] = self["tab_data"]
            self["tab_data"] = self["temporary_data"]['new_tab']
        except KeyError:
            pass


class ToList(paf.filter_base.Filter):
    """ transform N input to a list of N element
    """
    def __init__(self):
        """ initialization

        :param nb_input: number of input port
        :type nb_input: int
        """
        paf.filter_base.Filter.__init__(self)
        del self.input_port["main"]
        self.output_port["list"] = port.Port(MAKE_DATA([]))
        self.add_expected_parameter("index", MAKE_DATA(0), 0)

    def new_input(self):
        """create a new input
        """
        index = self["index"].value
        self.input_port["element" + str(index)] = port.Port(MAKE_DATA())
        self["index"] = index + 1

    @property
    def nb_input_port(self):
        """ return number of input port
        """
        return len(self.input_port)

    def run(self):
        """ running
        """
        out = MAKE_DATA([])
        for port_name in sorted(list(self.input_port.keys())):
            out.append(self.get_data(port_name))
        self.fill_port("list", out)


class Clone(paf.filter_base.Filter):
    """ clone an entry object to nb_output object (distinct)
    """
    def __init__(self):
        """ initialization

        :param nb_output: number of output port
        :type nb_output: int
        """
        paf.filter_base.Filter.__init__(self)
        del self.output_port["main"]
        self.add_expected_parameter("index", MAKE_DATA(0), 0)

    def new_output(self):
        """ create a new output
        """
        index = self["index"].value
        self.output_port["output" + str(index)] = port.Port(MAKE_DATA())
        self["index"] = index + 1

    @property
    def nb_output_port(self):
        """ return number of input port
        """
        return len(self.output_port)

    def run(self):
        """ running
        """
        for port_name in sorted(list(self.output_port.keys())):
            new_data = paf.data.copy_data(self.get_data("main"))
            self.fill_port(port_name, new_data)


class CustomModel(object):
    """ a model using custom simulator...
    """
    def __init__(self):
        """ initialization
        """
        self._script_dict = {}
        self._fom = None
        self._instruments = []
        self._sample = None

    @property
    def sample(self):
        """ return a sample
        """
        return self._sample

    @property
    def instruments(self):
        """ return list of instrument
        """
        return self._instruments

    @property
    def fom(self):
        """ access to fom function
        """
        return self._fom

    @fom.setter
    def fom(self, value):
        """ modify fom
        """
        self._fom = value

    @property
    def script_dict(self):
        """ property to access to the script module dictionary
        """
        return self._script_dict

    def add_stochio(self, stochio):
        """ add stoichiometric parameter
        """
        for key in list(stochio.keys()):
            #print key
            cmmd = key + " = {}\n"
            for idex, item in enumerate(stochio[key][:]):
                cmmd += key + "['stochio_" + str(idex) + "'] = "
                cmmd += str(item) + "\n"
            cmmd += key + "['mass_dens'] = " + str(stochio[key][-1:][0])
            cmmd += "\n"
            exec(cmmd,  self.script_dict)
            

    def add_sample(self, samples):
        """ add some sample
        """
        self._sample = samples[0]
        for sample in samples:
            for key in sample.keys():
                self.script_dict[key] = sample[key]

    def add_instrument(self, instruments):
        """ add some instrument
        """
        for key in instruments.keys():
            self.script_dict[key] = instruments[key]
            self._instruments.append(instruments[key])

    def add_simulator_script(self, simulators):
        """ create script simulator from a list of Simulator object.

        :param simulators: list of simulator
        """
        self.script_dict["simulators"] = simulators

        def simulate(simulators):
            result = np.array([], dtype=np.float64)
            for simulator in simulators: # proper simulation
                result = np.concatenate((result, simulator.simulate()))
            return result

        self.script_dict["simulate"] = simulate
        self.compiled = True
        s = 'def Sim():\n\treturn simulate(simulators)\n'
        exec(s, self.script_dict)

    def simulate(self):
        """ execute simulator
        """
        return self.script_dict["Sim"]()


class LinkData(paf.data.CompositeData):
    """ create a new setitem function
    """
    def __init__(self, origine=None, parts=None):
        """ initialization
        """
        #: list of excluded parameter
        self._excluded_par = ["I0"]
        paf.data.CompositeData.__init__(self)
        if origine is not None:
            self._value = origine.real_value
            self._data_type = dict
            self._showing_info = origine.showing_info
            self._abstract_data_type = origine.abstract_type
            self._parts = parts
            self._origine = origine

    @property
    def excluded_par(self):
        """ get list of exclude parameter
        """
        return self._excluded_par

    @excluded_par.setter
    def excluded_par(self, value):
        """ setter for excluded parameter
        """
        self._excluded_par = value

    def to_origine(self):
        """ tranform Link data to original data with new value
        """
        self._origine.real_value = self._value
        return self._origine

    def new_setter(self, key, value):
        """ new setter
        """
        for part in self._parts:
            paf.data.CompositeData.__setitem__(part, key, value)

    def __setitem__(self, key, value):
        """ new __setitem__ for link instrument
        """
        if key in self._excluded_par:
            paf.data.CompositeData.__setitem__(self, key, value)
        else:
            self.new_setter(key, value)


def link_instrument(instruments):
    """ create a link between instruments

    :param instruments: a list of pyxcel instrument
    """

    detectors = [inst["detector"] for inst in instruments]
    sources = [inst["source"] for inst in instruments]
    for instrument in instruments:
        instrument["detector"] = LinkData(instrument["detector"], detectors)
        instrument["source"] = LinkData(instrument["source"], sources)


def unlink_instrument(instruments):
    """ create a link between instruments

    :param instruments: a list of pyxcel instrument
    """

    for instrument in instruments:
        instrument["detector"] = instrument["detector"].to_origine()
        instrument["source"] = instrument["source"].to_origine()


class AbstractOptimisationFilter(paf.filter_base.Filter):
    """ combine optimization filter uzing SciPy differnetial Evolution
    """
    def __init__(self):
        """ initialization
        """
        paf.filter_base.Filter.__init__(self)
        centralizer = pyxcel.engine.centralizer.Centralizer()

        # input port
        self.input_port["experiments_datas"] = port.Port(MAKE_DATA())
        self.input_port["instruments"] = port.Port(MAKE_DATA([]))
        self.input_port["samples"] = port.Port(MAKE_DATA([{}]))
        self.input_port["stack_data"] = port.Port()

        # output port
        self.output_port["start_data"] = port.Port()  # TODO: delete
        self.output_port["end_data"] = port.Port()
        self.output_port["best_sim_table"] = port.Port()
        self.output_port["instruments"] = port.Port()
        self.output_port["samples"] = port.Port()
        self.output_port["best_history"] = port.Port()
        self.output_port["best_result"] = port.Port()

        # add expected parameter
        self.add_expected_parameter("pop_size", MAKE_DATA(10), 10)
        self.add_expected_parameter("fom_factors", MAKE_DATA([]), [])
        self.add_expected_parameter("FOM", MAKE_DATA(), MAKE_DATA())
        self.add_expected_parameter("parameters", MAKE_DATA([]), [])
        self.add_expected_parameter("fom_func", MAKE_DATA([]), [])
        self.add_expected_parameter("max_gen", MAKE_DATA(50),
                                    centralizer.option.default_max_gen)
        self.add_expected_parameter("simulators", MAKE_DATA([]),
                                    MAKE_DATA([]))
        self.add_expected_parameter("data_names", MAKE_DATA([]),
                                    MAKE_DATA([]))
        self.add_expected_parameter("links", MAKE_DATA([]), [])
        self.add_expected_parameter("refresh_speed", MAKE_DATA(1), 1)

        #: report notifier
        self._report_notifier = ReportNotifier()

        #: selected element for computing error bars with FOM value
        self._selected_error_set = None
        self._best_history = None

        #: table of parameter
        self._para_tab = ParaTab()

    @property
    def model(self):
        """ property for accessing to the model
        """
        return self._mod

    @property
    def report_notifier(self):
        """ accessing to report notifier
        """
        return self._report_notifier

    @property
    def fit_stochio(self):
        """ return True if simulator must recalculate stochio dependent
        parameter

        :return: True if simulator must recalculate stochio dependent parameter
        :rtype: boolean
        """
        return self._fit_stochio

    @property
    def fit_inst(self):
        """ ruturn True if we need to fit instrument
        """
        return self._fit_inst

    @property
    def pop_size(self):
        """ get the population size
        """
        if self._para_tab.string_value == "":
            self._para_tab.string_value = self.get_data("main").value
        nb_para = len(self._para_tab.bounds)
        return self["pop_size"].value * nb_para

    @property
    def worst_error_fom(self):
        """ accessing to worst error fom
        """
        fom_error_set = self._selected_error_set[:, -1]
        if (fom_error_set == 0.).any():
            return np.infty
        else:
            return np.max(fom_error_set)

    def set_worst_error(self, x, fom):
        """ set the error set for the worst FOM with new X and FOM
        """
        worst_fom = self.worst_error_fom
        if np.isinf(worst_fom):
            worst_fom = 0
        index = int(np.where(self._selected_error_set[:, -1:] == worst_fom)[0]
                    [0])
        new_value = np.concatenate((np.array(x), np.array([fom])))
        self._selected_error_set[index] = new_value

    def create_corr_matrix(self):
        ligne_list = self._selected_error_set[:, -1] != 0.
        x_list = self._selected_error_set[ligne_list, :-1].T
        corr = np.corrcoef(x_list)
        return corr

    def calculate_error_bar(self):
        """ calculate error bar for each parameter
        """
        # select all element with FOM != 0
        ligne_list = self._selected_error_set[:, -1] != 0.
        x_list = self._selected_error_set[ligne_list, :-1]
        error_bars = np.std(x_list, 0)
        self._para_tab.error = error_bars.tolist()

    def stop(self):
        """ stopping filter
        """
        self._stop = True

    def run(self):
        """ operation function
        """
        # load parameter
        string_value = self.get_data("main").value
        if string_value.count("stochio") or string_value.count("Profile"):
            self._fit_stochio = True
        else:
            self._fit_stochio = False
        if (string_value.count("setDist") or
                string_value.count("setPinhole_height") or
                string_value.count("setWidth_parallel_l") or
                string_value.count("setWidth_parallel_s")):
            self._fit_inst = True
        else:
            self._fit_inst = False
        self._para_tab.string_value = string_value

        # record refresh speed
        self._refresh_speed = (self["refresh_speed"].value *
                               self["pop_size"].value *
                               len(self._para_tab.bounds))

        # create model
        self._mod = CustomModel()
        samples = self.get_data("samples")
        self._mod.add_sample(samples.value)
        self._insts = self.get_data("instruments")
        self._mod.add_instrument({inst["name"].value: inst
                                  for inst in self._insts})
        self._sims = self["simulators"]
        self._mod.add_simulator_script(self._sims)

        # add stochio
        if self.fit_stochio:
            self._mod.add_stochio(self.get_data("stack_data").stochio)

        # link instrument
        links = self["links"].value
        for link in links:
            inst_to_link = [self._insts[idx] for idx in link]
            link_instrument(inst_to_link)

        # parameter and create for FOM
        self["FOM"].fom_func = self["fom_func"].value
        self["FOM"].set_p(len(self._para_tab.bounds))

        # parameter for experimental data
        exp_data = self.get_data("experiments_datas")
        theta_arrays = []
        for index in range(len(exp_data)):
            self["FOM"].fom_func[index].del_error_to_inf(exp_data[index])
            theta_arrays.append(exp_data[index].x)

        # parameter rest of FOM
        self["FOM"].fom_factors = self["fom_factors"].value
        self["FOM"].callback = self.report
        self._fom = self.create_fom(self["FOM"].fom)
        self["FOM"].theta_array = theta_arrays

        # parameter for simulators
        for index, simulator in enumerate(self._sims):
            simulator["parameter"] = self["parameters"][index]
            simulator["theta_array"] = theta_arrays[index]
            simulator["stack"] = samples[index].value['sample']
            simulator["instrument"] = self._insts[index]
            simulator.initialization(self)
        self._mod.script_dict["parameters"] = self._sims[0].model_parameters
        for simulator in self._sims.real_value[1:]:
            mp = simulator.model_parameters
            new_mp = self._mod.script_dict["parameters"]
            mp['d'] = new_mp['d']
            mp['sigmar'] = new_mp['sigmar']
            mp['numerical_density'] = new_mp['numerical_density']
            mp['mass_density'] = new_mp['mass_density']
            # print("pyxcel/engine/optimization/generic.py/AbstractOptimizationFilter.run()")
            for idx, each in enumerate(new_mp['material']): # edit simulator.model_parameters["material"] to remove "_"'s
                new_mp['material'][idx] = each.replace("_","")
            mp['material'] = new_mp['material'] 

        # parameter and optimization
        self._data_set = pyxcel.engine.optimization.fom.DataSet()
        for exp in exp_data:
            self._data_set.x = np.concatenate((self._data_set.x, exp.x))
            self._data_set.y = np.concatenate((self._data_set.y, exp.y))
            self._data_set.error = np.concatenate((self._data_set.error,
                                                   exp.error))

        # create error bar population calculating base
        self._selected_error_set = np.zeros((self.pop_size,
                                             len(self._para_tab.bounds)+1))
        self._best_history = np.zeros((self["max_gen"].value+1,
                                       len(self._para_tab.bounds)+1))

        self.optimize()

        # unlink instrument
        for link in links:
            inst_to_unlink = [self._insts[idx] for idx in link]
            unlink_instrument(inst_to_unlink)

        # send data
        self._para_tab.apply_to_dict(self["temporary_data"], self._result)
        self._para_tab.apply_to_param(self._mod.script_dict, self._result)
        self.fill_port("best_sim_table",
                       MAKE_DATA(self._para_tab.string_value))
        self.fill_port("samples", MAKE_DATA(self._mod.sample))
        self.fill_port("best_result", MAKE_DATA(self._selected_error_set))
        self.fill_port("best_history", MAKE_DATA(self._best_history))
        for inst in self._mod.instruments:
            self.fill_port("instruments", MAKE_DATA(inst))
        for index, simulator in enumerate(self._sims):
            type_name = simulator.abstract_type.split("_")[-1]
            inf = self["FOM"].born[index][0]
            sup = self["FOM"].born[index][1]
            self._para_tab.x = self._result
            y_sim = self._mod.simulate()[inf:sup]
            current_exp_data = exp_data[index]
            end_data = MAKE_DATA({"theta_array": current_exp_data.x,
                                  type_name + "_sim": y_sim,
                                  type_name + "_data": current_exp_data.y,
                                  "composite": True},
                                 abstract="opti_"+type_name)
            self.fill_port("end_data", MAKE_DATA(end_data))
