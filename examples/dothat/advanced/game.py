#!/usr/bin/env python

import sys
import signal

import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from dot3k.menu import Menu

# Add the root examples dir so Python can find the plugins
sys.path.append('../../')

from plugins.debris import Debris
from plugins.utils import Backlight, Contrast


print("""
This advanced example uses the menu framework.
It loads the debris game plugin. Your score is time survived in seconds, see how well you can do!

Press CTRL+C to exit.
""")

# Build your menu!
menu = Menu({
        'Debris Game': Debris(backlight),
        'Settings': {
            'Display': {
                'Contrast': Contrast(lcd),
                'Backlight': Backlight(backlight)
            }
        }
    },
    lcd)

# Hook captouch into menu with default settings
nav.bind_defaults(menu)

# Start the menu redraw loop
menu.run()

signal.pause()
