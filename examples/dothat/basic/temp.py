#!/usr/bin/env python

from dothat import lcd
from dothat import backlight
import time
import math

lcd.set_contrast(50)
x = 0

while True:
    x += 1
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    
    # Change backlight if temp changes
    if tempC < 60:
        backlight.rgb(0,255,0)
    elif tempC > 70:
        backlight.rgb(255,0,0)
    else:
        backlight.rgb(0,255,255)

    # Convert Temp to String
    tempF = str(tempC)

    # Write Temp and wait 1 sec.
    lcd.set_cursor_position(0, 0)
    lcd.write("Temp: " +  tempF + " C")
    backlight.set_graph(abs(math.sin(x / 100.0)))
    time.sleep(1)
    lcd.clear()
