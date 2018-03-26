# -*- coding: utf-8 -*-
"""Example for changing stream
"""
from __future__ import unicode_literals, absolute_import
import os
import time

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo import Halo

import sys

spinner = Halo(stream=sys.stderr)

spinner.start()
time.sleep(1)
spinner.stop()
