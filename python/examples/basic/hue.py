#!/usr/bin/env python
import colorsys
import dot3k.backlight as bl

hue = 0

while True:
	r,g,b = colorsys.hsv_to_rgb(hue/360.0,1.0,1.0)
	r,g,b = int(r*255.0), int(g*255.0), int(b*255.0)
	bl.rgb(r,b,g)
	hue += 1
	hue %= 360
