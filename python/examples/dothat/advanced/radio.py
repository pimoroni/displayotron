#!/usr/bin/env python

# Include advanced so Python can find the plugins
import sys
sys.path.append("../../")

import dothat.touch as touch
import dothat.lcd as lcd
import dothat.backlight as backlight
from dot3k.menu import Menu
from plugins.utils import Backlight, Contrast
from plugins.volume import Volume
from plugins.clock import Clock
from plugins.radio import Radio
from plugins.graph import GraphCPU, GraphTemp
import time

touch.enable_repeat(True)

# We want to use clock both as an option
# and as the idle plugin
clock = Clock(backlight)

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
    'Volume':Volume(backlight),
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
but you'll probably want to use dot3k.touch
"""
@touch.on(touch.UP)
def handle_up(ch,evt):
  menu.up()

@touch.on(touch.CANCEL)
def handle_cancel(ch,evt):
  menu.cancel()

@touch.on(touch.DOWN)
def handle_down(ch,evt):
  menu.down()

@touch.on(touch.LEFT)
def handle_left(ch,evt):
  menu.left()

@touch.on(touch.RIGHT)
def handle_right(ch,evt):
  menu.right()

@touch.on(touch.BUTTON)
def handle_button(ch,evt):
  menu.select()

while 1:
  # Redraw the menu, since we don't want to hand this off to a thread
  menu.redraw()
  time.sleep(0.05)
