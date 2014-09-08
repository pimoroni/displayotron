#!/usr/bin/env python

import dot3k.joystick as j
import signal

@j.on(j.UP)
def handle_up(pin):
  print("Up pressed!")

@j.on(j.DOWN)
def handle_down(pin):
  print("Down pressed!")

@j.on(j.LEFT)
def handle_left(pin):
  print("Left pressed!")

@j.on(j.RIGHT)
def handle_right(pin):
  print("Right pressed!")

@j.on(j.BUTTON)
def handle_button(pin):
  print("Button pressed!")

# Prevent the script exiting!
signal.pause()
