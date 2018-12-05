# -*- coding: utf8 -*-
"""
Launch main windows with default option.

    :platform: Unix, Windows
    :synopsis: main program.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import sys
import os
import logging
import directory
import pyxcel.view.main_window
import pyxcel.engine.centralizer
from pyxcel.view.cute import QApplication
from PyQt4 import QtGui
sys.path.append(os.path.join(directory.get_base_dir(), "genx"))
sys.path.append(os.path.join(directory.get_base_dir(), "lib"))

import ctypes
if sys.platform == "win32":
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == '__main__':
    # main execution
    logging.basicConfig(format='%(levelname)-8s %(asctime)s: %(message)s',
                        filename='pyxcel.log', level=logging.INFO)
    logging.info("Starting pyxcel")
    APP = QApplication(sys.argv)
    # set app icon    
    app_icon = QtGui.QIcon('ui/pyxcel.ico')

    APP.setWindowIcon(app_icon)
    CENTRALIZER = pyxcel.engine.centralizer.Centralizer()
    CENTRALIZER.option.ui_dir = os.path.join(directory.get_base_dir(), "ui")
    CENTRALIZER.option.doc_dir = os.path.join(directory.get_base_dir(), "doc")
    APP.installTranslator(CENTRALIZER.option.translator)
    CENTRALIZER.clipboard = APP.clipboard()
    CENTRALIZER.main_window = pyxcel.view.main_window.MainWindows()
    CENTRALIZER.main_window.showMaximized()
    sys.exit(APP.exec_())
    logging.info("Stopping pyxcel")
