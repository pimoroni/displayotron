#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This example clear the screen and turn
    off all LED from the Display-o-Tron HAT """

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import dothat.backlight as backlight
import dothat.lcd as lcd

# Reset the LED states and polarity
backlight.graph_off()

# Empty the screen
lcd.clear()

# Turn off the backlight
backlight.rgb(0, 0, 0)
