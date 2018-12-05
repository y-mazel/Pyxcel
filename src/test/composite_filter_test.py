# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Created on 7 nov. 2014

@author: GP243515
"""
import unittest
import paf.data as data
import paf.pump_base
import paf.filter_base
import paf.port
import paf.pipe
import paf.sink_base
import paf.composite_filter as composite
import time
MAKE_DATA = data.make_data


class PumpInt(paf.pump_base.Pump):

    def run(self):
        for i in range(100):
            d = MAKE_DATA(i)
            self.fill_port("main", d)


class PumpIntTimming(paf.pump_base.Pump):

    def run(self):
        for i in range(50):
            d = MAKE_DATA(i)
            self.fill_port("main", d)
        time.sleep(.5)
        for i in range(50):
            d = MAKE_DATA(i+50)
            self.fill_port("main", d)


class AddFilter(paf.filter_base.Filter):

    def __init__(self):
        paf.filter_base.Filter.__init__(self)
        p = paf.port.Port(MAKE_DATA())
        self.input_port["add"] = p

    def run(self):
        x = self.get_data("main").value + self.get_data("add").value
        self.fill_port("main", MAKE_DATA(x))


class TestSink(paf.sink_base.Sink):
    def __init__(self, test):
        paf.sink_base.Sink.__init__(self)
        self.i = 0
        self.test = test

    def run(self):
        self.test.assertEqual(self.i*3, self.get_data("main").value)
        self.i = self.i + 1


class CompositeAdd(composite.CompositFilter):
    def __init__(self):
        composite.CompositFilter.__init__(self)
        p1 = paf.port.Port(MAKE_DATA())
        self.input_port["add1"] = p1
        p2 = paf.port.Port(MAKE_DATA())
        self.input_port["add2"] = p2
        p3 = paf.port.Port(MAKE_DATA())
        self.output_port["o2"] = p3
        filter1 = AddFilter()
        filter2 = AddFilter()
        paf.pipe.connect(self.get_input_pump("main"), filter1)
        paf.pipe.connect(self.get_input_pump("add1"), filter1, sink_port="add")
        paf.pipe.connect(filter1, filter2)
        paf.pipe.connect(self.get_input_pump("add2"), filter2, sink_port="add")
        paf.pipe.connect(filter2, self.get_output_sink("main"))
        paf.pipe.connect(filter2, self.get_output_sink("o2"))


class CompositeTest(unittest.TestCase):
    """ test for composite filter
    """

    def test_loop_1(self):
        pump1 = PumpInt()
        pump2 = PumpInt()
        pump3 = PumpIntTimming()
        printeSink = TestSink(self)
        filter1 = CompositeAdd()
        paf.pipe.connect(pump1, filter1)
        paf.pipe.connect(pump2, filter1, sink_port="add1")
        paf.pipe.connect(pump3, filter1, sink_port="add2")
        paf.pipe.connect(filter1, printeSink)
        pump1.start()
        pump2.start()
        pump3.start()
        self.assertEqual(pump3.running, True)
        self.assertEqual(pump3.is_finish, False)
        time.sleep(1.)
        self.assertEqual(pump3.running, False)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
