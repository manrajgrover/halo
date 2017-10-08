# -*- coding: utf-8 -*-
"""Examples for halo.
"""
from __future__ import unicode_literals, absolute_import, print_function
import os
import time

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

spinner = Halo(text='Such Spins', spinner='dots')

try:
    spinner.start()
    time.sleep(2)
    spinner.text = 'Much Colors'
    spinner.color = 'magenta'
    time.sleep(2)
    spinner.text = 'Very emojis'
    spinner.spinner = 'hearts'
    time.sleep(2)
    spinner.stop_and_persist({'symbol': '🦄 '.encode('utf-8'), 'text': 'Wow!'})
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
