# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Beautiful terminal spinners in Python.
"""
from __future__ import unicode_literals, absolute_import, print_function

import sys
import signal
import threading
import time
import functools

import cursor
from spinners.spinners import Spinners
from log_symbols.symbols import LogSymbols

from halo._utils import is_supported, colored_frame, is_text_type, decode_utf_8_text, get_terminal_columns


class Halo(object):
    """Halo library.
    Attributes
    ----------
    CLEAR_LINE : str
        Code to clear the line
    """

    CLEAR_LINE = '\033[K'

    def __init__(self, text='', color='cyan', spinner=None, animation=None, interval=-1, enabled=True, stream=None):
        """Constructs the Halo object.
        Parameters
        ----------
        text : str, optional
            Text to display.
        color : str, optional
            Color of the text to display.
        spinner : str|dict, optional
            Spinner dict|str.
        interval : integer, optional
            Interval between each frame of the spinner in milliseconds.
        enabled : boolean, optional
            Spinner enabled or not.
        stream : io, optional
            Output.
        """

        self._spinner = self._get_spinner(spinner)

        self._text = self._get_text(text, animation)

        if int(interval) > 0:
            self._interval = int(interval)
        else:
            self._interval = self._spinner['interval']

        self._color = color

        if not stream:
            stream = sys.stdout

        self._stream = stream
        self._frame_index = 0
        self._text_index = 0
        self._spinner_thread = None
        self._stop_spinner = None
        self._spinner_id = None
        self._enabled = enabled  # Need to check for stream

        def handle_keyboard_interrupt(signal, frame):
            """Handle KeyboardInterrupt without try-except statement"""
            self.stop()
            raise KeyboardInterrupt

        signal.signal(signal.SIGINT, handle_keyboard_interrupt)

    def __enter__(self):
        """Starts the spinner on a separate thread. For use in context managers.
        Returns
        -------
        self
        """
        return self.start()

    def __exit__(self, type, value, traceback):
        """Stops the spinner. For use in context managers.
        Returns
        -------
        None
        """
        self.stop()

    def __call__(self, f):
        """Allow the Halo object to be used as a regular function decorator."""
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            with self:
                return f(*args, **kwargs)

        return wrapped

    @property
    def spinner(self):
        """Getter for spinner property.
        Returns
        -------
        dict
            spinner value
        """
        return self._spinner

    @spinner.setter
    def spinner(self, spinner=None):
        """Setter for spinner property.
        Parameters
        ----------
        spinner : dict, str
            Defines the spinner value with frame and interval
        """

        self._spinner = self._get_spinner(spinner)
        self._frame_index = 0
        self._text_index = 0

    @property
    def text(self):
        """Getter for text property.
        Returns
        -------
        str
            text value
        """
        return self._text['original']

    @text.setter
    def text(self, text):
        """Setter for text property.
        Parameters
        ----------
        text : str
            Defines the text value for spinner
        """
        self._text = self._get_text(text, animation=None)

    @property
    def color(self):
        """Getter for color property.
        Returns
        -------
        str
            color value
        """
        return self._color

    @color.setter
    def color(self, color):
        """Setter for color property.
        Parameters
        ----------
        color : str
            Defines the color value for spinner
        """
        self._color = color

    @property
    def spinner_id(self):
        """Getter for spinner id
        Returns
        -------
        str
            spinner id value
        """
        return self._spinner_id

    def _get_spinner(self, spinner):
        """Extracts spinner value from options and returns value
        containing spinner frames and interval, defaults to 'dots' spinner.
        Parameters
        ----------
        spinner : dict, str
            Contains spinner value or type of spinner to be used
        Returns
        -------
        dict
            Contains frames and interval defining spinner
        """
        default_spinner = Spinners['dots'].value

        if spinner and type(spinner) == dict:
            return spinner

        if is_supported():
            if all([is_text_type(spinner), spinner in Spinners.__members__]):
                return Spinners[spinner].value
            else:
                return default_spinner
        else:
            return Spinners['line'].value

    def _get_text(self, text, animation):
        """Creates frames based on the selected animation
        Returns
        -------
        self
        """
        stripped_text = text.strip()

        # Check which frame of the animation is the widest
        max_spinner_length = max([len(i) for i in self._spinner['frames']])

        # Subtract to the current terminal size the max spinner length
        # (-1 to leave room for the extra space between spinner and text)
        terminal_width = get_terminal_columns() - max_spinner_length - 1
        text_length = len(stripped_text)

        frames = []

        if terminal_width < text_length and animation:
            if animation == 'bounce':
                """
                Make the text bounce back and forth
                """
                for x in range(0, text_length - terminal_width):
                    frames.append(stripped_text[x:terminal_width + x])
                frames.extend(list(reversed(frames)))
            elif 'marquee':
                """
                Make the text scroll like a marquee
                """
                stripped_text = stripped_text + ' ' + stripped_text[:terminal_width]
                for x in range(0, text_length + 1):
                    frames.append(stripped_text[x:terminal_width + x])
        elif terminal_width < text_length and not animation:
            # Add ellipsis if text is larger than terminal width and no animation was specified
            frames = [stripped_text[:terminal_width - 6] + ' (...)']
        else:
            frames = [stripped_text]

        return {
            'original': text,
            'frames': frames
        }

    def clear(self):
        """Clears the line and returns cursor to the start.
        of line
        Returns
        -------
        self
        """
        if not self._enabled:
            return self

        self._stream.write('\r')
        self._stream.write(self.CLEAR_LINE)

        return self

    def _render_frame(self):
        """Renders the frame on the line after clearing it.
        """
        frame = self.frame()
        output = '\r{0}'.format(frame)
        self.clear()
        self._stream.write(output)

    def render(self):
        """Runs the render until thread flag is set.
        Returns
        -------
        self
        """
        while not self._stop_spinner.is_set():
            self._render_frame()
            time.sleep(0.001 * self._interval)

        return self

    def frame(self):
        """Builds and returns the frame to be rendered
        Returns
        -------
        self
        """
        frames = self._spinner['frames']
        frame = frames[self._frame_index]

        if self._color:
            frame = colored_frame(frame, self._color)

        self._frame_index += 1
        self._frame_index = self._frame_index % len(frames)

        return frame + ' ' + self.text_frame()

    def text_frame(self):
        """Builds and returns the text frame to be rendered
        Returns
        -------
        self
        """
        if len(self._text['frames']) == 1:
            # Return first frame (can't return original text because at this point it might be ellipsed)
            return self._text['frames'][0]

        frames = self._text['frames']
        frame = frames[self._text_index]

        self._text_index += 1
        self._text_index = self._text_index % len(frames)

        return frame

    def start(self, text=None):
        """Starts the spinner on a separate thread.
        Parameters
        ----------
        text : None, optional
            Text to be used alongside spinner
        Returns
        -------
        self
        """
        if text is not None:
            self._text = self._get_text(text, animation=None)

        if not self._enabled or self._spinner_id is not None:
            return self

        if self._stream.isatty():
            cursor.hide(stream=self._stream)

        self._stop_spinner = threading.Event()
        self._spinner_thread = threading.Thread(target=self.render)
        self._spinner_thread.setDaemon(True)
        self._render_frame()
        self._spinner_id = self._spinner_thread.name
        self._spinner_thread.start()

        return self

    def stop(self):
        """Stops the spinner and clears the line.
        Returns
        -------
        self
        """
        if not self._enabled:
            return self

        if self._spinner_thread:
            self._stop_spinner.set()
            self._spinner_thread.join()

        self._frame_index = 0
        self._spinner_id = None
        self.clear()

        if self._stream.isatty():
            cursor.show(stream=self._stream)

        return self

    def succeed(self, text=None):
        """Shows and persists success symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside success symbol.
        Returns
        -------
        self
        """
        return self.stop_and_persist({'symbol': LogSymbols.SUCCESS.value, 'text': text})

    def fail(self, text=None):
        """Shows and persists fail symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside fail symbol.
        Returns
        -------
        self
        """
        return self.stop_and_persist({'symbol': LogSymbols.ERROR.value, 'text': text})

    def warn(self, text=None):
        """Shows and persists warn symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside warn symbol.
        Returns
        -------
        self
        """
        return self.stop_and_persist({'symbol': LogSymbols.WARNING.value, 'text': text})

    def info(self, text=None):
        """Shows and persists info symbol and text and exits.
        Parameters
        ----------
        text : None, optional
            Text to be shown alongside info symbol.
        Returns
        -------
        self
        """
        return self.stop_and_persist({'symbol': LogSymbols.INFO.value, 'text': text})

    def stop_and_persist(self, options={}):
        """Stops the spinner and persists the final frame to be shown.
        Parameters
        ----------
        options : dict, optional
            Contains frame and interval for final frame
        Returns
        -------
        self
        Raises
        ------
        TypeError
            If options is not dictionary
        """
        if not self._enabled:
            return self

        if type(options) is not dict:
            raise TypeError('Options passed must be a dictionary')

        if 'symbol' in options and options['symbol'] is not None:
            symbol = decode_utf_8_text(options['symbol'])
        else:
            symbol = ' '

        if 'text' in options and options['text'] is not None:
            text = decode_utf_8_text(options['text'])
        else:
            text = self._text['original']

        text = text.strip()

        self.stop()

        output = u'{0} {1}\n'.format(symbol, text)
        self._stream.write(output)

        return self
