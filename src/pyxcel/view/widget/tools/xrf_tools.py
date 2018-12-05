# -*- coding: utf8 -*-
"""
GUI for xrf tools.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import os
import xraylib
import numpy as np
from matplotlib.figure import Figure
import pyxcel.engine.centralizer
from pyxcel.view.widget.operation.line_editor import LineEditor
from pyxcel.engine.simulator.xrf_no_genx import Line
from pyxcel.view.cute import QWidget, FigureCanvas, uic
from pyxcel.view.cute import NavigationToolbar


def calc_XRF_CS(one_element, transition, inc_en_eV):
    """ one_element is the chemical species symbol (e.g. Cl or Ni) transition
    is an integer corresponding to the transition as defined in xraylib
    inc_en_eV is the incident energy expressed in eV
    """
    atomic_number = xraylib.SymbolToAtomicNumber(one_element)
    XRF_CS = xraylib.CS_FluorLine_Kissel_Cascade(atomic_number, transition,
                                                 inc_en_eV/1000.)
    return XRF_CS


class XrfTools(QWidget):
    """ widget to display XRF properties
    """
    def __init__(self, parent=None):
        """ initialization
        """
        QWidget.__init__(self, parent)
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        former = os.path.join(self._centralizer.option.ui_dir,
                              "xrf_tool_box.ui")
        uic.loadUi(former, self)
        self.calculate_button.clicked.connect(self.calculate)
        self._fig = Figure((5.0, 4.0), dpi=100)
        self._canvas = FigureCanvas(self._fig)
        self.graph_layout.addWidget(self._canvas)
        self._toolbar = NavigationToolbar(self._canvas, self)
        self.graph_layout.addWidget(self._toolbar)
        self._axes = self._fig.add_subplot(111)
        self._line = Line()
        self._line_editor = LineEditor(self, self._line)
        self.element_layout.addWidget(self._line_editor)
        self._data = None
        self.copy_button.clicked.connect(self.copie_data)

    def copie_data(self):
        """ slot for copiing data
        """
        if self._data is not None:
            clipboard = self._centralizer.clipboard
            txt_data = "energy (keV)\t" + self._line["material"].value + "\n"
            for energy, value in self._data:
                txt_data += str(energy) + "\t" + str(value) + "\n"
            clipboard.setText(txt_data)

    def calculate(self):
        """ slot for calculate button clicked
        """
        self._axes.clear()
        start_E = float(self.start_line.text())
        end_E = float(self.end_line.text())
        no_steps = int((end_E-start_E) /
                       float(self.inc_line.text()))+1
        E_array = np.linspace(start_E, end_E, no_steps)
        one_element = self._line["material"].value
        transition = eval(self._line["line"].value)
        # with list comprehention
        CS_array = np.array([calc_XRF_CS(one_element, transition,
                                         one_energy*1000.)
                             for one_energy in E_array])
        # with np.zero
#         CS_array = np.zeros(E_array.size)
#         for idx, one_energy in enumerate(E_array):
#             CS_array[idx] = calc_XRF_CS(one_element, transition,
#                                         one_energy*1000.)
        self._data = zip(list(E_array), list(CS_array))
        self._axes.plot(E_array, CS_array, label=one_element +
                        ' XRF CS')
        self._axes.set_ylabel('XRF Cross-section (barn/atom)')
        self._axes.set_xlabel('Energy (keV)')
        self._axes.relim()
        self._axes.autoscale_view(True, True, True)
        self._axes.legend()
        self._fig.canvas.draw()
