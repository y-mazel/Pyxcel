# pylint: disable=import-error
# -*- coding: utf8 -*-
"""
Created on 24 oct. 2014

@author: GP243515
"""
import unittest
import paf.data as data
import paf.pump_base as pump
import paf.filter_base as filters
import paf.port as port
import paf.pipe as pipe
import paf.sink_base as sink
import paf.loop_filter as loop
import time
MAKE_DATA = data.make_data
N = 5


class PumpInt(pump.Pump):

    def run(self):
        for i in range(100):
            d = MAKE_DATA(i)
            self.fill_port("main", d)


class AddFilter(filters.Filter):

    def __init__(self):
        filters.Filter.__init__(self)
        p = port.Port(MAKE_DATA())
        self.input_port["add"] = p

    def run(self):
        x = self.get_data("main").value + self.get_data("add").value
        self.fill_port("main", MAKE_DATA(x))


class TestSink(sink.Sink):
    def __init__(self, test):
        sink.Sink.__init__(self)
        self.i = 0
        self.test = test

    def run(self):
        self.test.assertEqual(self.i*3**N, self.get_data("main").value)
        self.i = self.i + 1


class LoopAdd(loop.LoopFilter):
    def __init__(self, test):
        self.test = test
        loop.LoopFilter.__init__(self, N)
        p1 = port.Port(MAKE_DATA(0))
        self.add_port("add1", p1)
        p2 = port.Port(MAKE_DATA(0))
        self.add_port("add2", p2)
        filter1 = AddFilter()
        filter2 = AddFilter()
        pipe.connect(self.get_input_pump("main"), filter1)
        pipe.connect(self.get_input_pump("add1"), filter1, sink_port="add")
        pipe.connect(filter1, filter2)
        pipe.connect(self.get_input_pump("add2"), filter2, sink_port="add")
        pipe.connect(filter2, self.get_output_sink("main"))
        pipe.connect(filter2, self.get_output_sink("add1"))
        pipe.connect(filter2, self.get_output_sink("add2"))


class LoopAdd_error_in(loop.LoopFilter):
    def __init__(self, test):
        loop.LoopFilter.__init__(self, N)
        p1 = port.Port(MAKE_DATA())
        self.add_port("add1", p1)
        p2 = port.Port(MAKE_DATA())
        self.add_port("add2", p2)


class LoopAdd_error_out(loop.LoopFilter):
    def __init__(self, test):
        loop.LoopFilter.__init__(self, N)
        p1 = port.Port(MAKE_DATA())
        self.add_port("add1", p1)
        p2 = port.Port(MAKE_DATA())
        self.add_port("add2", p2)


class LoopTest(unittest.TestCase):

    def test_loop_1(self):
        pump1 = PumpInt()
        pump2 = PumpInt()
        pump3 = PumpInt()
        printeSink = TestSink(self)
        filter1 = LoopAdd(self)
        pipe.connect(pump1, filter1)
        pipe.connect(pump2, filter1, sink_port="add1")
        pipe.connect(pump3, filter1, sink_port="add2")
        pipe.connect(filter1, printeSink)
        pump1.start()
        pump2.start()
        pump3.start()
        time.sleep(1)

    def test_loop_2(self):
        LoopAdd_error_in(self)

    def test_loop_3(self):
        LoopAdd_error_out(self)

    def test_looper(self):
        looper = loop.Looper(None)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
