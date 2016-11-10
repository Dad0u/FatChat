#!/usr/bin/python3
#coding: utf-8
"""
Program by Victor Couty (victor@couty.eu)
2016
"""

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION = str(VERSION_MAJOR)+"."+str(VERSION_MINOR)

GREEN = "green"
ORANGE = "orange"
RED = "red"
BLUE = "blue"
BLACK = "black"

COLORS = [BLACK,GREEN,ORANGE,RED,BLUE]

DEFAULT_PORT = 1148

SIZE = 1024

SUCCESS = 0
NO_REPLY = 1
INCORRECT_REPLY = 2
CONN_REFUSED = 3
TIMEOUT = 4
CONN_RESET = 5

ERR = ["SUCCESS","NO_REPLY","INCORRECT_REPLY","CONN_REFUSED","TIMEOUT","CONN_RESET"]

KEY = b'I like trains'
USER = 'Dadou'
