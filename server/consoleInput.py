#!/usr/bin/python3
#coding: utf-8
"""
Program by Victor Couty (victor@couty.eu)
2016
"""

from threading import Thread
from time import sleep

class Console_input(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.loop = True
    self.q = []

  def run(self):
    while self.loop:
      cmd = input()
      self.q.append(cmd)
      sleep(.5)

  def get_cmd(self):
    r = self.q
    self.q = []
    return r

  def stop(self):
    self.loop = False


