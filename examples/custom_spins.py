# -*- coding: utf-8 -*-
"""Examples for halo.
"""
from __future__ import unicode_literals, absolute_import, print_function
import os
import time

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

spinner = Halo(
    text='Custom Spins',
    spinner={
        'interval': 100,
        'frames': ['-', '+', '*', '+', '-']
    }
)

try:
    spinner.start()
    time.sleep(2)
    spinner.succeed('It works!')
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
