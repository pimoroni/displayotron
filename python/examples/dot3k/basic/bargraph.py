#!/usr/bin/env python

import dot3k.lcd as lcd
import dot3k.backlight as backlight
import time

# Clear the LCD and display Hello World
lcd.clear()
lcd.write("Hello World")

# Turn off the backlight
backlight.rgb(0,0,0)

"""
set_graph accepts a float between 0.0 and 1.0
and lights up the LEDs accordingly
"""
for i in range(100):
    backlight.set_graph(i/100.0)
    time.sleep(0.05)

"""
set_bar will set a specific bargraph LED to
a brightness between 0 and 255
"""
for i in range(256):
    backlight.set_bar(0,[255-i]*9)
    time.sleep(0.01)

backlight.set_graph(0)
