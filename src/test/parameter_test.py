# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Created on 7 nov. 2014

@author: GP243515
"""
import unittest
import paf.pump_base
import paf.data
import quantities as pq
MAKE_DATA = paf.data.make_data


class megaPump (paf.pump_base.Pump):
    def __init__(self):
        paf.pump_base.Pump.__init__(self)
        self.add_expected_parameter("name", MAKE_DATA(1), 1)

    def run(self):
        paf.pump_base.Pump.run(self)


class ParamUnit(paf.pump_base.Pump):
    def __init__(self):
        paf.pump_base.Pump.__init__(self)
        self.add_expected_parameter("name", MAKE_DATA(1, unit=pq.m), 1)

    def run(self):
        paf.pump_base.Pump.run(self)


class ParameterTest(unittest.TestCase):
    def test_base_param(self):
        mp = megaPump()
        mp["name"] = 3
        self.assertEquals(mp["name"].value, 3)
        self.assertEquals(mp.parameter_list, ["name"])
        data = mp.to_composite_data()
        data["name"] = 55
        self.assertEqual(data["name"].value, mp["name"].value)

    def test_instance_data(self):
        mp = megaPump()
        mp.add_expected_parameter("name2", MAKE_DATA({'value': 3, 'oui':
                                                      'non'}, composite=True),
                                  {'value': 3, 'oui': 'non'})
        mp["name"] = MAKE_DATA(3)
        mp["name2"].value

    def test_Param_Unit(self):
        p = ParamUnit()
        p['name'] = 40
        p.get_expected_data_type('name').is_compatible(MAKE_DATA(0,
                                                                 unit=pq.cm))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
