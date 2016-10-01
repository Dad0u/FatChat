#!/usr/bin/python3
#coding: utf-8
"""
Program by Victor Couty (victor@couty.eu)
2016
"""


import tkinter as tk

from glob import *

class Main_window():
  def __init__(self):
    # Creating and configuring the window
    self.win = tk.Tk()
    self.win.grid_rowconfigure(0, weight=1)
    self.win.grid_columnconfigure(0, weight=1)
    self.win.title('FatChat client v'+VERSION)
    # To close properly when clicking the X
    self.win.protocol("WM_DELETE_WINDOW", self.close)
    self.out_text = tk.Text(self.win,wrap=tk.WORD)
    self.out_text.grid(row=0,column=0,columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S)
    self.out_text.configure(state='disabled')
    self.scrollbar = tk.Scrollbar(self.win)
    self.scrollbar.grid(row=0,column=2, sticky = tk.E+tk.N+tk.S)
    self.out_text.config(yscrollcommand=self.scrollbar.set)
    self.scrollbar.config(command=self.out_text.yview)
    self.in_text = tk.Entry(self.win)
    self.in_text.grid(row=1,column=0,sticky=tk.W+tk.E)
    self.in_text.bind('<Return>',self.send)
    self.send_button = tk.Button(command = self.send,text="Send")
    self.send_button.grid(row=1,column=1,columnspan=2, sticky=tk.SE)
    # Setting the properties for the tags (to add color)
    for color in COLORS:
      self.out_text.tag_config(color,foreground=color)

  def run(self):
    self.win.mainloop()

  def send(self, event = ''):
    s = self.in_text.get().encode('utf-8')
    self.in_text.delete(0,tk.END)

  def write(self, msg, header=None, color=BLACK):
    self.out_text.configure(state='normal')
    if header is not None:
      self.out_text.insert(tk.END,header+": ",color)
    self.out_text.insert(tk.END,msg+"\n")
    self.out_text.configure(state='disabled')
    self.out_text.see(tk.END)

  def close(self):
    self.win.destroy()
