#!/usr/bin/env python

import dot3k.joystick as j
import dot3k.lcd as l
import dot3k.backlight as b
import signal

"""
The joystick provides the @joystick.on() decorator
to make it super easy to attach handlers to each button.
"""

@j.on(j.UP)
def handle_up(pin):
  print("Up pressed!")
  l.clear()
  b.rgb(255,0,0)
  l.write("Up up and away!")

@j.on(j.DOWN)
def handle_down(pin):
  print("Down pressed!")
  l.clear()
  b.rgb(0,255,0)
  l.write("Down down doobie down!")

@j.on(j.LEFT)
def handle_left(pin):
  print("Left pressed!")
  l.clear()
  b.rgb(0,0,255)
  l.write("Leftie left left!")

@j.on(j.RIGHT)
def handle_right(pin):
  print("Right pressed!")
  l.clear()
  b.rgb(0,255,255)
  l.write("Rightie tighty!")

@j.on(j.BUTTON)
def handle_button(pin):
  print("Button pressed!")
  l.clear()
  b.rgb(255,255,255)
  l.write("Ouch!")

# Prevent the script exiting!
signal.pause()
