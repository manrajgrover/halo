"""Examples for halo.
"""
from __future__ import unicode_literals, absolute_import, print_function
import os
import time

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from halo.halo import Halo

spinner = Halo('Loading')

spinner.start()
time.sleep(10)
spinner.stop()
