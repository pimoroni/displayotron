#!/usr/bin/env python
'''
This example uses automation to advance through each
menu item in Dot3k.

It doesn't accept any user input.
'''
import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu, MenuOption
from plugins.graph import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from plugins.clock import Clock
from plugins.wlan import Wlan
import time

menu = Menu({
    'Clock':Clock(),
    'IP':IPAddress(),
    'CPU':GraphCPU(),
    'Temp':GraphTemp()
  },
  lcd,
  None,
  30)

def millis():
  return int(round(time.time()*1000.0))

last = millis()
delay = 2 # In seconds

def advance():
  global last
  if millis() > last + (delay*1000.0):
    menu.cancel()
    menu.down()
    menu.right()
    last = millis()

while 1:
  advance()
  menu.redraw()
  time.sleep(0.05)
