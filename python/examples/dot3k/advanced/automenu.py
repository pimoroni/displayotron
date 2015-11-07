#!/usr/bin/env python
print("""
This example uses automation to advance through each menu item.
You should see each menu item appear in turn. However use-input will not be accepted.

Press CTRL+C to exit.
""")

import sys

sys.path.append('../../')

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu, MenuOption
from plugins.graph import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from plugins.clock import Clock
from plugins.wlan import Wlan
import time

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
