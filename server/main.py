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

import socket
import select

from glob import *
from client import Client_thread
from consoleInput import Console_input

print("Starting FatChat server version {}...".format(VERSION))

conn = socket.socket()
conn.bind(('',DEFAULT_PORT))
conn.listen(3)
client_list = []
loop = True

ci = Console_input()
ci.start()
while loop:
  #Listening and acepting new clients
  new_conn = select.select([conn],[],[],0.05)[0]
  for c in new_conn:
    new_client = Client_thread(*c.accept())
    new_client.start()
    client_list.append(new_client)

  #Executing server console commands
  cmd = ci.get_cmd()
  if len(cmd) != 0:
    #print("Command(s):",cmd)
    for c in cmd:
      if c.lower()[:4] == 'stop':
        ci.stop()
        loop = False


  #Executing actions from clients
  for client in client_list:
    while not client.c2s.empty():
      action,args = client.c2s.get()
      if action == SAY_ALL:
        for cl in client_list:
          cl.s2c.put((SAY_ALL,[client.nick,args[0]]))

  #Removing ended client threads
  i = 0
  while i < len(client_list):
    if client_list[i].finished:
      del client_list[i]
    i+=1

print("Server shutting down!")
ci.join()
for cl in client_list:
  cl.disconnect()
  cl.join()
print("FatChat server closed properly, bye!")
