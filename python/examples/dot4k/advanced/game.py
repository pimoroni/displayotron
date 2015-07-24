#!/usr/bin/env python

# Add the root examples dir so Python can find the plugins
import sys
sys.path.append("../../")

# Import the dot3k libraries
import dot3k.lcd as lcd
from dot3k.menu import Menu

# Use "captouch" for dot4k
import dot3k.captouch as captouch

# Use "hatbacklight" for dot4k
import dot3k.hatbacklight as backlight

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
captouch.bind_defaults(menu)

# Start the menu redraw loop
menu.run()

signal.pause()
