#!/usr/bin/env python

import math
import time

import dothat.backlight as backlight
import dothat.lcd as lcd


print("""
This example gives a basic demo of Display-o-Tron HAT's features.
It will sweep the backlight, scan the bargraph and display text on screen!

Press CTRL+C to exit.
""")

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

pacman = [
    [0x0e, 0x1f, 0x1d, 0x1f, 0x18, 0x1f, 0x1f, 0x0e],
    [0x0e, 0x1d, 0x1e, 0x1c, 0x18, 0x1c, 0x1e, 0x0f]
]

colours = [
    "\x01   much red   \x01",
    "\x01  very orange \x01",
    "\x01  many yellow \x01",
    "\x01   also green \x01",
    "\x01   such blue  \x01",
    "\x01  so indigo   \x01",
    "\x01  ahoy voilet \x01"]
lcd.set_cursor_position(0, 2)

lcd.set_cursor_position(0, 0)
lcd.write(chr(0) + " such rainbow!")


def get_anim_frame(char, fps):
    return char[int(round(time.time() * fps) % len(char))]


x = 0

text = "  pimoroni ftw  "

while True:
    x += 3
    x %= 360

    backlight.sweep((360.0 - x) / 360.0)
    backlight.set_graph(abs(math.sin(x / 100.0)))

    if x == 0:
        lcd.set_cursor_position(0, 1)
        lcd.write(" " * 16)

    pos = int(x / 20)
    lcd.set_cursor_position(0, 1)
    lcd.write(text[:pos] + "\x02")

    lcd.set_cursor_position(0, 2)
    lcd.write(colours[int(x / 52)])

    lcd.create_char(0, get_anim_frame(pirate, 2))
    lcd.create_char(1, get_anim_frame(heart, 2))
    lcd.create_char(2, get_anim_frame(pacman, 2))

    time.sleep(0.01)
