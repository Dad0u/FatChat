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

def auth(conn):
  conn.send(b"YOLO")
  replying = select.select([conn],[],[],5)[0]
  if len(replying) == 0:
      return NO_REPLY
  else:
      reply = replying[0].recv(SIZE)
  if reply != b"POUET":
      print("Incorrect reply from the server: "+reply.decode())
      return INCORRECT_REPLY
  return SUCCESS

class Network_handler:
  def __init__(self,sprint):
    self.clear_conn()
    self.sprint = sprint

  def clear_conn(self):
    self.conn = None
    self.address = None
    self.port = None

  def connect(self,address,port):
    if self.conn is not None:
      self.sprint("Disconnecting from "+self.address+":"+str(self.port),
                                     "Info",ORANGE)
      self.conn.close()
    self.sprint("Connecting to "+address)
    #self.conn = socket.socket(socket.AF_INET,socket.sock_STREAM)
    self.conn = socket.socket()
    try:
      self.conn.connect((address,port))
    except (OSError,socket.gaierror) as e:
      self.sprint("Could not connect: "+str(e),"Error",RED)
      self.clear_conn()
      return
      
    auth_code = auth(self.conn)
    if auth_code == SUCCESS:
      self.address = address
      self.port = port
      self.sprint("Connected!","Info",ORANGE)
    else:
      self.conn.close()
      self.clear_conn()
      self.sprint("Could not connect: "+ERR[auth_code],"Error",RED)


    
