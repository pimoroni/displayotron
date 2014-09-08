#!/usr/bin/env python

import dot3k.joystick as j
import dot3k.lcd as l
import dot3k.backlight as b
import signal, time

hue = 0

@j.on(j.UP)
def handle_up(pin):
  print("Up pressed!")
  l.clear()
  l.set_cursor_position(0,0)
  l.write("Up up and away!")

@j.on(j.DOWN)
def handle_down(pin):
  print("Down pressed!")
  l.clear()
  l.set_cursor_position(0,0)
  l.write("Down down doobie down!")

@j.on(j.LEFT)
def handle_left(pin):
  global hue
  print("Left pressed!")
  l.clear()
  l.set_cursor_position(0,0)
  l.write("Leftie left left!")
  hue-=0.01

@j.on(j.RIGHT)
def handle_right(pin):
  global hue
  print("Right pressed!")
  l.clear()
  l.set_cursor_position(0,0)
  l.write("Rightie tighty!")
  hue+=0.01

@j.on(j.BUTTON)
def handle_button(pin):
  print("Button pressed!")
  l.clear()
  l.set_cursor_position(0,0)
  l.write("Ouch!")

while 1:
  b.hue(hue)
  time.sleep(0.1)

# Prevent the script exiting!
signal.pause()
