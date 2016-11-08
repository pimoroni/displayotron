#!/usr/bin/env python

import signal
from sys import exit

try:
    import uinput
except ImportError:
    exit("This script requires the uinput module\nInstall with: sudo pip install uinput")

import dot3k.joystick as nav


print("""
This example shows you how to use the Display-o-Tron 3000 Joystick as a mouse.
You'll need to be running a desktop environment to use this.
If you move the joystick, your mouse cursor should move.

Press CTRL+C to exit.
""")

"""
The joystick provides the @joystick.on() decorator
to make it super easy to attach handlers to each button.
"""

device = uinput.Device([
    uinput.BTN_LEFT,
    uinput.REL_X,
    uinput.REL_Y
])

delay = 0.1
ramp = 0.5


@nav.on(nav.UP)
def handle_up(pin):
    device.emit(uinput.REL_Y, -1)
    nav.repeat(nav.UP, lambda: device.emit(uinput.REL_Y, -1), delay, ramp)


@nav.on(nav.DOWN)
def handle_down(pin):
    device.emit(uinput.REL_Y, 1)
    nav.repeat(nav.DOWN, lambda: device.emit(uinput.REL_Y, 1), delay, ramp)


@nav.on(nav.LEFT)
def handle_left(pin):
    device.emit(uinput.REL_X, -1)
    nav.repeat(nav.LEFT, lambda: device.emit(uinput.REL_X, -1), delay, ramp)


@nav.on(nav.RIGHT)
def handle_right(pin):
    device.emit(uinput.REL_X, 1)
    nav.repeat(nav.RIGHT, lambda: device.emit(uinput.REL_X, 1), delay, ramp)


@nav.on(nav.BUTTON, 100)
def handle_button(pin):
    device.emit_click(uinput.BTN_LEFT)


# Prevent the script exiting!
signal.pause()
