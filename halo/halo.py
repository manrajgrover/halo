# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
from __future__ import unicode_literals, absolute_import, print_function

import sys
import threading
import cursor
import time
import logging

from spinners.spinners import Spinners
from log_symbols.symbols import LogSymbols
from halo._utils import is_supported, colored_frame, is_text_type, decode_utf_8_text



logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


class Halo(object):

    CLEAR_LINE = '\033[K'

    def __init__(self, options={}):
        if is_text_type(options):
            text = options
            options = {}
            options['text'] = text

        self._spinner = self._get_spinner(options)

        if 'frames' not in self._spinner:
            raise ValueError('Spinner must define frames')

        self._options = {
            'interval': self._spinner['interval'],
            'text': '',
            'color': 'cyan',
            'enabled': True,
            'stream': sys.stdout
        }

        self._options.update(options)

        self._interval = self._options['interval']
        self._text = self._options['text']
        self._color = self._options['color']
        self._stream = self._options['stream']
        logging.debug(self._stream)
        self._frame_index = 0
        self._spinner_thread = None
        self._stop_spinner = None
        self._spinner_id = None
        self._enabled = self._options['enabled'] # Need to check for stream

    @property
    def spinner(self):
        return self._spinner

    @spinner.setter
    def spinner(self, options):
        self._spinner = self._get_spinner(options)
        self._frame_index = 0

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def spinner_id(self):
        return self._spinner_id

    def _get_spinner(self, options):
        if is_supported():
            default_spinner = Spinners['dots'].value

            if type(options) == dict and 'spinner' in options:
                spinner = options['spinner']

                if type(spinner) == dict:
                    return spinner
                elif is_text_type(spinner):
                    if spinner in Spinners.__members__:
                        return Spinners[spinner].value
                    else:
                        return default_spinner
            elif is_text_type(options):
                spinner = options

                if spinner in Spinners.__members__:
                    return Spinners[spinner].value
                else:
                    return default_spinner
            else:
                return default_spinner
        else:
            return Spinners['line'].value

    def clear(self):
        if not self._enabled:
            return self

        self._stream.write('\r')
        self._stream.write(self.CLEAR_LINE)

        return self

    def _render_frame(self):
        frame = self.frame()
        output = '\r{0}'.format(frame)
        self.clear()
        self._stream.write(output)

    def render(self):
        while not self._stop_spinner.is_set():
            self._render_frame()
            time.sleep(0.001 * self._interval)

        return self

    def frame(self):
        frames = self._spinner['frames']
        frame = frames[self._frame_index]

        if self._color:
            frame = colored_frame(frame, self._color)

        self._frame_index += 1
        self._frame_index = self._frame_index % len(frames)

        return frame + ' ' + self._text

    def start(self, text=None):
        if text is not None:
            self._text = text

        if not self._enabled or self._spinner_id is not None:
            return self

        if self._stream.isatty():
            cursor.hide()

        self._stop_spinner = threading.Event()
        self._spinner_thread = threading.Thread(target=self.render)
        self._spinner_thread.setDaemon(True)
        self._render_frame()
        self._spinner_id = self._spinner_thread.name
        self._spinner_thread.start()

        return self

    def stop(self):
        if not self._enabled:
            return self

        if self._spinner_thread:
            self._stop_spinner.set()
            self._spinner_thread.join()

        self._frame_index = 0
        self._spinner_id = None
        self.clear()

        if self._stream.isatty():
            cursor.show()

        return self

    def succeed(self, text=None):
        text = self._text if text is None else text
        return self.stop_and_persist({'symbol': LogSymbols.SUCCESS.value, 'text': text})

    def fail(self, text=None):
        text = self._text if text is None else text
        return self.stop_and_persist({'symbol': LogSymbols.ERROR.value, 'text': text})

    def warn(self, text=None):
        text = self._text if text is None else text
        return self.stop_and_persist({'symbol': LogSymbols.WARNING.value, 'text': text})

    def info(self, text=None):
        text = self._text if text is None else text
        return self.stop_and_persist({'symbol': LogSymbols.INFO.value, 'text': text})

    def stop_and_persist(self, options={}):
        if type(options) is not dict:
            raise TypeError('Options passed must be a dictionary')

        if 'symbol' not in options or 'text' not in options:
            raise ValueError('Options must contain symbol and text keys')

        symbol = decode_utf_8_text(options['symbol']) if options['symbol'] is not None else ''
        text = decode_utf_8_text(options['text']) if options['text'] is not None else ''

        self.stop()

        output = u'{0} {1}\n'.format(symbol, text)
        self._stream.write(output)

        return self
