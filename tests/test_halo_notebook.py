# -*- coding: utf-8 -*-
"""This module tests HaloNotebook spinners.
"""
import os
import re
import sys
import time
import unittest

from spinners.spinners import Spinners

from halo import HaloNotebook
from halo._utils import get_terminal_columns, is_supported
from tests._utils import decode_utf_8_text, encode_utf_8_text, strip_ansi
from tests._utils import strip_ansi, find_colors, encode_utf_8_text, decode_utf_8_text

from termcolor import COLORS

if sys.version_info.major == 2:
    get_coded_text = encode_utf_8_text
else:
    get_coded_text = decode_utf_8_text


if is_supported():
    frames = [get_coded_text(frame) for frame in Spinners['dots'].value['frames']]
    default_spinner = Spinners['dots'].value
else:
    frames = [get_coded_text(frame) for frame in Spinners['line'].value['frames']]
    default_spinner = Spinners['line'].value


class TestHaloNotebook(unittest.TestCase):
    """Test HaloNotebook enum for attribute values.
    """
    TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        """Set up things before beginning of each test.
        """
        pass

    def _get_test_output(self, spinner):
        """Clean the output from Output widget and return it in list form.

        Returns
        -------
        list
            Clean output from Output widget
        """
        output = {}
        output_text = []
        output_colors = []

        for line in spinner.output.outputs:
            clean_line = strip_ansi(line['text'].strip('\r'))
            if clean_line != '':
                output_text.append(get_coded_text(clean_line))

            colors_found = find_colors(line['text'].strip('\r'))
            if colors_found:
                tmp = []
                for color in colors_found:
                    tmp.append(re.sub(r'[^0-9]', '', color, flags=re.I))
                output_colors.append(tmp)

        output['text'] = output_text
        output['colors'] = output_colors

        return output

    def test_basic_spinner(self):
        """Test the basic of basic spinners.
        """
        spinner = HaloNotebook(text='foo', spinner='dots')

        spinner.start()
        time.sleep(1)
        output = self._get_test_output(spinner)['text']
        spinner.stop()

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))
        self.assertEqual(spinner.output.outputs, spinner._output(''))

    def test_text_spinner_color(self):
        """Test basic spinner with available colors color (both spinner and text)
        """
        for color, color_int in COLORS.items():
            spinner = HaloNotebook(text='foo', text_color=color, color=color, spinner='dots')

            spinner.start()
            time.sleep(1)
            output = self._get_test_output(spinner)['colors']
            spinner.stop()

            # check if spinner colors match
            self.assertEqual(color_int, int(output[0][0]))
            self.assertEqual(color_int, int(output[1][0]))
            self.assertEqual(color_int, int(output[2][0]))

            # check if text colors match
            self.assertEqual(color_int, int(output[0][1]))
            self.assertEqual(color_int, int(output[1][1]))
            self.assertEqual(color_int, int(output[2][1]))

    def test_text_stripping(self):
        """Test the text being stripped before output.
        """
        spinner = HaloNotebook(text='foo\n', spinner='dots')

        spinner.start()
        time.sleep(1)
        output = self._get_test_output(spinner)['text']

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

        spinner.succeed('foo\n')
        output = self._get_test_output(spinner)['text']

        pattern = re.compile(r'(✔|v) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)

    def test_text_ellipsing(self):
        """Test the text gets ellipsed if it's too long
        """
        text = 'This is a text that it is too long. In fact, it exceeds the eighty column standard ' \
               'terminal width, which forces the text frame renderer to add an ellipse at the end of the ' \
               'text. ' * 6
        spinner = HaloNotebook(text=text, spinner='dots')

        spinner.start()
        time.sleep(1)
        output = self._get_test_output(spinner)['text']

        terminal_width = get_terminal_columns()

        # -6 of the ' (...)' ellipsis, -2 of the spinner and space
        self.assertEqual(output[0], '{0} {1} (...)'.format(frames[0], text[:terminal_width - 6 - 2]))
        self.assertEqual(output[1], '{0} {1} (...)'.format(frames[1], text[:terminal_width - 6 - 2]))
        self.assertEqual(output[2], '{0} {1} (...)'.format(frames[2], text[:terminal_width - 6 - 2]))

        spinner.succeed('End!')
        output = self._get_test_output(spinner)['text']

        pattern = re.compile(r'(✔|v) End!', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)

    def test_text_animation(self):
        """Test the text gets animated when it is too long
        """
        text = 'This is a text that it is too long. In fact, it exceeds the eighty column standard ' \
               'terminal width, which forces the text frame renderer to add an ellipse at the end of the ' \
               'text. ' * 6
        spinner = HaloNotebook(text=text, spinner='dots', animation='marquee')

        spinner.start()
        time.sleep(1)
        output = self._get_test_output(spinner)['text']

        terminal_width = get_terminal_columns()

        self.assertEqual(output[0], '{0} {1}'.format(frames[0], text[:terminal_width - 2]))
        self.assertEqual(output[1], '{0} {1}'.format(frames[1], text[1:terminal_width - 1]))
        self.assertEqual(output[2], '{0} {1}'.format(frames[2], text[2:terminal_width]))

        spinner.succeed('End!')
        output = self._get_test_output(spinner)['text']

        pattern = re.compile(r'(✔|v) End!', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)

    def test_context_manager(self):
        """Test the basic of basic spinners used through the with statement.
        """
        with HaloNotebook(text='foo', spinner='dots') as spinner:
            time.sleep(1)
            output = self._get_test_output(spinner)['text']

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))
        self.assertEqual(spinner.output.outputs, spinner._output(''))

    def test_decorator_spinner(self):
        """Test basic usage of spinners with the decorator syntax."""

        @HaloNotebook(text="foo", spinner="dots")
        def decorated_function():
            time.sleep(1)

            spinner = decorated_function.__closure__[1].cell_contents
            output = self._get_test_output(spinner)['text']
            return output

        output = decorated_function()

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

    def test_initial_title_spinner(self):
        """Test Halo with initial title.
        """
        spinner = HaloNotebook('bar')

        spinner.start()
        time.sleep(1)
        output = self._get_test_output(spinner)['text']
        spinner.stop()

        self.assertEqual(output[0], '{0} bar'.format(frames[0]))
        self.assertEqual(output[1], '{0} bar'.format(frames[1]))
        self.assertEqual(output[2], '{0} bar'.format(frames[2]))
        self.assertEqual(spinner.output.outputs, spinner._output(''))

    def test_id_not_created_before_start(self):
        """Test Spinner ID not created before start.
        """
        spinner = HaloNotebook()
        self.assertEqual(spinner.spinner_id, None)

    def test_ignore_multiple_start_calls(self):
        """Test ignoring of multiple start calls.
        """
        spinner = HaloNotebook()
        spinner.start()
        spinner_id = spinner.spinner_id
        spinner.start()
        self.assertEqual(spinner.spinner_id, spinner_id)
        spinner.stop()

    def test_chaining_start(self):
        """Test chaining start with constructor
        """
        spinner = HaloNotebook().start()
        spinner_id = spinner.spinner_id
        self.assertIsNotNone(spinner_id)
        spinner.stop()

    def test_succeed(self):
        """Test succeed method
        """
        spinner = HaloNotebook()
        spinner.start('foo')
        spinner.succeed('foo')

        output = self._get_test_output(spinner)['text']
        pattern = re.compile(r'(✔|v) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_succeed_with_new_text(self):
        """Test succeed method with new text
        """
        spinner = HaloNotebook()
        spinner.start('foo')
        spinner.succeed('bar')

        output = self._get_test_output(spinner)['text']
        pattern = re.compile(r'(✔|v) bar', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_info(self):
        """Test info method
        """
        spinner = HaloNotebook()
        spinner.start('foo')
        spinner.info()

        output = self._get_test_output(spinner)['text']
        pattern = re.compile(r'(ℹ|¡) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_fail(self):
        """Test fail method
        """
        spinner = HaloNotebook()
        spinner.start('foo')
        spinner.fail()

        output = self._get_test_output(spinner)['text']
        pattern = re.compile(r'(✖|×) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_warning(self):
        """Test warn method
        """
        spinner = HaloNotebook()
        spinner.start('foo')
        spinner.warn('Warning!')

        output = self._get_test_output(spinner)['text']
        pattern = re.compile(r'(⚠|!!) Warning!', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_spinner_getters_setters(self):
        """Test spinner getters and setters.
        """
        spinner = HaloNotebook()
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

        spinner.spinner = 'dots11'
        if is_supported():
            self.assertEqual(spinner.spinner, Spinners['dots11'].value)
        else:
            self.assertEqual(spinner.spinner, default_spinner)

        spinner.spinner = 'foo_bar'
        self.assertEqual(spinner.spinner, default_spinner)

        # Color is None
        spinner.color = None
        spinner.start()
        spinner.stop()
        self.assertIsNone(spinner.color)

    def test_unavailable_spinner_defaults(self):
        """Test unavailable spinner defaults.
        """
        spinner = HaloNotebook('dot')

        self.assertEqual(spinner.text, 'dot')
        self.assertEqual(spinner.spinner, default_spinner)

    def test_if_enabled(self):
        """Test if spinner is enabled
        """
        spinner = HaloNotebook(text="foo", enabled=False)
        spinner.start()
        time.sleep(1)
        output = self._get_test_output(spinner)['text']
        spinner.clear()
        spinner.stop()

        self.assertEqual(len(output), 0)
        self.assertEqual(output, [])

    def test_invalid_placement(self):
        """Test invalid placement of spinner.
        """

        with self.assertRaises(ValueError):
            HaloNotebook(placement='')
            HaloNotebook(placement='foo')
            HaloNotebook(placement=None)

        spinner = HaloNotebook(placement='left')
        with self.assertRaises(ValueError):
            spinner.placement = ''
            spinner.placement = 'foo'
            spinner.placement = None

    def test_default_placement(self):
        """Test default placement of spinner.
        """

        spinner = HaloNotebook()
        self.assertEqual(spinner.placement, 'left')

    def test_right_placement(self):
        """Test right placement of spinner.
        """
        spinner = HaloNotebook(text="foo", placement="right")
        spinner.start()
        time.sleep(1)

        output = self._get_test_output(spinner)['text']
        (text, _) = output[-1].split(" ")
        self.assertEqual(text, "foo")

        spinner.succeed()
        output = self._get_test_output(spinner)['text']
        (text, symbol) = output[-1].split(" ")
        pattern = re.compile(r"(✔|v)", re.UNICODE)

        self.assertEqual(text, "foo")
        self.assertRegexpMatches(symbol, pattern)
        spinner.stop()

    def tearDown(self):
        """Clean up things after every test.
        """
        pass


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestHaloNotebook)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
