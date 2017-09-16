#!/usr/bin/env python

from dothat import lcd
from dothat import backlight
import time

lcd.set_contrast(50)

while True:
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    
    # Change backlight if temp changes
    if tempC < 60:
        backlight.rgb(0,255,0)
        backlight.set_graph(0.4)
    elif tempC > 70:
        backlight.rgb(255,0,0)
        backlight.set_graph(0.8)
    else:
        backlight.rgb(0,255,255)
        backlight.set_graph(0.6)

    # Convert Temp to String
    tempF = str(tempC)

    # Write Temp and wait 1 sec.
    lcd.set_cursor_position(0, 0)
    lcd.write("Temp: " +  tempF + " C")
    time.sleep(1)
    lcd.clear()
