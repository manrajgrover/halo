# -*- coding: utf-8 -*-
"""Example for changing stream
"""
from __future__ import unicode_literals, absolute_import, print_function
import os
import time
import random

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

import sys

spinner = Halo(stream=sys.stderr)

spinner.start()
spinner.stop()

print("Testing")
