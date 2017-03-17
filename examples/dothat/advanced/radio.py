#!/usr/bin/env python

import sys
import time

import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from dot3k.menu import Menu

# Add the root examples dir so Python can find the plugins
sys.path.append('../../')

from plugins.clock import Clock
from plugins.graph import GraphCPU, GraphTemp
from plugins.radio import Radio
from plugins.volume import Volume
from plugins.utils import Backlight, Contrast


print("""
This advanced example uses the menu framework.
Providing you have VLC and extra dependencies installed, it should function as an internet radio!

Press CTRL+C to exit.
""")

nav.enable_repeat(True)

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
        'Clock': clock,
        'Radio Stream': Radio(),
        'Volume': Volume(backlight),
        'Status': {
            'CPU': GraphCPU(),
            'Temp': GraphTemp()
        },
        'Settings': {
            'Contrast': Contrast(lcd),
            'Backlight': Backlight(backlight)
        }
    },
    lcd,  # Draw to dot3k.lcd
    clock,  # Idle with the clock plugin,
    10  # Idle after 10 seconds
)

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.touch
"""


@nav.on(nav.UP)
def handle_up(ch, evt):
    menu.up()


@nav.on(nav.CANCEL)
def handle_cancel(ch, evt):
    menu.cancel()


@nav.on(nav.DOWN)
def handle_down(ch, evt):
    menu.down()


@nav.on(nav.LEFT)
def handle_left(ch, evt):
    menu.left()


@nav.on(nav.RIGHT)
def handle_right(ch, evt):
    menu.right()


@nav.on(nav.BUTTON)
def handle_button(ch, evt):
    menu.select()


while 1:
    # Redraw the menu, since we don't want to hand this off to a thread
    menu.redraw()
    time.sleep(0.05)
