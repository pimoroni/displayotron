#!/usr/bin/env python

import sys
import time

import dot3k.backlight as backlight
import dot3k.joystick as nav
import dot3k.lcd as lcd
from dot3k.menu import Menu

# Add the root examples dir so Python can find the plugins
sys.path.append('../../')

from plugins.clock import Clock
from plugins.graph import GraphCPU, GraphTemp
from plugins.radio import Radio
from plugins.utils import Backlight, Contrast
from plugins.volume import Volume


print("""
This advanced example uses the menu framework.
Providing you have VLC and extra dependencies installed, it should function as an internet radio!

Press CTRL+C to exit.
""")

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
            'CPU': GraphCPU(backlight),
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
but you'll probably want to use dot3k.joystick

Repeat delay determines how quickly holding the joystick
in a direction will start to trigger repeats
"""
REPEAT_DELAY = 0.5


@nav.on(nav.UP)
def handle_up(pin):
    menu.up()
    nav.repeat(nav.UP, menu.up, REPEAT_DELAY, 0.9)


@nav.on(nav.DOWN)
def handle_down(pin):
    menu.down()
    nav.repeat(nav.DOWN, menu.down, REPEAT_DELAY, 0.9)


@nav.on(nav.LEFT)
def handle_left(pin):
    menu.left()
    nav.repeat(nav.LEFT, menu.left, REPEAT_DELAY, 0.9)


@nav.on(nav.RIGHT)
def handle_right(pin):
    menu.right()
    nav.repeat(nav.RIGHT, menu.right, REPEAT_DELAY, 0.9)


@nav.on(nav.BUTTON)
def handle_button(pin):
    menu.select()


while 1:
    # Redraw the menu, since we don't want to hand this off to a thread
    menu.redraw()
    time.sleep(0.05)
