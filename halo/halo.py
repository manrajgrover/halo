# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import sys
import threading
import cursor
import time

from spinners.spinners import Spinners
from log_symbols.symbols import LogSymbols
from halo._utils import is_supported, colored_frame

class Halo(object):

    CLEAR_LINE = '\033[K'

    def __init__(self, options={}):
        if type(options) == unicode or type(options) == str:
            text = options
            options = {}
            options['text'] = text

        self._spinner = self._get_spinner(options)

        if 'frames' not in self._spinner:
            raise ValueError('Spinner must define frames')

        self._interval = options['interval'] if 'interval' in options else self._spinner['interval']
        self._text = options['text'] if 'text' in options else None
        self._color = options['color'] if 'color' in options else 'cyan'
        self._frame_index = 0
        self._spinner_thread = None
        self._stop_spinner = None
        self._enabled = options['enabled'] if 'enabled' in options else True # Need to check for stream

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

    def _get_spinner(self, options):
        if is_supported():
            default_spinner = Spinners['dots'].value

            if 'spinner' in options:
                spinner = options['spinner']
                if type(spinner) == dict:
                    return spinner
                elif spinner in Spinners.__members__:
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

        sys.stdout.write('\r')
        sys.stdout.write(self.CLEAR_LINE)
        sys.stdout.flush()

        return self

    def _render_frame(self):
        frame = self.frame()
        output = '\r{0}'.format(frame)
        self.clear()
        sys.stdout.write(output)

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

        if not self._enabled:
            return self

        if sys.stdout.isatty() is True:
            cursor.hide()
            self._stop_spinner = threading.Event()
            self._spinner_thread = threading.Thread(target=self.render)
            self._spinner_thread.setDaemon(True)
            self._render_frame()
            self._spinner_thread.start()

        return self

    def stop(self):
        if not self._enabled:
            return self

        if self._spinner_thread:
            self._stop_spinner.set()
            self._spinner_thread.join()

        self.clear()
        cursor.show()
        return self

    def succeed(self, text=''):
        return self.stop_and_persist({'symbol': LogSymbols.SUCCESS.value, 'text': text})

    def fail(self, text=''):
        return self.stop_and_persist({'symbol': LogSymbols.ERROR.value, 'text': text})

    def warn(self, text=''):
        return self.stop_and_persist({'symbol': LogSymbols.WARNING.value, 'text': text})

    def info(self, text=''):
        return self.stop_and_persist({'symbol': LogSymbols.INFO.value, 'text': text})

    def stop_and_persist(self, options={}):
        if type(options) is not dict:
            raise TypeError('Options passed must be a dictionary')

        if 'symbol' not in options or 'text' not in options:
            raise ValueError('Options must contain symbol and text keys')

        symbol = options['symbol'].decode('utf-8') if options['symbol'] is not None else ''
        text = options['text'].decode('utf-8') if options['text'] is not None else ''

        self.stop()

        output = u'{0} {1}\n'.format(symbol, text)
        sys.stdout.write(output)
        sys.stdout.flush()

        return self
