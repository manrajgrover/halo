# -*- coding: utf-8 -*-
"""Example for text wrapping animation
"""
from __future__ import unicode_literals
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

spinner = Halo(text='This is a text that it is too long. In fact, it exceeds the eighty column standard '
                    'terminal width, which forces the text frame renderer to add an ellipse at the end of the '
                    'text. This should definitely make it more than 180!', spinner='dots', animation='marquee')

try:
    spinner.start()
    time.sleep(15)
    spinner.succeed('End!')
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
