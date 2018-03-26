# -*- coding: utf-8 -*-
"""Example for custom spinner
"""
from __future__ import unicode_literals
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
