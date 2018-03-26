# -*- coding: utf-8 -*-
"""Example for context manager
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

with Halo(text='Loading', spinner='dots'):
    # Run time consuming work here
    time.sleep(4)

with Halo(text='Loading 2', spinner='dots'):
    # Run time consuming work here
    time.sleep(4)
