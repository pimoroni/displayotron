#!/usr/bin/env python
print("""
This example shows you how to use the Display-o-Tron 3000 Joystick as a mouse.
You'll need to be running a desktop environment to use this.
If you move the joystick, your mouse cursor should move.

Press CTRL+C to exit.
""")

import dot3k.joystick as j
import signal
import uinput

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


@j.on(j.UP)
def handle_up(pin):
    device.emit(uinput.REL_Y, -1)
    j.repeat(j.UP, lambda: device.emit(uinput.REL_Y, -1), delay, ramp)


@j.on(j.DOWN)
def handle_down(pin):
    device.emit(uinput.REL_Y, 1)
    j.repeat(j.DOWN, lambda: device.emit(uinput.REL_Y, 1), delay, ramp)


@j.on(j.LEFT)
def handle_left(pin):
    device.emit(uinput.REL_X, -1)
    j.repeat(j.LEFT, lambda: device.emit(uinput.REL_X, -1), delay, ramp)


@j.on(j.RIGHT)
def handle_right(pin):
    device.emit(uinput.REL_X, 1)
    j.repeat(j.RIGHT, lambda: device.emit(uinput.REL_X, 1), delay, ramp)


@j.on(j.BUTTON, 100)
def handle_button(pin):
    device.emit_click(uinput.BTN_LEFT)


# Prevent the script exiting!
signal.pause()
