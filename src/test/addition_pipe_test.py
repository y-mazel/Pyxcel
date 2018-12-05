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
import paf.pipe
import paf.sink_base as sink
MAKE_DATA = data.make_data


class PumpInt(pump.Pump):
    """ pump for integer
    """

    def run(self):
        """ pump the integer for 0 to 99
        """
        for i in range(100):
            d = MAKE_DATA(i)
            self.fill_port("main", d)


class PumpInt_error(pump.Pump):
    """ pump for trying security
    """
    def __init__(self, test):
        """ initialization
        """
        pump.Pump.__init__(self, data_type=MAKE_DATA(1))
        self.test = test

    def run(self):
        """ raise Type error exception intercepted by assert.
        """
        for _ in range(100):
            d = MAKE_DATA("i")
            with self.test.assertRaises(TypeError):
                self.fill_port("main", d)

    def run1(self):
        """ undirect running
        """
        pump.Pump.run(self)


class AddFilter(filters.Filter):
    """ filter to add the 2 input
    """

    def __init__(self):
        """ initialization
        """
        filters.Filter.__init__(self, MAKE_DATA(1))
        p = port.Port(MAKE_DATA(1))
        self.input_port["add"] = p

    def run(self):
        """ Do the addition
        """
        x = self.get_data("main").value + self.get_data("add").value
        self.fill_port("main", MAKE_DATA(x))

    def run1(self):
        """ undirect running
        """
        filters.Filter.run(self)


class TestSink(sink.Sink):
    """ think for testing result of the addition.
    """
    def __init__(self, test):
        """ initialization
        """
        sink.Sink.__init__(self)
        self.i = 0
        self.test = test

    def reinit(self):
        """ special rewrite of reinit
        """
        self._data = {}
        self.i = 0

    def run(self):
        """ run
        """
        self.test.assertEqual(self.i*2, self.get_data("main").value)
        self.i = self.i + 1


class AddTest(unittest.TestCase):
    """ test a pipeline for addition.
    """

    def test_pipeline1(self):
        no_sink = paf.pipe.NoSink()
        pump1 = PumpInt()
        pump2 = PumpInt()
        testSink = TestSink(self)
        filter1 = AddFilter()
        paf.pipe.connect(pump1, filter1)
        paf.pipe.connect(pump2, filter1, sink_port="add")
        paf.pipe.connect(filter1, testSink)
        paf.pipe.connect(filter1, no_sink)
        pump1.start()
        pump2.start()

    def test_pipeline_stop(self):
        pump1 = PumpInt()
        pump2 = PumpInt()
        filter1 = AddFilter()
        paf.pipe.connect(pump1, filter1)
        paf.pipe.connect(pump2, filter1, sink_port="add")
        pump1.start()
        pump1.stop()
        pump2.start()
        pump2.stop()
        pump2.reinit()
        pump1.reinit()
        pump1.start()
        pump2.start()

    def test_spipeline1(self):
        pump1 = PumpInt()
        pump2 = PumpInt()
        testSink = TestSink(self)
        filter1 = AddFilter()
        paf.pipe.connect(pump1, filter1)
        paf.pipe.connect(pump2, filter1, sink_port="add")
        paf.pipe.connect(filter1, testSink)
        pump1.start()
        pump2.start()

    def test_raise_to_many_input_error(self):
        filter1 = AddFilter()
        pump1 = PumpInt()
        paf.pipe.connect(pump1, filter1)
        with self.assertRaises(port.ToManyInputError):
            paf.pipe.connect(pump1, filter1)
        filter1.run1()

    def test_connect(self):
        pump1 = PumpInt()
        pump2 = PumpInt()
        testSink = TestSink(self)
        filter1 = AddFilter()
        p1 = paf.pipe.connect(pump1, filter1)
        p2 = paf.pipe.connect(pump2, filter1, sink_port="add")
        p3 = paf.pipe.connect(filter1, testSink)
        pump1.start()
        pump2.start()
        pump1.stop()
        pump2.stop()
        filter1.stop()
        testSink.stop()
        pump1.reinit()
        pump2.reinit()
        testSink.reinit()
        p1.clear()
        p2.clear()
        p3.clear()
        pump1.start()
        pump2.start()

    def test_connect2(self):
        pump1 = PumpInt()
        pump2 = PumpInt()
        testSink = TestSink(self)
        filter1 = AddFilter()
        paf.pipe.connect(pump1, filter1)
        paf.pipe.connect(pump2, filter1, sink_port="add")
        paf.pipe.connect(filter1, testSink)
        pump1.start()
        pump2.start()

    def test_pipe_connect(self):
        p = paf.pipe.Pipe(MAKE_DATA(1))
        p.fill(MAKE_DATA(2))
        p.clear()
        with self.assertRaises(IndexError):
            p.pop()
        p.output = TestSink(self)

    def test_pump_run(self):
        p = PumpInt_error(self)
        p.run1()


if __name__ == "__main__":
    unittest.main()
