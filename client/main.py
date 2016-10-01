#!/usr/bin/python3
#coding: utf-8
"""
Program by Victor Couty (victor@couty.eu)
2016
"""

import sys

from glob import *
from interface import Main_window

if sys.version_info.major != 3:
  print("Please use Python3 to run this program")
  sys.exit(-1)

mw = Main_window()
mw.run()

print("Closing FatChat client...")
