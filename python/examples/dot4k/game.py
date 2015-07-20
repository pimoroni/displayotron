#!/usr/bin/env python

# Include advanced so Python can find the plugins
import sys
sys.path.append("../advanced/")

import dot3k.captouch as captouch
import dot3k.lcd as lcd
import dot3k.hatbacklight as backlight
from dot3k.menu import Menu
from plugins.utils import Backlight, Contrast
from plugins.debris import Debris
import time

menu = Menu({
    'Debris Game':Debris(backlight),
    'Settings': {
      'Display': {
        'Contrast':Contrast(lcd),
        'Backlight':Backlight(backlight)
      }
    }
  },
  lcd)

REPEAT_DELAY = 0.5
@captouch.on(captouch.UP)
def handle_up(ch,evt):
  menu.up()

@captouch.on(captouch.DOWN)
def handle_down(ch,evt):
  menu.down()

@captouch.on(captouch.LEFT)
def handle_left(ch,evt):
  menu.left()

@captouch.on(captouch.RIGHT)
def handle_right(ch,evt):
  menu.right()

@captouch.on(captouch.BUTTON)
def handle_button(ch,evt):
  menu.select()

@captouch.on(captouch.CANCEL)
def handle_cancel(ch,evt):
  menu.cancel()

while 1:
  menu.redraw()
  time.sleep(0.05)
