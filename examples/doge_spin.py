# -*- coding: utf-8 -*-
"""Example for doge spinner ;)
"""
from __future__ import unicode_literals
import os
import sys
import time

# Import logger module
import logging

# Store the logging on 'logfile.log' or display on the console
# The formatter codes range the level of alert and time of occurrence of log message
file_formatter = logging.Formatter('%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s')
console_formatter = logging.Formatter('%(levelname)s -- %(message)s')

# The handler class determines where to log messages.
file_handler = logging.FileHandler("logfile.log")
file_handler.setLevel(logging.WARN)
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)

# Methods to interact with the logging system through class of instances
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importing the Halo class
from halo import Halo

# Halo Spin words and display emojis
spinner = Halo(text='Such Spins', spinner='dots')

# If one or more emojis don't display correctly, 
# logger both displays issue on console and log on "logfile.log"
try:
    logger.info("Start spinning process")
    spinner.start()
    time.sleep(2) 
    spinner.text = 'Much Colors'
    spinner.color = 'magenta'
    time.sleep(2)
    spinner.cu = 'Very emojis'
    print()
    logger.critical(" 'Very emojis' did not work! ")
    spinner.spinner = 'hearts'
    time.sleep(2)
    spinner.stop_and_persist(symbol='🦄'.encode('utf-8'), text='Wow!')
except (KeyboardInterrupt, SystemExit):
    spinner.stop()
    

