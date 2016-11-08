#!/usr/bin/env python

import time

import dot3k.backlight as backlight
import dot3k.lcd as lcd


print("""
This example shows you a feature of the Dot HAT backlight.
You should see the backlight go white, then multi-coloured.

Press CTRL+C to exit.
""")

# Clear the LCD and display Hello World
lcd.clear()
lcd.write("Hello World")

# Set all the backlights to white
backlight.rgb(255, 255, 255)

time.sleep(1)

# Set the backlights independently
backlight.left_rgb(255, 0, 0)
backlight.mid_rgb(255, 0, 255)
backlight.right_rgb(0, 0, 255)

time.sleep(1)
