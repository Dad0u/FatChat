#!/usr/bin/python3
#coding: utf-8
"""
Program by Victor Couty (victor@couty.eu)
2016
"""

from glob import *
import sys

if sys.version_info.major != 3:
  print("Please use Python3 to run this program")
  sys.exit(-1)

import select

class Client():
  def __init__(self, conn, addr):
    self.ip = addr[0]
    self.conn = conn
    self.port = addr[1]
    self.nick = ""

  def isTalking(self):
    try:
      return len(select.select([self.conn],[],[],0)[0]) > 0
    except:
      self.disconnect()

  def disconnect(self):
    print("Deconnexion de "+self.nick)
    try:
      self.conn.send(b'EXT')
    except:
      pass
    self.conn.close()
