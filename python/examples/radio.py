#!/usr/bin/env python

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu, Backlight, Contrast, MenuOption
import time
import plugins

"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.
"""
menu = Menu({
    'Radio Stream':plugins.Radio(),
    'Volume':plugins.Volume(),
    'Settings': {
      'Display': {
        'Contrast':Contrast(),
        'Backlight':Backlight(backlight)
      }
    }
  },
  lcd)

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.joystick
"""
@joystick.on(joystick.UP)
def handle_up(pin):
  menu.up()
  joystick.repeat(joystick.UP,menu.up,0.4,0.9)

@joystick.on(joystick.DOWN)
def handle_down(pin):
  menu.down()
  joystick.repeat(joystick.DOWN,menu.down,0.4,0.9)

@joystick.on(joystick.LEFT)
def handle_left(pin):
  menu.left()
  joystick.repeat(joystick.LEFT,menu.left,0.4,0.9)

@joystick.on(joystick.RIGHT)
def handle_right(pin):
  menu.right()
  joystick.repeat(joystick.RIGHT,menu.right,0.4,0.9)

@joystick.on(joystick.BUTTON)
def handle_button(pin):
  menu.select()

while 1:
  menu.redraw()
  time.sleep(0.05)
