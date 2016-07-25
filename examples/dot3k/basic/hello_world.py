#!/usr/bin/env python

import dot3k.lcd as lcd


print("""
This example shows a basic "Hello World" on the LCD.
You should see "Hello World" displayed on your LCD!

Press CTRL+C to exit.
""")


# Clear the LCD and display Hello World
lcd.clear()
lcd.write("Hello World")
