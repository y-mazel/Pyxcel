# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Created on 7 nov. 2014

@author: GP243515
"""
import unittest
import paf.data as data
import quantities as pq
import numpy as np
MAKE_DATA = data.make_data
try:
    from new import classobj
    py3 = False
except ImportError:
    py3 = True


class DataTest(unittest.TestCase):
    """ test for paf.data module
    """

    def test_data_array(self):
        """ test data array
        """
        dc = MAKE_DATA([{"name": 'test', 'value': 4, 'composite': True},
                        {"name": 'test', 'value': 85}])
        self.assertIs(type(dc), data.ListData)
        t = [{"name": 'test', 'value': 4},
             {"name": 'test', 'value': 85}]
        self.assertEqual(dc.value, t)

    def test_data_from_class(self):
        """ test to create a data object from class
        """
        class test:
            def __str__(self):
                return "yes!"
        d = MAKE_DATA(test)
        d2 = MAKE_DATA(test())
        self.assertEqual(d2.is_compatible(d), False)

    def test_quantities_nparray(self):
        """ test using numpy array and quantities data
        """
        a = np.array([10, 20, 30])
        dc = MAKE_DATA(a, unit=pq.m)
        dc.unit = pq.m
        self.assertEqual(list(dc.value), list(a))

    def test_data_from_data(self):
        """ test to create new data from an another
        """
        data1 = MAKE_DATA(6, unit=pq.m)
        data2 = MAKE_DATA(data1)
        data3 = MAKE_DATA(3, unit=pq.cm)
        data4 = MAKE_DATA(data1, copy=True)
        self.assertIs(data1, data2)
        self.assertIsNot(data1, data4)
        data2.unit = pq.cm
        self.assertEqual(600, data2.value)
        self.assertEqual(float, type(data2.value))
        self.assertEqual(data1.is_compatible(data3), True)

    def test_data_from_data_quantities(self):
        """ create data from a quantities data
        """
        data1 = MAKE_DATA({"value": [6., 500.], "unit": pq.cm})
        data2 = MAKE_DATA(data1)
        self.assertEqual(str(data1[1]), '500.0 cm')
        self.assertEqual([6., 500.], data2.value)
        for d in data1:
            d.unit = pq.m
        self.assertEqual([.06, 5], data1.value)
        data1[0].value = 7
        self.assertEqual([7, 5], data1.value)
        data1[0].value = 8 * pq.m
        self.assertEqual([8, 5], data1.value)

    def test_data_from_data_list(self):
        """ create data from a data list.
        """
        data1 = MAKE_DATA([6,  5], unit=pq.m)
        data2 = MAKE_DATA(5)
        data3 = MAKE_DATA([5, 6])
        data4 = MAKE_DATA([5], unit=pq.m)
        data5 = MAKE_DATA([5, 5], unit=pq.m)
        for d in data1:
            d.unit = pq.cm
        self.assertEqual([600, 500], data1.value)
        self.assertEqual(data1.is_compatible(data2), False)
        self.assertEqual(data1.is_compatible(data3), False)
        self.assertEqual(data1.is_compatible(data4), True)
        self.assertEqual(data1.is_compatible(data5), True)

    def test_basique(self):
        """ some basic test
        """
        dc = MAKE_DATA({"name": 'test', 'value': 4, 'abstract': ''},
                       composite=True)
        dc_s = MAKE_DATA({"name": 'test', 'value': 4, 'v2': dc,
                          'abstract': ''}, composite=True)
        if py3:
            self.assertEquals(str(dc_s), "name = test, v2 = (name = test, \
value = 4), value = 4")
        else:
            self.assertEquals(str(dc_s), "name = test, v2 = (name = test, \
value = 4), value = 4")
        self.assertEquals(dc[MAKE_DATA("name")], dc['name'])
        dc_s.set_showing_info("name", "other name", 1)
        self.assertEquals(dc_s.showing_info[1], ('other name', 'name'))
        dc2 = MAKE_DATA(40000, unit=pq.J)
        dc3 = MAKE_DATA({"name": 33, 'value': 4}, composite=True)
        dc4 = MAKE_DATA({"name": 'test2', 'value': 4}, composite=True)
        dcs = MAKE_DATA({"name": 'test2', 'value': 4,
                         's': {'a': 34, 'b': 2}}, composite=True)
        self.assertEquals(dcs["name"].value, 'test2')
        dcs["name"] = "tt"
        self.assertEquals(dcs["name"].value, 'tt')
        dcs["name"] = MAKE_DATA("test2")
        with self.assertRaises(KeyError):
            dcs["valoe"] = 6
        with self.assertRaises(KeyError):
            self.assertEquals(dcs["valoe"].value, 4)
        self.assertEquals(dcs.is_compatible(dc), False)
        dc5 = MAKE_DATA([40000, 80000], unit=pq.J)
        self.assertEquals(dc.is_compatible(dc2), False)
        self.assertEquals(dc.is_compatible(dc3), False)
        self.assertEquals(dc.is_compatible(dc4), True)
        self.assertEquals(dc.is_compatible(5), False)
        self.assertEquals(dc.value, {'name': 'test', 'value': 4})
        self.assertEquals(dc2.is_compatible(dc5), False)
        with self.assertRaises(AttributeError):
            dc3.unit
        data.Data.add_abstract_compatibility("name_type1", "name_type2")
        dca = MAKE_DATA({"name": 'test', 'value': 4}, abstract="name_type1")
        dca2 = MAKE_DATA({"name": 'test', 'value': 4}, abstract="name_type2")
        dca3 = MAKE_DATA({"name": 'test', 'value': 4}, abstract="name_type3")
        dca4 = MAKE_DATA({"name": 'test', 'value': 4}, abstract="name_type4")
        dca.value = 5
        self.assertNotEqual(dca.value, dca2.value)
        self.assertEquals(dca3.is_compatible(dca4), True)
        self.assertEquals(dca.is_compatible(dca2), True)
        self.assertEquals(dca2.is_compatible(dca), False)
        data.Data.add_abstract_compatibility("name_type2", "ghfh")
        self.assertEquals(dca2.is_compatible(dca), False)
        dcs["name"] = "value"

    def test_iterator_in_lits_data(self):
        """ test for iterator in ListData object
        """
        l = [14, 15, 25, 21, 65, 8, 0, 33]
        l1 = data.ListData(l)
        for (num, el) in enumerate(l1):
            self.assertEquals(l[num], el.value)
            if num % 3 == 1:
                break
        for (num, el) in enumerate(l1):
            self.assertEquals(l[num], el.value)
        for (num, el) in enumerate(l1):
            self.assertEquals(l1[num].value, l[num])

    def test_unit(self):
        """ test quantities data and change unit
        """
        datacm = MAKE_DATA(41000, unit=pq.cm)
        datam = MAKE_DATA(4, unit=pq.m)
        datacm.convert_unit(datam)
        self.assertEquals(datacm.value, 410)
        dcm = MAKE_DATA({"name": 'test', 'value':
                         {"value": 4, 'unit': pq.m}}, composite=True)
        dcm2 = MAKE_DATA({"name": 'test', 'v':
                         {"value": 4, 'unit': pq.m}}, composite=True)
        dcmm = MAKE_DATA({"name": 'test', 'value':
                         {"value": 4, 'unit': pq.mm}}, composite=True)
        dcm.convert_unit(dcmm)
        self.assertEqual(dcm.composite_key, ['name', 'value'])
        dcm2['v'] = 55

    def test_data_list(self):
        """ test ListData class
        """
        data_list_simpel = MAKE_DATA([3, 4, 5])
        self.assertEquals(data_list_simpel[0].value, 3)
        data_list_simpel[0] = 5
        self.assertEquals(data_list_simpel[0].value, 5)
        data_list_simpel[0] = 3
        with self.assertRaises(KeyError):
            data_list_simpel[-1] = 6
        with self.assertRaises(KeyError):
            self.assertEquals(data_list_simpel[3].value, 5)
        data_list_simpel.append(MAKE_DATA(5))
        self.assertEquals(len(data_list_simpel), 4)
        self.assertEquals(data_list_simpel[0].value, 3)
        data_list_simpel[2] = MAKE_DATA(5)
        data_list_Q = MAKE_DATA([3, 4, 5], unit=pq.cm)
        data_list_Q.append(MAKE_DATA(5, unit=pq.cm))
        data_list_Q[3] = 4

    def test_compite_data_error(self):
        """ test error raisin in composite data.
        """
        with self.assertRaises(TypeError):
            data.CompositeData(5)
        d1 = data.CompositeData({'i': 5})
        for (x, _) in d1.items():
            self.assertIn(x, d1.keys())
        d2 = data.CompositeData({'i': "test"})
        self.assertEqual(d1.is_compatible(d2), False)

    def test_copy_data(self):
        """ test for copy data function
        """
        dc1 = MAKE_DATA({"name": 'test', 'value':
                         {"value": 4, 'unit': pq.m}}, composite=True)
        dcc1 = data.copy_data(dc1)
        self.assertEqual(dcc1.value, dc1.value)
        ld1 = MAKE_DATA([5, 55, 100, 150])
        ldc1 = data.copy_data(ld1)
        self.assertEqual(ld1.value, ldc1.value)
        self.assertEqual(ld1.value, [5, 55, 100, 150])

    def test_list_data(self):
        """ test for ListData object
        """
        l1 = MAKE_DATA([MAKE_DATA(5), MAKE_DATA(6)])
        self.assertEqual(l1.value, [5, 6])
        del l1[1]
        self.assertEqual(str(l1), "[5]")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
