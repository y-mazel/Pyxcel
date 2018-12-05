# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit line parameter.

    :platform: Unix, Windows
    :synopsis: edit parameter to fit.

.. moduleauthor:: Gael PICOT <gael.picot@free.fr>
"""
import xraylib
import periodictable
import logging
import sys
from pyxcel.uni import uni
from pyxcel.view.cute import QWidget, QPushButton, QComboBox
try:
    import pyxcel.view.widget.operation.line_editor_4 as former
except ImportError:
    import pyxcel.view.widget.operation.line_editor_5 as former


lines = ((xraylib.KA1_LINE, "KA1_LINE", "xraylib.KA1_LINE"),
         (xraylib.KA2_LINE, "KA2_LINE", "xraylib.KA2_LINE"),
         (xraylib.KA3_LINE, "KA3_LINE", "xraylib.KA3_LINE"),
         (xraylib.KB1_LINE, "KB1_LINE", "xraylib.KB1_LINE"),
         (xraylib.KB2_LINE, "KB2_LINE", "xraylib.KB2_LINE"),
         (xraylib.KB3_LINE, "KB3_LINE", "xraylib.KB3_LINE"),
         (xraylib.KB4_LINE, "KB4_LINE", "xraylib.KB4_LINE"),
         (xraylib.KB5_LINE, "KB5_LINE", "xraylib.KB5_LINE"),
         (xraylib.LA1_LINE, "LA1_LINE", "xraylib.LA1_LINE"),
         (xraylib.LA2_LINE, "LA2_LINE", "xraylib.LA2_LINE"),
         (xraylib.LB1_LINE, "LB1_LINE", "xraylib.LB1_LINE"),
         (xraylib.LB2_LINE, "LB2_LINE", "xraylib.LB2_LINE"),
         (xraylib.LB3_LINE, "LB3_LINE", "xraylib.LB3_LINE"),
         (xraylib.LB4_LINE, "LB4_LINE", "xraylib.LB4_LINE"),
         (xraylib.LB5_LINE, "LB5_LINE", "xraylib.LB5_LINE"),
         (xraylib.LB6_LINE, "LB6_LINE", "xraylib.LB6_LINE"),
         (xraylib.LB7_LINE, "LB7_LINE", "xraylib.LB7_LINE"),
         (xraylib.LB9_LINE, "LB9_LINE", "xraylib.LB9_LINE"),
         (xraylib.LB10_LINE, "LB10_LINE", "xraylib.LB10_LINE"),
         (xraylib.LB15_LINE, "LB15_LINE", "xraylib.LB15_LINE"),
         (xraylib.LB17_LINE, "LB17_LINE", "xraylib.LB17_LINE"),
         (xraylib.LG1_LINE, "LG1_LINE", "xraylib.LG1_LINE"),
         (xraylib.LG2_LINE, "LG2_LINE", "xraylib.LG2_LINE"),
         (xraylib.LG3_LINE, "LG3_LINE", "xraylib.LG3_LINE"),
         (xraylib.LG4_LINE, "LG4_LINE", "xraylib.LG4_LINE"),
         (xraylib.LG5_LINE, "LG5_LINE", "xraylib.LG5_LINE"),
         (xraylib.LG6_LINE, "LG6_LINE", "xraylib.LG6_LINE"),
         (xraylib.LG8_LINE, "LG8_LINE", "xraylib.LG8_LINE"),
         (xraylib.LE_LINE, "LE_LINE", "xraylib.LE_LINE"),
         (xraylib.LH_LINE, "LH_LINE", "xraylib.LH_LINE"),
         (xraylib.LL_LINE, "LL_LINE", "xraylib.LL_LINE"),
         (xraylib.LS_LINE, "LS_LINE", "xraylib.LS_LINE"),
         (xraylib.LT_LINE, "LT_LINE", "xraylib.LT_LINE"),
         (xraylib.LU_LINE, "LU_LINE", "xraylib.LU_LINE"),
         (xraylib.LV_LINE, "LV_LINE", "xraylib.LV_LINE"),
         (xraylib.MA1_LINE, "MA1_LINE", "xraylib.MA1_LINE"),
         (xraylib.MA2_LINE, "MA2_LINE", "xraylib.MA2_LINE"),
         (xraylib.MB_LINE, "MB_LINE", "xraylib.MB_LINE"),
         (xraylib.MG_LINE, "MG_LINE", "xraylib.MG_LINE"))


class LineEditor(QWidget):
    """ widget for line editor.
    """
    def __init__(self, parent, data):
        """ initialization
        """
        QWidget.__init__(self)
        self._parent = parent
        self._data = data
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        self._element_combo = self.findChild(QComboBox, "element_combo")
        self._line_combo = self.findChild(QComboBox, "line_combo")
        validate_button = self.findChild(QPushButton, "validate_button")
        validate_button.clicked.connect(self.validate)
        cancel_button = self.findChild(QPushButton, "cancel_button")
        cancel_button.clicked.connect(self.cancel)
        self.fill_element()
        material = self._data["material"].value
        atomic_number = 0
        for element in periodictable.elements:
            if element.symbol == material:
                atomic_number = element.number
        index = self._element_combo.findData(atomic_number)
        self._element_combo.setCurrentIndex(index)
        self.change_sel_el()
        line = self._data["line"].value
        index = self._line_combo.findData(line)
        self._line_combo.setCurrentIndex(index)
        self._element_combo.currentIndexChanged.connect(self.change_sel_el)
        self._element_number = 1

        try:
            parent.go_back
        except:
            self._validate_widget = self.findChild(QWidget, "validate_widget")
            self._validate_widget.hide()
            self._line_combo.currentIndexChanged.connect(self.validate)

    @property
    def data(self):
        """ accessing to data
        """
        return self._data

    @property
    def element_number(self):
        """ selected element number
        """
        return self._element_number

    def fill_element(self):
        """ fill element in element combobox
        """
        for element in periodictable.elements:
            if element.number == 0:
                continue
            self._element_combo.addItem(element.symbol + ", " + element.name +
                                        " (" + str(element.number) + ")",
                                        element.number)

    def change_sel_el(self):
        """ change selected element slot
        """
        if sys.version_info[0] < 3:
            el = int(self._element_combo.itemData(self._element_combo.
                                                  currentIndex()).toInt()[0])
        else:
            el = int(self._element_combo.itemData(self._element_combo.
                                                  currentIndex()))
        self._line_combo.clear()
        for line in lines:
            if xraylib.LineEnergy(el, line[0]) != 0.:
                self._line_combo.addItem(line[1], line[2])

    def validate(self):
        """ validate entry
        """
        if sys.version_info[0] < 3:
            line = uni(self._line_combo.itemData(self._line_combo.
                                                 currentIndex()).toString())
        else:
            line = uni(self._line_combo.itemData(self._line_combo.
                                                 currentIndex()))
        self._data["line"] = line
        if sys.version_info[0] < 3:
            el = int(self._element_combo.itemData(self._element_combo.
                                                  currentIndex()).toInt()[0])
        else:
            el = int(self._element_combo.itemData(self._element_combo.
                                                  currentIndex()))
        mat = periodictable.core.element_base[el][1]
        self._data["material"] = mat
        try:
            self._parent.go_back()
        except:
            pass
        logging.info("validate line %s for element %s", line, mat)

    def cancel(self):
        """ cancel entry
        """
        self._parent.go_back()
