#!/usr/bin/env python

import sys
import time

import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from dot3k.menu import Menu, MenuOption

# Add the root examples dir so Python can find the plugins
sys.path.append('../../')

from plugins.clock import Clock
from plugins.graph import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from plugins.text import Text
from plugins.utils import Backlight, Contrast
from plugins.wlan import Wlan

print("""
This advanced example uses the menu framework.
It gives you a basic menu setup with plugins. You should be able
to view system info and adjust settings!

Press CTRL+C to exit.
""")


class BacklightIdleTimeout(MenuOption):
    def __init__(self, backlight):
        self.backlight = backlight
        self.r = 255
        self.g = 255
        self.b = 255
        MenuOption.__init__(self)

    def setup(self, config):
        self.config = config

        self.r = int(self.get_option('Backlight', 'r', 255))
        self.g = int(self.get_option('Backlight', 'g', 255))
        self.b = int(self.get_option('Backlight', 'b', 255))

    def cleanup(self):
        print("Idle timeout expired. Turning on backlight!")
        self.backlight.rgb(self.r, self.g, self.b)

    def begin(self):
        print("Idle timeout triggered. Turning off backlight!")
        self.backlight.rgb(0, 0, 0)


"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""

backlight_idle = BacklightIdleTimeout(backlight)

menu = Menu(
    structure={
        'WiFi': Wlan(),
        'Clock': Clock(backlight),
        'Status': {
            'IP': IPAddress(),
            'CPU': GraphCPU(backlight),
            'Temp': GraphTemp()
        },
        'Settings': {
            'Display': {
                'Contrast': Contrast(lcd),
                'Backlight': Backlight(backlight)
            }
        }
    },
    lcd=lcd,
    idle_handler=backlight_idle,
    idle_time=5,
    input_handler=Text())

# Pass the configuration into the idle handler,
# since the menu class does not do this!
backlight_idle.setup(menu.config)
"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.touch
"""
nav.bind_defaults(menu)

while 1:
    menu.redraw()
    time.sleep(0.05)
