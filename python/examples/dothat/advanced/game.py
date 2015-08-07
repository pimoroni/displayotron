#!/usr/bin/env python

# Add the root examples dir so Python can find the plugins
import sys
sys.path.append("../../")

# Import the dot3k libraries
import dothat.lcd as lcd
from dot3k.menu import Menu

# Use "captouch" for dot4k
import dothat.touch as touch

# Use "hatbacklight" for dot4k
import dothat.backlight as backlight

# Import some plugins
from plugins.utils import Backlight, Contrast
from plugins.debris import Debris

import signal

# Build your menu!
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

# Hook captouch into menu with default settings
touch.bind_defaults(menu)

# Start the menu redraw loop
menu.run()

signal.pause()
