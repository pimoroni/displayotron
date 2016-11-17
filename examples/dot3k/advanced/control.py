#!/usr/bin/env python

import sys
import time

import dot3k.lcd as lcd
import dot3k.backlight as backlight
import dot3k.joystick as nav

from menu import Menu, MenuOption

# Add the root examples dir so Python can find the plugins
sys.path.append('../../')

from plugins.deluge import Deluge
from plugins.text import Text
from plugins import Volume, Backlight, Contrast, GraphTemp, GraphCPU, Clock, Radio, Stocks
import utils.usbkeyboard as keyboard


print("""
This example builds upon the others and incorporates idle plugins,
remote control support, and more.

To use this example you need a Rii mini wireless keyboard plugged into USB!

Press CTRL+C to exit.
""")

my_clock = Clock()

menu = Menu(structure={
    'Deluge': Deluge(),
    'Clock': my_clock,
    'Stocks': Stocks(),
    'Radio': Radio(),
    'Status': {
        'CPU': GraphCPU(),
        'Temp': GraphTemp()
    },
    'Settings': {
        'Volume': Volume(),
        'Contrast': Contrast(lcd),
        'Backlight': Backlight(backlight)
    }
},
    lcd=lcd,
    idle_handler=my_clock,
    idle_time=3,
    input_handler=Text())

"""
usbkeyboard provides the same methods as joystick
so it's a drop-in replacement!
"""


@keyboard.on(keyboard.UP)
def handle_up(pin):
    menu.up()


@keyboard.on(keyboard.DOWN)
def handle_down(pin):
    menu.down()


@keyboard.on(keyboard.LEFT)
def handle_left(pin):
    menu.left()


@keyboard.on(keyboard.RIGHT)
def handle_right(pin):
    menu.right()


@keyboard.on(keyboard.BUTTON)
def handle_button(pin):
    menu.button()


REPEAT_DELAY = 0.5
REPEAT_DATE = 0.99


@nav.on(nav.UP)
def handle_up(pin):
    menu.up()
    nav.repeat(nav.UP, menu.up, REPEAT_DELAY, 0.99)


@nav.on(nav.DOWN)
def handle_down(pin):
    menu.down()
    nav.repeat(nav.DOWN, menu.down, REPEAT_DELAY, 0.99)


@nav.on(nav.LEFT)
def handle_left(pin):
    menu.left()
    nav.repeat(nav.LEFT, menu.left, REPEAT_DELAY, 0.99)


@nav.on(nav.RIGHT)
def handle_right(pin):
    menu.right()
    nav.repeat(nav.RIGHT, menu.right, REPEAT_DELAY, 0.99)


@nav.on(nav.BUTTON)
def handle_button(pin):
    menu.select()


while 1:
    menu.redraw()
    time.sleep(0.05)
