#!/usr/bin/env python

import copy
import datetime
import math
import time
from sys import exit

try:
    import psutil
except ImportError:
    exit("This library requires the psutil module\nInstall with: sudo pip install psutil")

import dot3k.backlight as backlight
import dot3k.lcd as lcd


print("""
This example shows you how to create animations on Display-o-Tron!
You should see a collection of animated icons on your display.

Press CTRL+C to exit.
""")

lcd.write(chr(0) + 'Ooo! Such time' + chr(0))
lcd.set_cursor_position(0, 2)
lcd.write(chr(1) + chr(4) + ' Very Wow! ' + chr(3) + chr(2) + chr(5))

pirate = [
    [0x00, 0x1f, 0x0b, 0x03, 0x00, 0x04, 0x11, 0x1f],
    [0x00, 0x1f, 0x16, 0x06, 0x00, 0x08, 0x03, 0x1e],
    [0x00, 0x1f, 0x0b, 0x03, 0x00, 0x04, 0x11, 0x1f],
    [0x00, 0x1f, 0x05, 0x01, 0x00, 0x02, 0x08, 0x07]
]

heart = [
    [0x00, 0x0a, 0x1f, 0x1f, 0x1f, 0x0e, 0x04, 0x00],
    [0x00, 0x00, 0x0a, 0x0e, 0x0e, 0x04, 0x00, 0x00],
    [0x00, 0x00, 0x00, 0x0e, 0x04, 0x00, 0x00, 0x00],
    [0x00, 0x00, 0x0a, 0x0e, 0x0e, 0x04, 0x00, 0x00]
]

raa = [
    [0x1f, 0x1d, 0x19, 0x13, 0x17, 0x1d, 0x19, 0x1f],
    [0x1f, 0x17, 0x1d, 0x19, 0x13, 0x17, 0x1d, 0x1f],
    [0x1f, 0x13, 0x17, 0x1d, 0x19, 0x13, 0x17, 0x1f],
    [0x1f, 0x19, 0x13, 0x17, 0x1d, 0x19, 0x13, 0x1f]
]

arr = [
    [31, 14, 4, 0, 0, 0, 0, 0],
    [0, 31, 14, 4, 0, 0, 0, 0],
    [0, 0, 31, 14, 4, 0, 0, 0],
    [0, 0, 0, 31, 14, 4, 0, 0],
    [0, 0, 0, 0, 31, 14, 4, 0],
    [0, 0, 0, 0, 0, 31, 14, 4],
    [4, 0, 0, 0, 0, 0, 31, 14],
    [14, 4, 0, 0, 0, 0, 0, 31]
]

char = [
    [12, 11, 9, 9, 25, 25, 3, 3],
    [0, 15, 9, 9, 9, 25, 27, 3],
    [3, 13, 9, 9, 9, 27, 27, 0],
    [0, 15, 9, 9, 9, 25, 27, 3]
]

pacman = [
    [0x0e, 0x1f, 0x1d, 0x1f, 0x18, 0x1f, 0x1f, 0x0e],
    [0x0e, 0x1d, 0x1e, 0x1c, 0x18, 0x1c, 0x1e, 0x0f]
]


def getAnimFrame(char, fps):
    return char[int(round(time.time() * fps) % len(char))]


cpu_sample_count = 200
cpu_samples = [0] * cpu_sample_count
hue = 0.0
while True:
    hue += 0.008
    backlight.sweep(hue)

    cpu_samples.append(psutil.cpu_percent() / 100.0)
    cpu_samples.pop(0)

    cpu_avg = sum(cpu_samples) / cpu_sample_count
    backlight.set_graph(cpu_avg)

    if hue > 1.0:
        hue = 0.0

    lcd.create_char(0, getAnimFrame(char, 4))
    lcd.create_char(1, getAnimFrame(arr, 16))
    lcd.create_char(2, getAnimFrame(raa, 8))
    lcd.create_char(3, getAnimFrame(pirate, 2))
    lcd.create_char(4, getAnimFrame(heart, 4))
    lcd.create_char(5, getAnimFrame(pacman, 3))
    lcd.set_cursor_position(0, 1)
    t = datetime.datetime.now().strftime("%H:%M:%S.%f")
    lcd.write(t)

    time.sleep(0.005)
