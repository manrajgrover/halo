# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import sys
import threading
import cursor
import time

from spinners.spinners import Spinners
from log_symbols.symbols import LogSymbols
from halo._utils import is_supported, colored_text

class Halo(object):

    CLEAR_LINE = '\033[K'

    def __init__(self, options):
        if type(options) == unicode:
            text = options
            options = {}
            options['text'] = text

        if is_supported():
            if 'spinner' in options:
                spinner = option['spinner']
                if type(spinner) == dict:
                    self._spinner = spinner
                elif spinner in Spinners:
                    self._spinner = Spinners[spinner].value
            else:
                self._spinner = Spinners['dots'].value
        else:
            self._spinner = Spinners['line'].value

        if 'frames' not in self._spinner:
            raise Exception('Spinner must define frames')

        self._interval = options['interval'] if 'interval' in options else self._spinner['interval']
        self._text = options['text'] if 'text' in options else None
        self._color = options['color'] if 'color' in options else None
        self._frame_index = 0
        self._spinner_thread = None
        self._stop_spinner = None
        self._enabled = options['enabled'] if 'enabled' in options else True # Need to check for stream

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

    def clear(self):
        if self._enabled is None:
            return self

        sys.stdout.write('\r')
        sys.stdout.write(self.CLEAR_LINE)
        sys.stdout.flush()

    def render(self):
        while not self._stop_spinner.is_set():
            frame = self.frame()
            output = '\r{0}'.format(frame)
            self.clear()
            sys.stdout.write(output)
            time.sleep(0.001 * self._interval)

    def frame(self):
        frames = self._spinner['frames']
        frame = frames[self._frame_index]

        if self._color:
            frame = colored_text(frame, self._color)

        self._frame_index += 1
        self._frame_index = self._frame_index % len(frames)

        return frame + ' ' + self._text

    def start(self, text=None):
        if text is not None:
            self._text = text

        if self._enabled is None:
            return self

        if sys.stdout.isatty() is True:
            cursor.hide()
            self._stop_spinner = threading.Event()
            self._spinner_thread = threading.Thread(target=self.render)
            self._spinner_thread.start()

    def stop(self):
        if self._enabled is None:
            return self

        if self._spinner_thread:
            self._stop_spinner.set()
            self._spinner_thread.join()

        self.clear()
        cursor.show()

    def success(self, text):
        return self.stop_and_persist({'symbol': LogSymbols.SUCCESS, 'text': text})

    def fail(self, text):
        return self.stop_and_persist({'symbol': LogSymbols.FAIL, 'text': text})

    def warn(self, text):
        return self.stop_and_persist({'symbol': LogSymbols.WARN, 'text': text})

    def info(self, text):
        return self.stop_and_persist({'symbol': LogSymbols.INFO, 'text': text})

    def stop_and_persist(self, options):
        return self
