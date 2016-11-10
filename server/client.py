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

import select
from threading import Thread
import random
from multiprocessing import Queue
import hashlib
from Crypto.Cipher import AES

from glob import *
from encoder import Encoder


def parse(msg,val):
  return msg[msg.find(val+b'[')+len(val)+1:].split(b']')[0]

def auth(c):
  msg = c.conn.recv(SIZE)
  if msg[:4] == b'HELO':
    c.nick = parse(msg,b'USER').decode('utf-8') # To check (found it ? is it valid ?)
    salt = bytes([random.randint(0,255) for i in range(16)])
    print("Salt",salt)
    c.conn.send(b'SALT:'+salt)
    return salt
  else:
    print("Incorrect auth:",msg)
    c.conn.send(b'NOPE')
    c.disconnect()

class Client_thread(Thread):
  def __init__(self, conn, addr):
    Thread.__init__(self)
    self.ip = addr[0]
    self.conn = conn
    self.port = addr[1]
    self.nick = ""
    self.loop = True
    self.c2s = Queue()
    self.s2c = Queue()
    self.finished = False

  def is_talking(self):
    try:
      return len(select.select([self.conn],[],[],0.05)[0]) > 0
    except:
      self.disconnect()

  def receive(self):
    try:
      return self.conn.recv(SIZE)
    except:
      self.disconnect()

  def run(self):
    self.encoder = Encoder(auth(self))
    while self.loop:
      while not self.s2c.empty():
        action,args = self.s2c.get()
        if action == SAY_ALL:

          #self.conn.send(args[0]+b':'+args[1])
          self.conn.send(self.encoder.encrypt(args[1]+args[0]))

      if self.is_talking():
        try:
          msg = self.encoder.decrypt(self.conn.recv(SIZE))
        except:
          self.disconnect()
        if msg == b'':
          self.disconnect()
          return
        if msg[0] != 33:
          self.c2s.put((SAY_ALL,[msg]))
        else:
          print("Special command from",self.nick,":",msg.decode('utf-8'))
    self.finished = True

  def disconnect(self,reason = "Server error"):
    print(self.nick+" disconnected")
    try:
      self.conn.send(b'EXT')
    except:
      pass
    self.conn.close()
    self.loop = False
