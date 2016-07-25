#!/usr/bin/env python

import time

import dot3k.backlight as backlight
import dot3k.lcd as lcd


print("""
This example shows a range of different backlight techniques for Display-o-Tron.
You should see the backlight go Red, Green, Blue, White and then Rainbow!

Press CTRL+C to exit.
""")

pirate = [
    [0x00, 0x1f, 0x0b, 0x03, 0x00, 0x04, 0x11, 0x1f],
    [0x00, 0x1f, 0x16, 0x06, 0x00, 0x08, 0x03, 0x1e],
    [0x00, 0x1f, 0x0b, 0x03, 0x00, 0x04, 0x11, 0x1f],
    [0x00, 0x1f, 0x05, 0x01, 0x00, 0x02, 0x08, 0x07]
]


def get_anim_frame(anim, fps):
    return anim[int(round(time.time() * fps) % len(anim))]


lcd.set_cursor_position(1, 0)
lcd.write('Display-o-tron')
lcd.write('      ' + chr(0) + '3000  ')
lcd.create_char(0, get_anim_frame(pirate, 4))

while 1:
    backlight.rgb(255, 0, 0)
    time.sleep(1)
    backlight.rgb(0, 255, 0)
    time.sleep(1)
    backlight.rgb(0, 0, 255)
    time.sleep(1)
    backlight.rgb(255, 255, 255)
    time.sleep(1)
    for i in range(0, 360):
        backlight.hue(i / 360.0)
        time.sleep(0.01)
    for i in range(0, 360):
        backlight.sweep(i / 360.0)
        time.sleep(0.01)
