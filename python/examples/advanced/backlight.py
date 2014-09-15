#!/usr/bin/env python

import dot3k, time
from threading import Thread

pirate = [
        [0x00,0x1f,0x0b,0x03,0x00,0x04,0x11,0x1f],
        [0x00,0x1f,0x16,0x06,0x00,0x08,0x03,0x1e],
        [0x00,0x1f,0x0b,0x03,0x00,0x04,0x11,0x1f],
        [0x00,0x1f,0x05,0x01,0x00,0x02,0x08,0x07]
]

def get_anim_frame(anim, fps):
  return anim[ int(round(time.time()*fps) % len(anim)) ]

dot3k.lcd.set_cursor_position(1,0)
dot3k.lcd.write('Display-o-tron')
dot3k.lcd.write('      ' + chr(0) + '3000  ')
dot3k.lcd.create_char(0,get_anim_frame(pirate,4))



while 1:
  dot3k.backlight.rgb(255,0,0)
  time.sleep(1)
  dot3k.backlight.rgb(0,255,0)
  time.sleep(1)
  dot3k.backlight.rgb(0,0,255)
  time.sleep(1)
  dot3k.backlight.rgb(255,255,255)
  time.sleep(1)
  for i in range(0,360):
    dot3k.backlight.hue(i/360.0)
    time.sleep(0.01)
  for i in range(0,360):
    dot3k.backlight.sweep(i/360.0)
    time.sleep(0.01)
