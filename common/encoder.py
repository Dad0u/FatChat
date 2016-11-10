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

from Crypto.Cipher import AES
import hashlib 

from glob import *

class Encoder():
  """
  Class to generate the encrypted data ready to be sent
  from the unicode messages
  """
  def __init__(self,salt):
    h = hashlib.sha256()
    h.update(KEY+salt)
    self.cipher_encrypt = AES.AESCipher(h.digest(),AES.MODE_CBC,salt)
    self.cipher_decrypt = AES.AESCipher(h.digest(),AES.MODE_CBC,salt)

  def encrypt(self,message):
    if type(message) is str:
      message = message.encode()
    if len(message) == 0 or len(message) >= 2**16 - 32:
      print("Tried to encode a string of",len(message),"bytes!")
      return
    out = bytes([len(message)//256,len(message)%256])
    if len(message) % 32 != 0:
      message += b'\x00'*(32-len(message)%32)
    out += self.cipher_encrypt.encrypt(message)
    return out

  def decrypt(self,ciphertext):
    l = 256*ciphertext[0]+ciphertext[1]
    s = self.cipher_decrypt.decrypt(ciphertext[2:])
    return s[:l].decode()
