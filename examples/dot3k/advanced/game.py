#!/usr/bin/env python

import sys
import time

import dot3k.backlight as backlight
import dot3k.joystick as nav
import dot3k.lcd as lcd
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

menu = Menu({
        'Debris Game': Debris(),
        'Settings': {
            'Display': {
                'Contrast': Contrast(lcd),
                'Backlight': Backlight(backlight)
            }
        }
    },
    lcd)

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
    menu.redraw()
    time.sleep(0.05)
