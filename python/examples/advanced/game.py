#!/usr/bin/env python

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu
from plugins.utils import Backlight, Contrast
from plugins.debris import Debris
import time

menu = Menu({
    'Debris Game':Debris(),
    'Settings': {
      'Display': {
        'Contrast':Contrast(lcd),
        'Backlight':Backlight(backlight)
      }
    }
  },
  lcd)

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
  menu.redraw()
  time.sleep(0.05)
