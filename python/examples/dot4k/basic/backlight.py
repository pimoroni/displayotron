#!/usr/bin/env python

import dot3k.hatbacklight as backlight
import dot3k.lcd as lcd
import time
import math


lcd.set_cursor_position(0,1)
lcd.write(" Such Rainbow! ")

x = 0

while True:
    x+=1
   
    backlight.sweep( (x%360)/360.0)
    backlight.set_graph(abs(math.sin(x/100.0)))
    time.sleep(0.01)
