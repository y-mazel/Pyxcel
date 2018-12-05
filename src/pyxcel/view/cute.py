# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Package for importing Qt4 or 5.

    :platform: Unix, Windows
    :synopsis: fast simulation windows.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
try:
    from PyQt4.QtGui import QMainWindow, QMdiArea, QAction, QTabWidget
    from PyQt4.QtGui import QTreeWidget, QInputDialog, QTreeWidgetItem
    from PyQt4.QtGui import QApplication, QFileDialog, QMessageBox, QComboBox
    from PyQt4.QtGui import QLabel, QPushButton, QMenu, QWidget, QHBoxLayout
    from PyQt4.QtGui import QSpacerItem, QSizePolicy, QCheckBox, QGroupBox
    from PyQt4.QtGui import QSizePolicy, QErrorMessage, QVBoxLayout, QLineEdit
    from PyQt4.QtGui import QListWidget, QFormLayout, QDialog, QTableWidget
    from PyQt4.QtGui import QTableWidgetItem, QTextEdit, QSpinBox, QTableView
    from PyQt4.QtCore import Qt, pyqtSlot, QSize, QObject, pyqtSignal
    from PyQt4.QtCore import QDateTime
    from PyQt4.QtCore import QTranslator, QLocale, QModelIndex, QVariant
    from PyQt4.Qt import QAbstractTableModel
    from PyQt4 import uic
#     from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt4agg import FigureCanvas
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as \
        NavigationToolbar
    QT_VERSION = 4
    print("qt_version 4")
except ImportError as er:
    print(er)
#     from PyQt5.QtWidgets import QMainWindow, QMdiArea, QAction, QTabWidget
#     from PyQt5.QtWidgets import QTreeWidget, QInputDialog, QTreeWidgetItem
#     from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
#     from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QMenu, QWidget
#     from PyQt5.QtWidgets import QHBoxLayout, QSpacerItem, QSizePolicy
#     from PyQt5.QtWidgets import QCheckBox, QGroupBox, QSizePolicy, QTableView
#     from PyQt5.QtWidgets import QErrorMessage, QVBoxLayout, QLineEdit
#     from PyQt5.QtWidgets import QListWidget, QFormLayout, QDialog, QTableWidget
#     from PyQt5.QtWidgets import QTableWidgetItem, QTextEdit, QSpinBox
#     from PyQt5.QtCore import Qt, pyqtSlot, QSize, QObject, pyqtSignal
#     from PyQt5.QtCore import QTranslator, QLocale, QModelIndex, QVariant
#     from PyQt5.QtCore import QDateTime
#     from PyQt5.Qt import QAbstractTableModel
#     from PyQt5 import uic
#     import matplotlib
#     matplotlib.use("Qt5Agg")
#     from matplotlib.backends.backend_qt5agg import FigureCanvas
#     from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as \
#         NavigationToolbar
#     QT_VERSION = 5
#     print("qt_version 5")

div = [QMainWindow, QMdiArea, QAction, QTabWidget, QTreeWidget, QInputDialog,
       QTreeWidgetItem, QApplication, QFileDialog, QMessageBox, QComboBox,
       QLabel, QPushButton, QMenu, QWidget, QHBoxLayout, QSpacerItem,
       QSizePolicy, QCheckBox, QGroupBox, QSizePolicy, QErrorMessage,
       QVBoxLayout, QLineEdit, QListWidget, QFormLayout, Qt, QDialog,
       QTableWidget, QTableWidgetItem, QTextEdit, pyqtSlot, FigureCanvas,
       uic, QSize, QObject, pyqtSignal, NavigationToolbar, QSpinBox,
       QTranslator, QLocale, QAbstractTableModel, QTableView, QModelIndex,
       QVariant, QDateTime]
