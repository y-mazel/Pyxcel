# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Created on 24 oct. 2014

@author: GP243515
"""
import paf.data
try:
    import pyxcel.engine.modeling.entity as entity
    ignor = True
except:
    ignor = False
import unittest
import numpy as np
import directory
import os
temp_dir = os.path.join(directory.get_base_dir(), "temp")
temp_file = os.path.join(temp_dir, "f.xml")


class SaveTest(unittest.TestCase):
    """ test save and load file.
    """

    def test_main(self):
        """ test save and load instrument
        """
        if not ignor:
            pass
        else:
            data_io = paf.data.DataIo()
            dx = entity.XRaySourceData()
            dy = entity.XRRDetectorData()
            d1 = entity.InstrumentData(dx, dy)
            data_io.data_to_file(temp_file, d1)
            d2 = data_io.file_to_data(temp_file)
            self.assertEqual(type(d2['main']), entity.InstrumentData)
            self.assertEqual(type(d2['main']['source']), entity.XRaySourceData)
            self.assertEqual(type(d2['main']['detector']),
                             entity.XRRDetectorData)

    def test_all_simple(self):
        """ test for all basic instrument
        """
        data_io = paf.data.DataIo()
        d1 = paf.data.SimpleData(5j)
        d2 = paf.data.SimpleData(False)
        d2t = paf.data.SimpleData(True)
        d3 = paf.data.SimpleData(np.array([5, 6, 7]))
        d4 = paf.data.SimpleData(type)
        d5 = paf.data.SimpleData(unittest.TestCase)
        data_io.data_to_file(temp_file, d1)
        d1_b = data_io.file_to_data(temp_file)
        self.assertEqual(d1.value, d1_b['main'].value)
        data_io.data_to_file(temp_file, d2)
        d2_b = data_io.file_to_data(temp_file)
        self.assertEqual(d2.value, d2_b['main'].value)
        data_io.data_to_file(temp_file, d2t)
        d2t_b = data_io.file_to_data(temp_file)
        self.assertEqual(d2t.value, d2t_b['main'].value)
        data_io.data_to_file(temp_file, d3)
        d3_b = data_io.file_to_data(temp_file)
        for i in range(3):
            self.assertEqual(d3.value[i], d3_b['main'].value[i])
        self.assertEqual(str(d3), str(d3_b['main']))
        data_io.data_to_file(temp_file, d4)
        d4_b = data_io.file_to_data(temp_file)
        self.assertEqual(d4.value, d4_b['main'].value)
        data_io.data_to_file(temp_file, d5)
        d5_b = data_io.file_to_data(temp_file)
        self.assertEqual(d5.value, d5_b['main'].value)

    def test_list(self):
        """ test for saving and loading list data.
        """
        data_io = paf.data.DataIo()
        d1 = paf.data.ListData([5, 6, 7])
        data_io.data_to_file(temp_file, d1)
        d2 = data_io.file_to_data(temp_file)
        self.assertEqual(d2['main'].value, d1.value)
