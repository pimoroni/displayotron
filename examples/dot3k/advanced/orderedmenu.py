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
from plugins.utils import Backlight, Contrast


print("""
This advanced example uses the menu framework.
It gives you an example of a menu created with a specific order.

Press CTRL+C to exit.
""")

class SpaceInvader(MenuOption):
    """
    A silly example "plug-in" showing an
    animated space invader.
    """

    def __init__(self):
        self.start = self.millis()
        self.invader = [
            [14, 31, 21, 31, 9, 18, 9, 18],
            [14, 31, 21, 31, 18, 9, 18, 9]
        ]
        MenuOption.__init__(self)

    def redraw(self, menu):
        now = self.millis()

        x = int((self.start - now) / 200 % 16)
        menu.lcd.create_char(0, self.invader[int((self.start - now) / 400 % 2)])

        menu.write_row(0, 'Space Invader!')
        menu.write_row(1, (' ' * x) + chr(0))
        menu.clear_row(2)


my_invader = SpaceInvader()

menu = Menu(
    None,
    lcd,
    my_invader,
    5)

"""
If you want menu items to appear in a defined order, you must
add them one at a time using 'add_item'. This method accepts
a plugin instance, plus the path where you want it to appear.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""

menu.add_item('Space Invader', my_invader)
menu.add_item('Clock', Clock())
menu.add_item('Status/IP', IPAddress())
menu.add_item('Status/Test', '')
menu.add_item('Status/CPU', GraphCPU())
menu.add_item('Status/Arrr', 'Blah blah')
menu.add_item('Status/Temp', GraphTemp())
menu.add_item('Settings/Display/Contrast', Contrast(lcd)),
menu.add_item('Settings/Display/Backlight', Backlight(backlight))

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.joystick
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
    menu.redraw()
    time.sleep(0.05)
