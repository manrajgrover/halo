# -*- coding: utf-8 -*-
"""This module tests Halo spinners.
"""
import io
import os
import re
import sys
import time
import unittest

from colorama import Fore
from spinners.spinners import Spinners

from halo import Halo
from halo._utils import get_terminal_columns, is_supported
from tests._utils import decode_utf_8_text, encode_utf_8_text, strip_ansi

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


class TestHalo(unittest.TestCase):
    """Test Halo enum for attribute values.
    """
    TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def setUp(self):
        """Set up things before beginning of each test.
        """
        self._stream_file = os.path.join(self.TEST_FOLDER, 'test.txt')
        self._stream = io.open(self._stream_file, 'w+')

    def _get_test_output(self, no_ansi=True):
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
            clean_line = strip_ansi(line.strip('\n')) if no_ansi else line.strip('\n')
            if clean_line != '':
                output.append(get_coded_text(clean_line))

        return output

    def test_basic_spinner(self):
        """Test the basic of basic spinners.
        """
        spinner = Halo(text='foo', spinner='dots', stream=self._stream)

        spinner.start()
        time.sleep(1)
        spinner.stop()
        output = self._get_test_output()

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

    def test_spinner_getter(self):
        instance = Halo()
        if is_supported():
            default_spinner_value = "dots"
        else:
            default_spinner_value = "line"

        instance.spinner = default_spinner_value
        self.assertEqual(default_spinner, instance.spinner)

        instance.spinner = "This_spinner_do_not_exist"
        self.assertEqual(default_spinner, instance.spinner)

        instance.spinner = -123
        self.assertEqual(default_spinner, instance.spinner)

    def test_text_stripping(self):
        """Test the text being stripped before output.
        """
        spinner = Halo(text='foo\n', spinner='dots', stream=self._stream)

        spinner.start()
        time.sleep(1)
        spinner.succeed('foo\n')
        output = self._get_test_output()

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

        pattern = re.compile(r'(✔|v) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)

    def test_text_ellipsing(self):
        """Test the text gets ellipsed if it's too long
        """
        text = 'This is a text that it is too long. In fact, it exceeds the eighty column standard ' \
               'terminal width, which forces the text frame renderer to add an ellipse at the end of the ' \
               'text. ' * 6
        spinner = Halo(text=text, spinner='dots', stream=self._stream)

        spinner.start()
        time.sleep(1)
        spinner.succeed('End!')
        output = self._get_test_output()

        terminal_width = get_terminal_columns()

        # -6 of the ' (...)' ellipsis, -2 of the spinner and space
        self.assertEqual(output[0], '{0} {1} (...)'.format(frames[0], text[:terminal_width - 6 - 2]))
        self.assertEqual(output[1], '{0} {1} (...)'.format(frames[1], text[:terminal_width - 6 - 2]))
        self.assertEqual(output[2], '{0} {1} (...)'.format(frames[2], text[:terminal_width - 6 - 2]))

        pattern = re.compile(r'(✔|v) End!', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)

    def test_text_animation(self):
        """Test the text gets animated when it is too long
        """
        text = 'This is a text that it is too long. In fact, it exceeds the eighty column standard ' \
               'terminal width, which forces the text frame renderer to add an ellipse at the end of the ' \
               'text. ' * 6
        spinner = Halo(text=text, spinner='dots', stream=self._stream, animation='marquee')

        spinner.start()
        time.sleep(1)
        spinner.succeed('End!')
        output = self._get_test_output()

        terminal_width = get_terminal_columns()

        self.assertEqual(output[0], '{0} {1}'.format(frames[0], text[:terminal_width - 2]))
        self.assertEqual(output[1], '{0} {1}'.format(frames[1], text[1:terminal_width - 1]))
        self.assertEqual(output[2], '{0} {1}'.format(frames[2], text[2:terminal_width]))

        pattern = re.compile(r'(✔|v) End!', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)

    def test_context_manager(self):
        """Test the basic of basic spinners used through the with statement.
        """
        with Halo(text='foo', spinner='dots', stream=self._stream):
            time.sleep(1)
        output = self._get_test_output()

        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

    def test_decorator_spinner(self):
        """Test basic usage of spinners with the decorator syntax."""

        @Halo(text="foo", spinner="dots", stream=self._stream)
        def decorated_function():
            time.sleep(1)

        decorated_function()
        output = self._get_test_output()
        self.assertEqual(output[0], '{0} foo'.format(frames[0]))
        self.assertEqual(output[1], '{0} foo'.format(frames[1]))
        self.assertEqual(output[2], '{0} foo'.format(frames[2]))

    def test_initial_title_spinner(self):
        """Test Halo with initial title.
        """
        spinner = Halo('bar', stream=self._stream)

        spinner.start()
        time.sleep(1)
        spinner.stop()

        output = self._get_test_output()

        self.assertEqual(output[0], '{0} bar'.format(frames[0]))
        self.assertEqual(output[1], '{0} bar'.format(frames[1]))
        self.assertEqual(output[2], '{0} bar'.format(frames[2]))

    def test_id_not_created_before_start(self):
        """Test Spinner ID not created before start.
        """
        spinner = Halo(stream=self._stream)
        self.assertEqual(spinner.spinner_id, None)

    def test_ignore_multiple_start_calls(self):
        """Test ignoring of multiple start calls.
        """
        spinner = Halo(stream=self._stream)
        spinner.start()
        spinner_id = spinner.spinner_id
        spinner.start()
        self.assertEqual(spinner.spinner_id, spinner_id)
        spinner.stop()

    def test_chaining_start(self):
        """Test chaining start with constructor
        """
        spinner = Halo(stream=self._stream).start()
        spinner_id = spinner.spinner_id
        self.assertIsNotNone(spinner_id)
        spinner.stop()

    def test_succeed(self):
        """Test succeed method
        """
        spinner = Halo(stream=self._stream)
        spinner.start('foo')
        spinner.succeed('foo')

        output = self._get_test_output()
        pattern = re.compile(r'(✔|v) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_succeed_with_new_text(self):
        """Test succeed method with new text
        """
        spinner = Halo(stream=self._stream)
        spinner.start('foo')
        spinner.succeed('bar')

        output = self._get_test_output()
        pattern = re.compile(r'(✔|v) bar', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_info(self):
        """Test info method
        """
        spinner = Halo(stream=self._stream)
        spinner.start('foo')
        spinner.info()

        output = self._get_test_output()
        pattern = re.compile(r'(ℹ|¡) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_fail(self):
        """Test fail method
        """
        spinner = Halo(stream=self._stream)
        spinner.start('foo')
        spinner.fail()

        output = self._get_test_output()
        pattern = re.compile(r'(✖|×) foo', re.UNICODE)

        self.assertRegexpMatches(output[-1], pattern)
        spinner.stop()

    def test_warning(self):
        """Test warn method
        """
        spinner = Halo(stream=self._stream)
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
        spinner = Halo('dot')

        self.assertEqual(spinner.text, 'dot')
        self.assertEqual(spinner.spinner, default_spinner)

    def test_if_enabled(self):
        """Test if spinner is enabled
        """
        spinner = Halo(text="foo", enabled=False, stream=self._stream)
        spinner.start()
        time.sleep(1)
        spinner.clear()
        spinner.fail()

        output = self._get_test_output()
        self.assertEqual(len(output), 0)
        self.assertEqual(output, [])

    def test_spinner_interval_default(self):
        """Test proper assignment of the default interval value.
        """
        spinner = Halo()
        self.assertEqual(spinner._interval, default_spinner['interval'])

    def test_spinner_interval_argument(self):
        """Test proper assignment of the interval value from the constructor argument.
        """
        spinner = Halo(interval=123)
        self.assertEqual(spinner._interval, 123)

    def test_spinner_interval_dict(self):
        """Test proper assignment of the interval value from a dictionary.
        """
        spinner = Halo(spinner={'interval': 321, 'frames': ['+', '-']})
        self.assertEqual(spinner._interval, 321)

    def test_invalid_placement(self):
        """Test invalid placement of spinner.
        """

        with self.assertRaises(ValueError):
            Halo(placement='')
            Halo(placement='foo')
            Halo(placement=None)

        spinner = Halo(placement='left')
        with self.assertRaises(ValueError):
            spinner.placement = ''
            spinner.placement = 'foo'
            spinner.placement = None

    def test_default_placement(self):
        """Test default placement of spinner.
        """

        spinner = Halo()
        self.assertEqual(spinner.placement, 'left')

    def test_right_placement(self):
        """Test right placement of spinner.
        """
        spinner = Halo(text='foo', placement='right', stream=self._stream)
        spinner.start()
        time.sleep(1)

        output = self._get_test_output()
        (text, _) = output[-1].split(' ')
        self.assertEqual(text, 'foo')

        spinner.succeed()
        output = self._get_test_output()
        (text, symbol) = output[-1].split(' ')
        pattern = re.compile(r"(✔|v)", re.UNICODE)

        self.assertEqual(text, 'foo')
        self.assertRegexpMatches(symbol, pattern)
        spinner.stop()

    def test_bounce_animation(self):
        def filler_text(n_chars):
            return "_" * n_chars

        terminal_width = get_terminal_columns()

        text = "{}abc".format(filler_text(terminal_width))
        expected_frames_without_appended_spinner = [
            "{}".format(filler_text(terminal_width - 2)),
            "{}".format(filler_text(terminal_width - 2)),
            "{}".format(filler_text(terminal_width - 2)),
            "{}a".format(filler_text(terminal_width - 3)),
            "{}ab".format(filler_text(terminal_width - 4)),
            "{}abc".format(filler_text(terminal_width - 5)),
            "{}abc".format(filler_text(terminal_width - 5)),
            "{}ab".format(filler_text(terminal_width - 4)),
            "{}a".format(filler_text(terminal_width - 3)),
            "{}".format(filler_text(terminal_width - 2)),
            "{}".format(filler_text(terminal_width - 2)),
            "{}".format(filler_text(terminal_width - 2)),
        ]
        # Prepend the actual spinner
        expected_frames = [
            "{0} {1}".format(frames[idx % frames.__len__()], frame)
            for idx, frame in enumerate(expected_frames_without_appended_spinner)
        ]
        spinner = Halo(text, animation="bounce", stream=self._stream)
        spinner.start()
        # Sleep a full bounce cycle
        time.sleep(1.2)
        spinner.stop()
        output = self._get_test_output()

        zipped_expected_and_actual_frame = zip(expected_frames, output)
        for multiple_frames in zipped_expected_and_actual_frame:
            expected_frame, actual_frame = multiple_frames
            self.assertEquals(expected_frame, actual_frame)

    def test_animation_setter(self):
        spinner = Halo("Asdf")
        spinner.animation = "bounce"
        self.assertEquals("bounce", spinner.animation)
        spinner.animation = "marquee"
        self.assertEquals("marquee", spinner.animation)

    def test_spinner_color(self):
        """Test ANSI escape characters are present
        """
        colors = {
            'cyan': Fore.CYAN,
            'magenta': Fore.MAGENTA,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE
        }

        for k, v in colors.items():
            self._stream = io.open(self._stream_file, 'w+')  # reset stream
            spinner = Halo(color=k, stream=self._stream)
            spinner.start()
            spinner.stop()

            output = self._get_test_output(no_ansi=False)
            assert v in output[1]

    def tearDown(self):
        pass


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestHalo)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
