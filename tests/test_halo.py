# -*- coding: utf-8 -*-
"""This module tests Halo spinners.
"""
import re
import unittest
import time
import sys
import io
import logging

from spinners.spinners import Spinners

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

    def test_id_not_created_before_start(self):
        """Test Spinner ID not created before start.
        """
        spinner = Halo({'stream': self._stream})
        self.assertEqual(spinner.spinner_id, None)

    def test_ignore_multiple_start_calls(self):
        """Test ignoring of multiple start calls.
        """
        spinner = Halo({'stream': self._stream})
        spinner.start()
        spinner_id = spinner.spinner_id
        spinner.start()
        self.assertEqual(spinner.spinner_id, spinner_id)
        spinner.stop()

    def test_chaining_start(self):
        """Test chaining start with constructor
        """
        spinner = Halo({'stream': self._stream}).start()
        spinner_id = spinner.spinner_id
        self.assertIsNotNone(spinner_id)
        spinner.stop()

    def test_succeed(self):
        """Test succeed method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.succeed('foo')

        output = self._get_test_output()
        pattern = re.compile(ur'(✔|√) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1].decode('utf-8'), pattern)
        spinner.stop()

    def test_succeed_with_new_text(self):
        """Test succeed method with new text
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.succeed('bar')

        output = self._get_test_output()
        pattern = re.compile(ur'(✔|√) bar', re.UNICODE)

        self.assertRegexpMatches(output[-1].decode('utf-8'), pattern)
        spinner.stop()

    def test_info(self):
        """Test info method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.info()

        output = self._get_test_output()
        pattern = re.compile(ur'(ℹ|i) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1].decode('utf-8'), pattern)
        spinner.stop()

    def test_fail(self):
        """Test fail method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.fail()

        output = self._get_test_output()
        pattern = re.compile(ur'(✖|×) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1].decode('utf-8'), pattern)
        spinner.stop()

    def test_warning(self):
        """Test warn method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.warn('Warning!')

        output = self._get_test_output()
        pattern = re.compile(ur'(⚠|‼) Warning!', re.UNICODE)

        self.assertRegexpMatches(output[-1].decode('utf-8'), pattern)
        spinner.stop()

    def test_spinner_with_no_frames(self):
        """Test spinner with no frames.
        """

        with self.assertRaises(ValueError):
            spinner = Halo({'spinner': {'not_frame': []}})

    def test_spinner_getters_setters(self):
        """Test spinner getters and setters.
        """
        spinner = Halo()
        self.assertEqual(spinner.text, '')
        self.assertEqual(spinner.color, 'cyan')
        self.assertIsNone(spinner.spinner_id)

        spinner.spinner = 'dots12'
        spinner.text = 'bar'
        spinner.color = 'red'

        self.assertEqual(spinner.text, 'bar')
        self.assertEqual(spinner.color, 'red')
        self.assertEqual(spinner.spinner, Spinners['dots12'].value)


    def tearDown(self):
        """Summary
        """
        remove_file('test.txt')



if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestHalo)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
