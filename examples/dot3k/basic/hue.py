#!/usr/bin/env python
print("""
This example shows how to set the backlight to a hue!
It uses coloursys, rather than the built-in hue function, to show you a colour conversion in Python.

Press CTRL+C to exit.
""")

import colorsys
import dot3k.backlight as bl

hue = 0

while True:
    r, g, b = [int(x * 255.0) for x in colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)]
    bl.rgb(r, b, g)
    hue += 1
    hue %= 360
