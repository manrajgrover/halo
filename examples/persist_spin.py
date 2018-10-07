# -*- coding: utf-8 -*-
"""Example for persisting spinner
"""
from __future__ import unicode_literals
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

success_message = 'Loading success'
failed_message = 'Loading failed'
unicorn_message = 'Loading unicorn'

spinner = Halo(text=success_message, spinner='dots')

try:
    spinner.start()
    time.sleep(1)
    spinner.succeed()
    spinner.start(failed_message)
    time.sleep(1)
    spinner.fail()
    spinner.start(unicorn_message)
    time.sleep(1)
    spinner.stop_and_persist(symbol='🦄'.encode('utf-8'), text=unicorn_message)
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
