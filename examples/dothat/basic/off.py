#!/usr/bin/env python

import dothat.backlight as backlight
import dothat.lcd as lcd

"""
This example clear the screen and turn off all LED from the Display-o-Tron HAT.
"""

# Reset the LED states and polarity
backlight.graph_off()

# Empty the screen
lcd.clear()

# Turn off the backlight
backlight.rgb(0, 0, 0)

