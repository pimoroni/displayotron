#!/usr/bin/env python

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu
from plugins.utils import Backlight, Contrast
from plugins.clock import Clock
from plugins import Radio, Volume, GraphCPU, GraphTemp
import time

# We want to use clock both as an option
# and as the idle plugin
clock = Clock()

"""
Using a set of nested dictionaries you can describe
the menu you want to display on dot3k.

A nested dictionary describes a submenu.
An instance of a plugin class ( derived from MenuOption ) can be used for things like settings, radio, etc
A function name will call that function.
"""
menu = Menu({
    'Clock':clock,
    'Radio Stream':Radio(),
    'Volume':Volume(),
    'Status': {
      'CPU':GraphCPU(),
      'Temp':GraphTemp()
    },
    'Settings': {
      'Contrast':Contrast(lcd),
      'Backlight':Backlight(backlight)
    }
  },
  lcd,   # Draw to dot3k.lcd
  clock, # Idle with the clock plugin,
  10     # Idle after 10 seconds
)

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.joystick

Repeat delay determines how quickly holding the joystick
in a direction will start to trigger repeats
"""
REPEAT_DELAY = 0.5

@joystick.on(joystick.UP)
def handle_up(pin):
  menu.up()
  joystick.repeat(joystick.UP,menu.up,REPEAT_DELAY,0.9)

@joystick.on(joystick.DOWN)
def handle_down(pin):
  menu.down()
  joystick.repeat(joystick.DOWN,menu.down,REPEAT_DELAY,0.9)

@joystick.on(joystick.LEFT)
def handle_left(pin):
  menu.left()
  joystick.repeat(joystick.LEFT,menu.left,REPEAT_DELAY,0.9)

@joystick.on(joystick.RIGHT)
def handle_right(pin):
  menu.right()
  joystick.repeat(joystick.RIGHT,menu.right,REPEAT_DELAY,0.9)

@joystick.on(joystick.BUTTON)
def handle_button(pin):
  menu.select()

while 1:
  # Redraw the menu, since we don't want to hand this off to a thread
  menu.redraw()
  time.sleep(0.05)
