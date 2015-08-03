# -*- coding: utf-8 -*-
from __future__ import (absolute_import)

import unittest
import sure
import time

from data_gather import ServiceMessage

DATA_FILE = "../test_data/preprocessed_data.txt"
ITERATIONS = -1


class TestMessageExtraction(unittest.TestCase):
    def setUp(self):
        self.test_file = file(DATA_FILE, 'r')

    def test_time_extraction(self):
        iters = 0
        for line in self.test_file.read().split('\n'):
            iters += 1
            print "Line: ", line

            test_time = ServiceMessage(line).extract_event_time()
            if ServiceMessage.is_valid_message(line):
                if isinstance(test_time, dict):
                    test_time.should.be.a(dict)
                else:
                    import pdb;
                    pdb.set_trace()
                test_time['hour'].should.be.an(int)
                test_time['min'].should.be.an(int)
            else:
                print line
                test_time.should.equal(None)
            if iters > ITERATIONS != -1:
                break

    def test_delay_extraction(self):
        iters = 0
        for line in self.test_file.read().split('\n'):
            iters += 1
            delay_time = ServiceMessage(line).extract_delay_value()
            if line.find('delay') > -1:
                print "Line: ", line[10:], '\n', delay_time
            if ServiceMessage.is_valid_message(line):
                if line.find('delay') > -1 and line.find('minute') > -1:
                    delay_time.should.be.a(dict)
                    delay_time.should.contain('minutes')
                    delay_time['minutes'].should.be.an(int)
                else:
                    delay_time.should.equal(None)
            if iters > ITERATIONS != -1:
                break

    def test_gap_extraction(self):
        iters = 0
        for line in self.test_file.read().split('\n'):
            iters += 1
            gap_time = ServiceMessage(line).extract_gap_value()
            if line.find('gap') > -1:
                print "Line: ", line[10:], '\n', gap_time
            if ServiceMessage.is_valid_message(line):
                if line.find('gap') > -1 and line.find('minute') > -1:
                    gap_time.should.be.a(dict)
                    gap_time.should.contain('minutes')
                    gap_time['minutes'].should.be.an(int)
                else:
                    gap_time.should.equal(None)
            if iters > ITERATIONS != -1:
                break


if __name__ == '__main__':
    unittest.main()
