#!/usr/bin/env python

import signal

import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav


print("""
This example shows the Display-o-Tron HAT touch inputs in action.
Touch an input and you should see the LCD change accordingly.

Press CTRL+C to exit.
""")

"""
Captouch provides the @captouch.on() decorator
to make it super easy to attach handlers to each button.

It's also a drop-in replacement for joystick, with one exception: 
it has a "cancel" method.

The handler will receive "channel" ( corresponding to a particular
button ID ) and "event" ( corresponding to press/release ) arguments.
"""


@nav.on(nav.UP)
def handle_up(ch, evt):
    print("Up pressed!")
    lcd.clear()
    backlight.rgb(255, 0, 0)
    lcd.write("Up up and away!")


@nav.on(nav.DOWN)
def handle_down(ch, evt):
    print("Down pressed!")
    lcd.clear()
    backlight.rgb(0, 255, 0)
    lcd.write("Down down doobie down!")


@nav.on(nav.LEFT)
def handle_left(ch, evt):
    print("Left pressed!")
    lcd.clear()
    backlight.rgb(0, 0, 255)
    lcd.write("Leftie left left!")


@nav.on(nav.RIGHT)
def handle_right(ch, evt):
    print("Right pressed!")
    lcd.clear()
    backlight.rgb(0, 255, 255)
    lcd.write("Rightie tighty!")


@nav.on(nav.BUTTON)
def handle_button(ch, evt):
    print("Button pressed!")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.write("Ouch!")


@nav.on(nav.CANCEL)
def handle_cancel(ch, evt):
    print("Cancel pressed!")
    lcd.clear()
    backlight.rgb(0, 0, 0)
    lcd.write("Boom!")


# Prevent the script exiting!
signal.pause()
