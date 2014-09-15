#!/usr/bin/env python

import dot3k.lcd as lcd
import dot3k.backlight as backlight
import time

# Clear the LCD and display Hello World
lcd.clear()
lcd.write("Hello World")

# Set all the backlights to white
backlight.rgb(255,255,255)

# Set the backlights independently
backlight.left_rgb(255,0,0)
backlight.mid_rgb(255,0,255)
backlight.right_rgb(0,0,255)
