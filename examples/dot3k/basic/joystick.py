#!/usr/bin/env python

import signal

import dot3k.backlight as backlight
import dot3k.joystick as nav
import dot3k.lcd as lcd


print("""
This example shows you how to use the Display-o-Tron 3000 Joystick.
If you press a joystick direction, you should see the LCD change accordingly.

Press CTRL+C to exit.
""")

"""
The joystick provides the @joystick.on() decorator
to make it super easy to attach handlers to each button.
"""


@nav.on(nav.UP)
def handle_up(pin):
    print("Up pressed!")
    lcd.clear()
    backlight.rgb(255, 0, 0)
    lcd.write("Up up and away!")


@nav.on(nav.DOWN)
def handle_down(pin):
    print("Down pressed!")
    lcd.clear()
    backlight.rgb(0, 255, 0)
    lcd.write("Down down doobie down!")


@nav.on(nav.LEFT)
def handle_left(pin):
    print("Left pressed!")
    lcd.clear()
    backlight.rgb(0, 0, 255)
    lcd.write("Leftie left left!")


@nav.on(nav.RIGHT)
def handle_right(pin):
    print("Right pressed!")
    lcd.clear()
    backlight.rgb(0, 255, 255)
    lcd.write("Rightie tighty!")


@nav.on(nav.BUTTON)
def handle_button(pin):
    print("Button pressed!")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.write("Ouch!")


# Prevent the script exiting!
signal.pause()
