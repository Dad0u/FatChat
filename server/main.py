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

import socket
import select

from client import Client

print("Starting FatChat server version {}...".format(VERSION))

conn = socket.socket()
conn.bind(('',DEFAULT_PORT))
conn.listen(3)
client = []

def auth(c):
  msg = c.conn.recv(SIZE)
  if msg == b'YOLO':
    c.conn.send(b'POUET')
  else:
    print("Incorrect auth:",msg)
    c.conn.send(b'NOPE')
    client.remove(c)

while True:
  new_conn = select.select([conn],[],[],0.05)[0]
  for c in new_conn:
    client.append(Client(*c.accept()))
    print("New client connected from "+client[-1].ip+", authentication...")
    auth(client[-1])

  
print("FatChat server terminating, bye!")
