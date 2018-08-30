# -*- coding: utf-8 -*-
"""Example for doge spinner ;)
"""
from __future__ import unicode_literals, absolute_import, print_function
import os
import time

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

spinner = Halo(text='Such Spins', text_color='red', color='red', spinner='dots')

try:
    spinner.start()
    time.sleep(3)
    spinner.stop()
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
