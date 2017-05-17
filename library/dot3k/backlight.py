import colorsys
import math
from sys import exit

try:
    import sn3218
except ImportError:
    exit("This library requires the sn3218 module\nInstall with: sudo pip install sn3218")


LED_R_R = 0x00
LED_R_G = 0x01
LED_R_B = 0x02

LED_M_R = 0x03
LED_M_G = 0x04
LED_M_B = 0x05

LED_L_R = 0x06
LED_L_G = 0x07
LED_L_B = 0x08

leds = [0x00] * 18


def use_rbg():
    """Swap the Green and Blue channels on the LED backlight

    Use if you have a first batch Display-o-Tron 3K

    """

    global LED_R_G, LED_R_B
    global LED_M_G, LED_M_B
    global LED_L_G, LED_L_B

    (LED_R_G, LED_R_B) = (LED_R_B, LED_R_G)
    (LED_M_G, LED_M_B) = (LED_M_B, LED_M_G)
    (LED_L_G, LED_L_B) = (LED_L_B, LED_L_G)


def set_graph(value):
    """Light a number of bargraph LEDs depending upon value

    :param hue: hue value between 0.0 and 1.0

    """

    value *= 9

    if value > 9:
        value = 9

    for i in range(9):
        leds[9 + i] = 0

    lit = int(math.floor(value))
    for i in range(lit):
        leds[9 + i] = 255

        partial = lit
        if partial < 9:
            leds[9 + partial] = int((value % 1) * 255)

    update()


def set(index, value):
    """Set a specific LED to a value

    :param index (int): index of the LED from 0 to 18
    :param value (int): brightness value from 0 to 255

    """

    leds[index] = value
    update()


def set_bar(index, value):
    """Set a value or values to one or more LEDs

    :param index: starting index
    :param value: a single int, or list of brightness values from 0 to 255

    """

    if isinstance(value, int):
        set(LED_R_R + 9 + (index % 9), value)
    if isinstance(value, list):
        for i, v in enumerate(value):
            set(LED_R_R + 9 + ((index + i) % 9), v)
    update()


def hue_to_rgb(hue):
    """Convert a hue to RGB brightness values

    :param hue: hue value between 0.0 and 1.0

    """

    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    return [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]


def hue(hue):
    """Set the backlight LEDs to supplied hue

    :param hue: hue value between 0.0 and 1.0

    """

    col_rgb = hue_to_rgb(hue)
    rgb(col_rgb[0], col_rgb[1], col_rgb[2])


def sweep(hue, range=0.08):
    """Set the backlight LEDs to a gradient centered on supplied hue

    Supplying zero to range would be the same as hue()

    :param hue: hue value between 0.0 and 1.0
    :param range: range value to deviate the left and right hue

    """

    left_hue((hue - range) % 1)
    mid_hue(hue)
    right_hue((hue + range) % 1)


def left_hue(hue):
    """Set the left backlight to supplied hue

    :param hue: hue value between 0.0 and 1.0

    """

    col_rgb = hue_to_rgb(hue)
    left_rgb(col_rgb[0], col_rgb[1], col_rgb[2])
    update()


def mid_hue(hue):
    """Set the middle backlight to supplied hue

    :param hue: hue value between 0.0 and 1.0

    """

    col_rgb = hue_to_rgb(hue)
    mid_rgb(col_rgb[0], col_rgb[1], col_rgb[2])
    update()


def right_hue(hue):
    """Set the right backlight to supplied hue

    :param hue: hue value between 0.0 and 1.0

    """

    col_rgb = hue_to_rgb(hue)
    right_rgb(col_rgb[0], col_rgb[1], col_rgb[2])
    update()


def left_rgb(r, g, b):
    """Set the left backlight to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    set(LED_L_R, r)
    set(LED_L_B, b)
    set(LED_L_G, g)
    update()


def mid_rgb(r, g, b):
    """Set the middle backlight to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    set(LED_M_R, r)
    set(LED_M_B, b)
    set(LED_M_G, g)
    update()


def right_rgb(r, g, b):
    """Set the right backlight to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    set(LED_R_R, r)
    set(LED_R_B, b)
    set(LED_R_G, g)
    update()


def rgb(r, g, b):
    """Set all backlights to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    left_rgb(r, g, b)
    mid_rgb(r, g, b)
    right_rgb(r, g, b)


def off():
    """Turn off the backlight."""

    rgb(0, 0, 0)


def update():
    """Update backlight with changes to the LED buffer"""

    sn3218.output(leds)


# set gamma correction for backlight to normalise brightness
g_channel_gamma = [int(value / 1.6) for value in sn3218.default_gamma_table]
sn3218.channel_gamma(1, g_channel_gamma)
sn3218.channel_gamma(4, g_channel_gamma)
sn3218.channel_gamma(7, g_channel_gamma)

r_channel_gamma = [int(value / 1.4) for value in sn3218.default_gamma_table]
sn3218.channel_gamma(0, r_channel_gamma)
sn3218.channel_gamma(3, r_channel_gamma)
sn3218.channel_gamma(6, r_channel_gamma)

w_channel_gamma = [int(value / 24) for value in sn3218.default_gamma_table]
for i in range(9, 18):
    sn3218.channel_gamma(i, w_channel_gamma)

sn3218.enable()
