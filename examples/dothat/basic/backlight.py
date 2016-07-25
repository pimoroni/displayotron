#!/usr/bin/env python

import math
import time

import dothat.backlight as backlight
import dothat.lcd as lcd


print("""
This example shows you a feature of the Dot HAT backlight.
You should see a rainbow sweep across the whole display!

Press CTRL+C to exit.
""")

lcd.set_cursor_position(0, 1)
lcd.write(" Such Rainbow! ")

x = 0

while True:
    x += 1

    backlight.sweep((x % 360) / 360.0)
    backlight.set_graph(abs(math.sin(x / 100.0)))
    time.sleep(0.01)
