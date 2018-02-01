#!/usr/bin/env python
segone = [
    0b11111,
    0b11111,
    0b11111,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
]
segtwo = [
    0b11111,
    0b11111,
    0b11111,
    0b00111,
    0b00111,
    0b00111,
    0b00111,
    0b00111,
]
segthree = [
    0b11111,
    0b11111,
    0b11111,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
]
segfour = [
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
    0b11100,
]
segfive = [
    0b00111,
    0b00111,
    0b00111,
    0b00111,
    0b00111,
    0b00111,
    0b00111,
    0b00111,
]
segsix = [
    0b00111,
    0b00111,
    0b00111,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
]
segdot = [
    0b00000,
    0b00000,
    0b01110,
    0b01110,
    0b01110,
    0b00000,
    0b00000,
    0b00000,
]

number = {
    0: [3, 2, 4, 5, 1, 1],
    1: [0, 5, 0, 5, 0, 6],
    2: [1, 2, 3, 1, 1, 1],
    3: [1, 2, 1, 2, 1, 1],
    4: [4, 5, 1, 2, 0, 6],
    5: [3, 1, 1, 2, 1, 1],
    6: [3, 1, 3, 2, 1, 1],
    7: [1, 2, 0, 5, 0, 6],
    8: [3, 2, 3, 2, 1, 1],
    9: [3, 2, 1, 2, 1, 1],
    'dot': [7, 7, 0],
    'empty': [0, 0, 0],
}

# setup character
from dot3k import lcd, backlight
from datetime import datetime
import time

backlight.rgb(61, 255, 129)
lcd.set_contrast(45)
lcd.set_display_mode(True, False, False)
lcd.create_char(0, [0, 0, 0, 0, 0, 0, 0, 0])
lcd.create_char(1, segone)
lcd.create_char(2, segtwo)
lcd.create_char(3, segthree)
lcd.create_char(4, segfour)
lcd.create_char(5, segfive)
lcd.create_char(6, segsix)
lcd.create_char(7, segdot)


lcd.clear()
running = True
tick = False
while running:
    now = datetime.now()
    second = 'dot' if tick else 'empty'
    tick = not tick
    chars = [now.hour / 10, now.hour % 10, second, now.minute / 10, now.minute % 10]
    pos = 0
    for char in chars:
        char = number[char]
        width = len(char) / 3
        for index, num in enumerate(char):
            lcd.set_cursor_position(index % width + pos, index / width)
            lcd.write(chr(num))
        pos += width + 1
    time.sleep(0.5)
