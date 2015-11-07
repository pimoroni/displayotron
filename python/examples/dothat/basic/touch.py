#!/usr/bin/env python
print("""
This example shows the Display-o-Tron HAT touch inputs in action.
Touch an input and you should see the LCD change accordingly.

Press CTRL+C to exit.
""")

import dothat.touch as j
import dothat.lcd as l
import dothat.backlight as b
import signal

"""
Captouch provides the @captouch.on() decorator
to make it super easy to attach handlers to each button.

It's also a drop-in replacement for joystick, with one exception: 
it has a "cancel" method.

The handler will receive "channel" ( corresponding to a particular
button ID ) and "event" ( corresponding to press/release ) arguments.
"""


@j.on(j.UP)
def handle_up(ch, evt):
    print("Up pressed!")
    l.clear()
    b.rgb(255, 0, 0)
    l.write("Up up and away!")


@j.on(j.DOWN)
def handle_down(ch, evt):
    print("Down pressed!")
    l.clear()
    b.rgb(0, 255, 0)
    l.write("Down down doobie down!")


@j.on(j.LEFT)
def handle_left(ch, evt):
    print("Left pressed!")
    l.clear()
    b.rgb(0, 0, 255)
    l.write("Leftie left left!")


@j.on(j.RIGHT)
def handle_right(ch, evt):
    print("Right pressed!")
    l.clear()
    b.rgb(0, 255, 255)
    l.write("Rightie tighty!")


@j.on(j.BUTTON)
def handle_button(ch, evt):
    print("Button pressed!")
    l.clear()
    b.rgb(255, 255, 255)
    l.write("Ouch!")


@j.on(j.CANCEL)
def handle_cancel(ch, evt):
    print("Cancel pressed!")
    l.clear()
    b.rgb(0, 0, 0)
    l.write("Boom!")


# Prevent the script exiting!
signal.pause()
