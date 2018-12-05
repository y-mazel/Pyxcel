# -*- coding: utf8 -*-
"""
GUI to create a new instrument.

    :platform: Unix, Windows
    :synopsis: Controller module for modeling.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
from pyxcel.uni import uni
import pyxcel.engine.modeling.entity as entity
import pyxcel.engine.centralizer
import os
import logging
from pyxcel.view.cute import QWidget, uic


class CreateInstrument(QWidget):
    """ windows for instrument creator
    """
    source_dict = {"XRR": entity.XRaySourceData, "XRF": entity.XRaySourceData}

    detector_dict = {"XRR": entity.XRRDetectorData,
                     "XRF": entity.XRFDetectorData}

    def __init__(self, parent):
        """ initialization
        """
        QWidget.__init__(self, None)
        self._parent = parent
        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        former = os.path.join(self._centralizer.option.ui_dir,
                              "create_instrument.ui")
        uic.loadUi(former, self)
        self.validate_button.clicked.connect(self.validate)
        self.cancel_button.clicked.connect(self.cancel)
        self.name_edit.setFocus()
        self.name_edit.returnPressed.connect(self.validate)
        self.adjustSize()
        self.show()

    def validate(self):
        """ validate creation
        """
        type_name = uni(self.type_combo.currentText())
        source = self.source_dict[type_name]
        detector = self.detector_dict[type_name]
        name = self.name_edit.text()
        self._centralizer.controller.create_instrument(name, source, detector,
                                                       type_name)
        logging.info("Creating a new instrument %s of type: %s", name, type_name)
        self.close()

    def cancel(self):
        """ canceling creation
        """
        self.close()
