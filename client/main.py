#!/usr/bin/python3
#coding: utf-8
"""
Program by Victor Couty (victor@couty.eu)
2016
"""

import sys

if sys.version_info.major != 3:
  print("Please use Python3 to run this program")
  sys.exit(-1)

from glob import *
from interface import Main_window

mw = Main_window()
mw.run()

print("Closing FatChat client...")
