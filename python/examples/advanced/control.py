#!/usr/bin/env python
"""
Control!

This example builds upon the others and incorporates idle plugins,
remote control support, and more.

If you've got a Rii keyboard, plug it in and give this a whirl!
"""

import dot3k.lcd as lcd
import dot3k.backlight as backlight
import dot3k.joystick as joystick
import utils.usbkeyboard as keyboard
from dot3k.menu import Menu, MenuOption
from plugins.text import Text
from plugins.deluge import Deluge
from plugins import Volume, Backlight, Contrast, GraphTemp, GraphCPU, Clock, Radio, Stocks
import time

my_clock = Clock()

menu = Menu(structure={
    'Deluge':Deluge(),
    'Clock':my_clock,
    'Stocks':Stocks(),
    'Radio':Radio(),
    'Status': {
      'CPU':GraphCPU(),
      'Temp':GraphTemp()
    },
    'Settings': {
      'Volume':Volume(),
      'Contrast':Contrast(lcd),
      'Backlight':Backlight(backlight)
    }
  },
  lcd=lcd,
  idle_handler=my_clock,
  idle_time=3,
  input_handler=Text())

"""
usbkeyboard provides the same methods as dot3k.joystick
so it's a drop-in replacement!
"""
@keyboard.on(keyboard.UP)
def handle_up(pin):
  menu.up()
@keyboard.on(keyboard.DOWN)
def handle_down(pin):
  menu.down()
@keyboard.on(keyboard.LEFT)
def handle_left(pin):
  menu.left()
@keyboard.on(keyboard.RIGHT)
def handle_right(pin):
  menu.right()
@keyboard.on(keyboard.BUTTON)
def handle_button(pin):
  menu.button()

REPEAT_DELAY = 0.5
REPEAT_DATE = 0.99
@joystick.on(joystick.UP)
def handle_up(pin):
  menu.up()
  joystick.repeat(joystick.UP,menu.up,REPEAT_DELAY,0.99)

@joystick.on(joystick.DOWN)
def handle_down(pin):
  menu.down()
  joystick.repeat(joystick.DOWN,menu.down,REPEAT_DELAY,0.99)

@joystick.on(joystick.LEFT)
def handle_left(pin):
  menu.left()
  joystick.repeat(joystick.LEFT,menu.left,REPEAT_DELAY,0.99)

@joystick.on(joystick.RIGHT)
def handle_right(pin):
  menu.right()
  joystick.repeat(joystick.RIGHT,menu.right,REPEAT_DELAY,0.99)

@joystick.on(joystick.BUTTON)
def handle_button(pin):
  menu.select()

while 1:
  menu.redraw()
  time.sleep(0.05)
