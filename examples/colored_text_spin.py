# -*- coding: utf-8 -*-
"""Example for doge spinner ;)
"""
from __future__ import unicode_literals
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

spinner = Halo(text='Such Spins', text_color= 'cyan', color='green', spinner='dots')

try:
    spinner.start()
    time.sleep(2)
    spinner.text = 'Much Colors'
    spinner.color = 'magenta'
    spinner.text_color = 'green'
    time.sleep(2)
    spinner.text = 'Very emojis'
    spinner.spinner = 'hearts'
    spinner.text_color = 'magenta'
    time.sleep(2)
    spinner.stop_and_persist(symbol='🦄 '.encode('utf-8'), text='Wow!')
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
