# -*- coding: utf-8 -*-
"""This module tests Halo spinners.
"""
import re
import unittest
import time
import sys
import requests
import io
import logging

from _utils import strip_ansi, remove_file
from halo.halo import Halo


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


class TestHalo(unittest.TestCase):
    """Test Halo enum for attribute values.
    """

    def setUp(self):
        """Summary
        """
        self._stream = io.open('test.txt', 'w+')

    def _get_test_output(self):
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
        self._stream.seek(0)
        data = self._stream.readlines()
        output = []

        for line in data:
            clean_line = strip_ansi(line.strip('\n'))
            if clean_line != '':
                output.append(clean_line.encode('utf-8'))

        return output

    def test_basic_spinner(self):
        """Test the basic of basic spinners.
        """
        spinner = Halo({'text': 'foo', 'spinner': 'dots', 'stream': self._stream})
        spinner.start()
        time.sleep(1)
        spinner.stop()
        output = self._get_test_output()

        self.assertEqual(output[0], '⠋ foo')
        self.assertEqual(output[1], '⠙ foo')
        self.assertEqual(output[2], '⠹ foo')

    def test_initial_title_spinner(self):
        """Test Halo with initial title.
        """
        stdout_ = sys.stdout
        sys.stdout = self._stream
        spinner = Halo('bar')

        spinner.start()
        time.sleep(1)
        spinner.stop()
        sys.stdout = stdout_

        output = self._get_test_output()

        self.assertEqual(output[0], '⠋ bar')
        self.assertEqual(output[1], '⠙ bar')
        self.assertEqual(output[2], '⠹ bar')


    def tearDown(self):
        """Summary
        """
        remove_file('test.txt')



if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestHalo)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
