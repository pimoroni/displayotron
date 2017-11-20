#!/usr/bin/env python

from multiprocessing import Process
import threading

print("""
This example shows you a feature of the Dot HAT.
You should see the Temperature of your Raspberry Pi!

Press CTRL+C to exit.
""")

def temp():
    print 'Starting Temp'
    from dothat import backlight
    from dothat import lcd
    import time

    lcd.set_contrast(50)

    while True:
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
        lcd.write("Temp: " + tempF + " C")
        time.sleep(1)
        lcd.clear()

    print 'backlight: finishing'

def graph():
    print 'Starting Graph'

    from dothat import backlight
    import time
    import math

    x = 0
    while True:

        x += 1
        backlight.set_graph(abs(math.sin(x / 100.0)))
        time.sleep(0.01)

    print 'graph: finishing'


if __name__ == '__main__':

    p1 = Process(target=temp)
    p1.start()
    p2 = Process(target=graph)
    p2.start()
    p1.join()
    p2.join()


""" 
Multithreading:    
==============

p1 = threading.Thread(name='background', target=temp)
p2 = threading.Thread(name='background', target=graph)

p1.start()
p2.start()

Another way of doing parallel:
=============================

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

runInParallel(func1, func2)
"""
