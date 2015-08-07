#!/usr/bin/env python

# Include advanced so Python can find the plugins
import sys
sys.path.append("../../")

import dothat.touch as touch
import dothat.lcd as lcd
import dothat.backlight as backlight
from dot3k.menu import Menu, MenuOption
from plugins.utils import Backlight, Contrast
from plugins.graph import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from plugins.clock import Clock
from plugins.wlan import Wlan
import time

class SpaceInvader(MenuOption):
  """
  A silly example "plug-in" showing an
  animated space invader.
  """

  def __init__(self):
    self.start = self.millis()
    self.invader = [
      [14,31,21,31,9,18,9,18],
      [14,31,21,31,18,9,18,9]
    ]
    MenuOption.__init__(self)

  def redraw(self, menu):
    now = self.millis()

    x = int((self.start-now)/200 % 16)
    menu.lcd.create_char(0, self.invader[int((self.start-now)/400 % 2)])

    menu.write_row(0,'Space Invader!')
    menu.write_row(1,(' '*x) + chr(0))
    menu.clear_row(2)

"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""
my_invader = SpaceInvader()

menu = Menu({
    'Space Invader':my_invader,
    'Clock':Clock(backlight),
    'Status': {
      'IP':IPAddress(),
      'CPU':GraphCPU(backlight),
      'Temp':GraphTemp()
    },
    'Settings': {
      'Display': {
        'Contrast':Contrast(lcd),
        'Backlight':Backlight(backlight)
      }
    }
  },
  lcd,
  my_invader,
  30)

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.captouch
"""
touch.bind_defaults(menu)

while 1:
  menu.redraw()
  time.sleep(0.05)
