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
from threading import Thread
from multiprocessing import Queue

from glob import *
from encoder import Encoder

def parse(msg,val):
  return msg[msg.find(val+b'[')+len(val)+1:].split(b']')[0]

class Fetcher(Thread):
  def __init__(self,nh):
    Thread.__init__(self)
    self.loop = True
    self.nh = nh

  def run(self):
    self.nh.sprint("Starting Fetcher!")
    while self.loop:
      print("Fetcher loop!")
      waiting = select.select([self.nh.conn],[],[],0.1)[0]
      if len(waiting) == 0:
        continue
      msg = self.nh.conn.recv(SIZE)
      if len(msg) == 0:
        print("Fetcher disonnected!")
        self.loop = False

#      self.nh.sprint(msg.decode('utf-8'))
      self.nh.sprint(self.nh.encoder.decrypt(msg))
    self.nh.sprint("Fetcher ending!")
    self.nh.disconnect()

  def stop(self):
    self.loop = False

class Network_handler:
  def __init__(self,sprint):
    self.clear_conn()
    self.sprint = sprint

  def clear_conn(self):
    self.conn = None
    self.address = None
    self.port = None
    self.connected = False

  def connect(self,address,port):
    if self.connected:
      self.sprint("Disconnecting from "+self.address+":"+str(self.port),
                                     "Warning",ORANGE)
      self.disconnect()
    self.sprint("Connecting to "+address)
    #self.conn = socket.socket(socket.AF_INET,socket.sock_STREAM)
    self.conn = socket.socket()
    try:
      self.conn.connect((address,port))
    except (OSError,socket.gaierror) as e:
      self.sprint("Could not connect: "+str(e),"Error",RED)
      self.clear_conn()
      return
      
    auth_code = self.auth()
    if auth_code == SUCCESS:
      self.address = address
      self.port = port
      self.connected = True
      self.sprint("Connected!","Info",GREEN)
      self.fetcher = Fetcher(self)
      self.fetcher.start()
    else:
      self.conn.close()
      self.clear_conn()
      self.sprint("Could not connect: "+ERR[auth_code],"Error",RED)

  def auth(self):
    sollicitation = b'HELO '+bytes("Fatchat client V["+VERSION,"utf-8")+\
    b"] USER["+bytes(USER,'utf-8')+b']'
    self.conn.send(sollicitation)
    try:
      replying = select.select([self.conn],[],[],5)[0]
    except ConnectionResetError as e:
      return CONN_RESET
      
    if len(replying) == 0:
        return NO_REPLY
    else:
      try:
        reply = replying[0].recv(SIZE)
      except ConnectionResetError as e:
        return CONN_RESET
    if reply[:5] != b'SALT:':
      print("Incorrect reply from the server: "+reply.decode())
      return INCORRECT_REPLY
    salt = reply[5:]
    self.encoder = Encoder(salt)
    return SUCCESS

  def send(self,msg):
    if self.connected:
      msg = self.encoder.encrypt(msg)
      try:
        self.conn.send(msg) # <--- To be a bit more complex...
      except:
        self.sprint("Error while sending message, disconnecting!")
        self.disconnect()
    else:
      self.sprint("Not connected!","Warning",ORANGE)

  def disconnect(self):
    if not self.connected:
      self.sprint("Not connected","Warning",ORANGE)
      return
    #self.send(b"DISC")
    if self.fetcher.loop == True:
      self.fetcher.stop()
    self.fetcher.join()
    self.conn.close()
    self.clear_conn()
    self.sprint("Disconnected!","Info",GREEN)


  
