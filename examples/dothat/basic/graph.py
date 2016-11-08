#!/usr/bin/env python

import time

import dothat.backlight as backlight
import dothat.lcd as lcd


print("""
This example shows you how to take individual control of the bar graph LEDs.
You should see the bar graph LEDs count up in binary!

Press CTRL+C to exit.
""")

'''
Each LED can be either on/off,
and brightness is controlled globally using:

* graph_set_led_duty(min, max)

When you don't need a bar graph, these LEDs could display
remaining lives in a game, the status of different processes,
the hour of the day in binary or anything else you might need!
'''

lcd.set_cursor_position(0, 1)
lcd.write("   So Graph!    ")

# Reset the LED states and polarity
backlight.graph_off()

# Dim the LEDs by setting the max duty to 1
backlight.graph_set_led_duty(0, 1)

# Now run a binary counter on the LEDs
while True:
    for x in range(64):
        for led in range(6):
            backlight.graph_set_led_state(led, x & (1 << led))
        time.sleep(0.1)
