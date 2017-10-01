# -*- coding: utf-8 -*-
"""This module tests Halo spinners.
"""
import re
import unittest
import time
import sys
import io
import logging
import os

from spinners.spinners import Spinners

from tests._utils import strip_ansi, remove_file, encode_utf_8_text, decode_utf_8_text
from halo import Halo
from halo._utils import is_supported

if sys.version_info.major == 2:
    get_coded_text = encode_utf_8_text
else:
    get_coded_text = decode_utf_8_text


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

if is_supported():
    frames = [get_coded_text(frame) for frame in Spinners['dots'].value['frames']]
    default_spinner = Spinners['dots'].value
else:
    frames = [get_coded_text(frame) for frame in Spinners['line'].value['frames']]
    default_spinner = Spinners['line'].value


class TestHalo(unittest.TestCase):
    """Test Halo enum for attribute values.
    """
    TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        """Set up things before beginning of each test.
        """
        self._stream_file = os.path.join(self.TEST_FOLDER, 'test.txt')
        self._stream = io.open(self._stream_file, 'w+')

    def _get_test_output(self):
        """Clean the output from stream and return it in list form.
        
        Returns
        -------
        list
            Clean output from stream
        """
        self._stream.seek(0)
        data = self._stream.readlines()
        output = []

        for line in data:
            clean_line = strip_ansi(line.strip('\n'))
            if clean_line != '':
                output.append(get_coded_text(clean_line))

        return output

    def test_basic_spinner(self):
        """Test the basic of basic spinners.
        """
        spinner = Halo({'text': 'foo', 'spinner': 'dots', 'stream': self._stream})
        spinner.start()
        time.sleep(1)
        spinner.stop()
        output = self._get_test_output()

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

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

        self.assertEqual(output[0], '{0} bar'.format(frames[0]))
        self.assertEqual(output[1], '{0} bar'.format(frames[1]))
        self.assertEqual(output[2], '{0} bar'.format(frames[2]))

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
        pattern = re.compile(r'(✔|v) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_succeed_with_new_text(self):
        """Test succeed method with new text
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.succeed('bar')

        output = self._get_test_output()
        pattern = re.compile(r'(✔|v) bar', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_info(self):
        """Test info method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.info()

        output = self._get_test_output()
        pattern = re.compile(r'(ℹ|¡) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_fail(self):
        """Test fail method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.fail()

        output = self._get_test_output()
        pattern = re.compile(r'(✖|×) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_warning(self):
        """Test warn method
        """
        spinner = Halo({'stream': self._stream})
        spinner.start('foo')
        spinner.warn('Warning!')

        output = self._get_test_output()
        pattern = re.compile(r'(⚠|!!) Warning!', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

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

        if is_supported():
            self.assertEqual(spinner.spinner, Spinners['dots12'].value)
        else:
            self.assertEqual(spinner.spinner, default_spinner)

        spinner.spinner = {'spinner': 'dots11'}
        if is_supported():
            self.assertEqual(spinner.spinner, Spinners['dots11'].value)
        else:
            self.assertEqual(spinner.spinner, default_spinner)

        spinner.spinner = {'spinner': 'foo_bar'}
        self.assertEqual(spinner.spinner, default_spinner)

        # Color is None
        spinner.color = None
        spinner.start()
        spinner.stop()
        self.assertIsNone(spinner.color)

    def test_unavailable_spinner_defaults(self):
        """Test unavailable spinner defaults.
        """
        spinner = Halo('dot')

        self.assertEqual(spinner.text, 'dot')
        self.assertEqual(spinner.spinner, default_spinner)

    def test_if_enabled(self):
        """Test if spinner is enabled
        """
        stdout_ = sys.stdout
        sys.stdout = self._stream
        spinner = Halo({'text': 'foo', 'enabled': False})
        spinner.start()
        time.sleep(1)
        spinner.clear()
        spinner.stop()
        sys.stdout = stdout_

        output = self._get_test_output()
        self.assertEqual(len(output), 0)
        self.assertEqual(output, [])

    def test_stop_and_persist_no_dict_or_options(self):
        """Test if options is not dict or required options in stop_and_persist.
        """
        with self.assertRaises(TypeError):
            spinner = Halo()
            spinner.start()
            spinner.stop_and_persist('not dict')


    def tearDown(self):
        """Clean up things after every test.
        """
        self._stream.close()
        remove_file(self._stream_file)



if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestHalo)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
