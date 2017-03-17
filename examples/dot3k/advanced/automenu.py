#!/usr/bin/env python

import sys
import time

import dot3k.backlight as backlight
import dot3k.joystick as nav
import dot3k.lcd as lcd
from dot3k.menu import Menu, MenuOption

# Add the root examples dir so Python can find the plugins
sys.path.append('../../')

from plugins.clock import Clock
from plugins.graph import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from plugins.wlan import Wlan


print("""
This example uses automation to advance through each menu item.
You should see each menu item appear in turn. However use-input will not be accepted.

Press CTRL+C to exit.
""")

menu = Menu({
        'Clock': Clock(),
        'IP': IPAddress(),
        'CPU': GraphCPU(),
        'Temp': GraphTemp()
    },
    lcd,
    None,
    30)


def millis():
    return int(round(time.time() * 1000.0))


def advance():
    global last
    if millis() > last + (delay * 1000.0):
        menu.cancel()
        menu.down()
        menu.right()
        last = millis()


last = millis()
delay = 2  # In seconds

while 1:
    advance()
    menu.redraw()
    time.sleep(0.05)
