# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
GUI to edit composite data.

    :platform: Unix, Windows
    :synopsis: GUI to Pipeline.

.. moduleauthor:: Gaël PICOT <gael.picot@free.fr>
"""
import paf.data
import pyxcel.engine.centralizer
from pyxcel.uni import uni
from pyxcel.engine.database import CompositeDataObservable, ListDataObservable
from pyxcel.view.cute import QWidget, QHBoxLayout, QLabel, QSpacerItem
from pyxcel.view.cute import QSizePolicy, QLineEdit, QPushButton, QFileDialog
from pyxcel.view.cute import QApplication, QComboBox, QFormLayout
from matplotlib.cbook import tostr
from quantities import Quantity
try:
    import pyxcel.view.widget.composite_editor_4 as former
except ImportError:
    import pyxcel.view.widget.composite_editor_5 as former
MAKE_DATA = paf.data.make_data


try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


def clear_layout(layout):
    """ clear a layout
    """
    for i in reversed(range(layout.count())):
        if layout.itemAt(i).widget() is not None:
            widget_to_del = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_del)
            widget_to_del.deleteLater()
        else:
            layout.removeItem(layout.itemAt(i))


class FieldEditor(QWidget):
    """ line for edit a single value.
    """
    def __init__(self, parent, field_data, name, key, auto=False):
        """ initialization
        """
        QWidget.__init__(self, parent)
        #: parent widget
        self._parent = parent
        self._name = name
        self._key = key
        self._field_data = field_data
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._tempory_value = field_data.value
        self._old_value = field_data.value
        self._abstract = field_data.abstract_type
        self._auto = auto
        self._line_edit = None
        self._combo = None
        self._line_label = None
        self._lock = False

        # choose field constructor
        if field_data.abstract_type == 'filename':
            self.construct_file_field()
        elif field_data.abstract_type == 'fom_sel':
            self.construct_fom_selector()
        elif isinstance(self._old_value, bool):
            self.construct_bool_field()
        elif isinstance(field_data, paf.data.SimpleData):
            self.construct_simple_field()
        elif isinstance(field_data, paf.data.QuantitiesData):
            self._unit = field_data.unit
            self.construct_quantities_field()
        else:
            self._tempory_value = field_data
            self.construct_more_field()

    def construct_fom_selector(self):
        """ construct a new fom selector
        """
        self._combo = QComboBox()
        fom_dict = pyxcel.engine.centralizer.Centralizer().option.fom_dict
        for index, key in enumerate(sorted(list(fom_dict.keys()))):
            self._combo.addItem(key)
            if key == self._old_value:
                self._combo.setCurrentIndex(index)
        self._combo.currentIndexChanged.connect(self.
                                                edit_simple_tempory_value())
        self._layout.addWidget(self._combo)

    def _refresh(self):
        """ refresh value
        """
        value = self._parent.data_composite[self._key].value
        self._field_data = self._parent.data_composite[self._key]
        self._tempory_value = value
        self._old_value = value
        if self._line_edit is not None:
            self._line_edit.setText(uni(value))
        elif self._line_label is not None:
            text = str(self._parent.data_composite[self._key])
            max_len = pyxcel.engine.centralizer.Centralizer().option.max_len
            if len(text) > max_len:
                text = text[:max_len]
                text += "..."
            self._line_label.setText(uni(text))
        elif isinstance(value, bool):
            if value:
                self._combo_bool.setCurrentIndex(0)
            else:
                self._combo_bool.setCurrentIndex(1)

    def refresh(self):
        """ refresh value *if is not lock*
        """
        if not self._lock:
            self._refresh()

    def construct_bool_field(self):
        """ construct field for boolean
        """
        bool_combo = QComboBox()
        self._combo_bool = bool_combo
        bool_combo.addItem("True")
        bool_combo.addItem("False")
        if self._old_value is False:
            bool_combo.setCurrentIndex(1)
        bool_combo.currentIndexChanged.connect(self.edit_simple_tempory_value()
                                               )
        self._layout.addWidget(bool_combo)

    def more(self):
        """ edit composite element.
        """
        self._parent.new_data(self._tempory_value)

    def choose(self):
        """ slot for choose a file.
        """
        resultat = QFileDialog.getOpenFileName(None, 'Open', "", '*.*')
        if resultat[1]:
            self._line_edit.setText(uni(resultat))

    def construct_quantities_field(self):
        """ create a field for quantities data showing unit.
        """
        self._line_edit = QLineEdit()
        self._line_edit.setObjectName(uni(self._key) + "_edit")
        self._line_edit.setText(uni(self._tempory_value))
        self._line_edit.textChanged.connect(self.edit_simple_tempory_value())
        self._layout.addWidget(self._line_edit)
        label = QLabel()
        label.setObjectName(uni(self._key) + '_unit_label')
        try:
            label.setText(self._unit.symbol)
        # if the database is saved and reopened
        except AttributeError:
            #print(unicode(self._unit.symbol))
            label.setText(str(self._unit)[2:])
        
        self._layout.addWidget(label)

    def validate(self):
        """ validate change of the value
        """
        self.edit_simple_tempory_value()
        if self._tempory_value != self._old_value or self._auto:
            self._parent.change_value(self._key, self._tempory_value)

    def edit_simple_tempory_value(self):
        """ create slot to change temporary value
        """
        if self._field_data.data_type is int:
            def set_parameter_slot(int_value):
                """ slot to change temporary int value
                """
                self._tempory_value = int(int_value)
        elif self._field_data.abstract_type == 'fom_sel':
            def set_parameter_slot(int_value):
                """ slot to change temporary fom value
                """
                self._tempory_value = uni(self._combo.currentText())
        elif self._field_data.data_type is float:
            def set_parameter_slot(float_value):
                """ slot to change temporary float value
                """
                self._tempory_value = float(float_value)
        elif self._field_data.data_type is bool:
            def set_parameter_slot(index):
                """ slot to change temporary bool value
                """
                if index == 0:
                    self._tempory_value = True
                else:
                    self._tempory_value = False
        elif self._field_data.data_type is complex:
            def set_parameter_slot(complex_value):
                """ slot to change temporary complex value
                """
                self._tempory_value = complex(complex_value)
        else:
            def set_parameter_slot(string_value):
                """ slot to change temporary string value
                """
                self._tempory_value = str(string_value)

        def add_try(slot):
            """ creator to add try
            """
            def new_slot(arg):
                """ new slot
                """
                try:
                    slot(arg)
                    if self._auto:
                        par = self._parent
                        par.data_composite.disconnect_to_signal(par.refresh)
                        self.validate()
                        self._lock = True
                        par.refresh()
                        self._lock = False
                        par.data_composite.connect_to_signal(par.refresh)
                except:
                    pass
            return new_slot
        set_parameter_slot = add_try(set_parameter_slot)
        return set_parameter_slot

    def construct_file_field(self):
        """ construct a field to choose a file
        """
        label = QLabel()
        label.setObjectName(uni(self._key) + '_label')
        label.setText(self._name)
        self._layout.addWidget(label)
        self._line_edit = QLineEdit()
        self._line_edit.setObjectName(uni(self._key) + "_edit")
        self._line_edit.setText(uni(self._tempory_value))
        self._line_edit.textChanged.connect(self.edit_simple_tempory_value())
        self._layout.addWidget(self._line_edit)
        choose_button = QPushButton(self)
        choose_button.setObjectName(uni(self._key) + "_button")
        choose_button.clicked.connect(self.choose)
        choose_button.setText("choisir")
        self._layout.addWidget(choose_button)

    def construct_simple_field(self):
        """ construct simple field
        """
        self._line_edit = QLineEdit()
        self._line_edit.setObjectName(uni(self._key) + "_edit")
        self._line_edit.setText(uni(self._tempory_value))
        self._line_edit.textChanged.connect(self.edit_simple_tempory_value())
        self._layout.addWidget(self._line_edit)

    def construct_more_field(self):
        """ construct field for composite element
        """
        self._line_label = QLabel(self)
        self._line_label.setObjectName(uni(self._key) + "_edit")
        text = str(self._field_data)
        max_len = pyxcel.engine.centralizer.Centralizer().option.max_len
        if len(text) > max_len:
            text = text[:max_len]
            text += "..."
        self._line_label.setText(uni(text))
        self._layout.addWidget(self._line_label)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum)
        self._layout.addItem(spacerItem)
        more_button = QPushButton(self)
        more_button.setObjectName(uni(self._key) + "_button")
        more_button.clicked.connect(self.more)
        more_button.setText("Edit")
        self._layout.addWidget(more_button)


class CompositeEditor(QWidget):
    """ widget to edit composite data
    """
    def __init__(self, parent, data_composite, auto=None):
        """ initialization
        """
        QWidget.__init__(self, parent)

        class DataWarper(paf.data.CompositeData):
            """ to wrap simple data
            """
            def __init__(self, data):
                paf.data.CompositeData.__init__(self, {"value": data.value})
                self._data = data

            def __setitem__(self, key, value):
                paf.data.CompositeData.__setitem__(self, key, value)
                self._data.value = value

        self._centralizer = pyxcel.engine.centralizer.Centralizer()
        if isinstance(data_composite, paf.data.SimpleData):
            data_composite = DataWarper(data_composite)
        if auto is None:
            auto = self._centralizer.option.composite_auto
        self._auto = auto
        data_composite = CompositeDataObservable(data_composite)
        self._field = {}
        self._former = former.Ui_Form()
        self._former.setupUi(self)
        if auto:
            validation_widget = self.findChild(QWidget, "validation_widget")
            validation_widget.hide()
        self._parent = parent
        self._layout = self.findChild(QWidget, "workspace").layout()
        self._data_composite = data_composite
        self.load_composite(data_composite)
        self._data_composite.connect_to_signal(self.refresh)
        self.connect_signals()

    @property
    def data_composite(self):
        """ accesss to data composite
        """
        return self._data_composite

    def connect_signals(self):
        """ connect GUI signal
        """
        # button
        cancel_button = self.findChild(QPushButton, "cancel_button")
        cancel_button.clicked.connect(self.cancel)
        validate_button = self.findChild(QPushButton, "validate_button")
        validate_button.clicked.connect(self.validate)

    def validate(self):
        """ validate
        """
        self._data_composite.disconnect_to_signal(self.refresh)
        for key, _ in self._data_composite.showing_info:
            self._field[key].validate()
        self._data_composite.connect_to_signal(self.refresh)
        self.refresh()
        try:
            self._parent.go_back()
        except:
            pass

    def cancel(self):
        """ cancel modification.
        """
        try:
            self._parent.go_back()
        except:
            pass

    def change_value(self, name, value):
        """ change value of an element.
        """
        if isinstance(value, CompositeDataObservable):
            value = value.composite_data
        elif isinstance(value, ListDataObservable):
            value = value.list_data
        self._data_composite[name] = value

    def refresh(self):
        """ refresh window.
        """
        if self.parent() is not None:
            for _, field in self._field.items():
                field.refresh()

    def clear(self):
        """ clear all composite field
        """
        clear_layout(self._layout)

    def load_composite(self, data_composite=None):
        """ load a CompositeData object
        """
        self.clear()
        type_name = (data_composite.__class__.__module__ + '.' +
                     data_composite.__class__.__name__)
        if data_composite is not None:
            self._data_composite = data_composite
            index = 0
            for (key, name) in self._data_composite.showing_info:
                # add label
                label = QLabel(self)
                label.setObjectName(uni(key) + '_label')
                label.setText(uni(name))
                self._layout.setWidget(index, QFormLayout.LabelRole, label)
                value = data_composite[key]
                name = uni(_translate(type_name, name, None))
                self._field[key] = FieldEditor(self, value, name, key,
                                               self._auto)
                self._layout.setWidget(index, QFormLayout.FieldRole,
                                       self._field[key])
                index += 1
        spacer = QSpacerItem(100, 100, QSizePolicy.Expanding,
                             QSizePolicy.Expanding)
        self._layout.addItem(spacer)

    def new_data(self, data):
        """ load a new data.
        """
        self._parent.data = data
