import colorsys
from sys import exit

try:
    from sn3218 import SN3218
except ImportError:
    try:
        import sn3218
    except ImportError:
        exit("This library requires the sn3218 module\nInstall with: sudo pip install sn3218")
else:
    sn3218 = SN3218()

try:
    import cap1xxx
except ImportError:
    exit("This library requires the cap1xxx module\nInstall with: sudo pip install cap1xxx")


cap = cap1xxx.Cap1166(i2c_addr=0x2C, skip_init=True)

NUM_LEDS = 6
STEP_VALUE = 16

leds = [0x00] * 18  # B G R, B G R, B G R, B G R, B G R, B G R

# set gamma correction for backlight to normalise brightness
g_channel_gamma = [int(value / 1.6) for value in sn3218.default_gamma_table]
r_channel_gamma = [int(value / 1.4) for value in sn3218.default_gamma_table]

for x in range(0, 18, 3):
    sn3218.channel_gamma(x + 1, g_channel_gamma)
    sn3218.channel_gamma(x + 2, r_channel_gamma)

sn3218.enable()

graph_set_led_state = cap.set_led_state
graph_set_led_polarity = cap.set_led_polarity
graph_set_led_duty = cap.set_led_direct_duty


def use_rbg():
    """Does nothing.

    Implemented for library compatibility with Dot3k backlight.

    """
    pass


def graph_off():
    cap._write_byte(cap1xxx.R_LED_POLARITY, 0b00000000)
    cap._write_byte(cap1xxx.R_LED_OUTPUT_CON, 0b00000000)


def set_graph(percentage):
    """Light a number of bargraph LEDs depending upon value

    :param hue: hue value between 0.0 and 1.0

    """

    cap._write_byte(cap1xxx.R_LED_DIRECT_RAMP, 0b00000000)
    cap._write_byte(cap1xxx.R_LED_BEHAVIOUR_1, 0b00000000)
    cap._write_byte(cap1xxx.R_LED_BEHAVIOUR_2, 0b00000000)

    # The Cap 1xxx chips do *not* have full per-LED PWM
    # brightness control. However...
    # They have the ability to define what on/off actually
    # means, plus invert the state of any LED.

    total_value = STEP_VALUE * NUM_LEDS
    actual_value = int(total_value * percentage)
    set_polarity = 0b00000000
    set_state = 0b00000000
    set_duty = 0  # Value from 0 to 15
    for x in range(NUM_LEDS):
        if actual_value >= STEP_VALUE:
            set_polarity |= 1 << (NUM_LEDS - 1 - x)
        if 0 < actual_value < STEP_VALUE:
            set_state |= 1 << (NUM_LEDS - 1 - x)
            set_duty = actual_value << 4
        actual_value -= STEP_VALUE
    cap._write_byte(cap1xxx.R_LED_DIRECT_DUT, set_duty)
    cap._write_byte(cap1xxx.R_LED_POLARITY, set_polarity)
    cap._write_byte(cap1xxx.R_LED_OUTPUT_CON, set_state)


def set(index, value):
    """Set a specific backlight LED to a value

    :param index (int): index of the LED from 0 to 17
    :param value (int): brightness value from 0 to 255

    """

    index = index if isinstance(index, list) else [index]
    for i in index:
        leds[i] = value
    update()


def set_bar(index, value):
    """Does nothing.

    Implemented for library compatibility with Dot3k backlight.

    """
    pass


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


def sweep(hue, sweep_range=0.0833):
    """Set the backlight LEDs to a gradient centered on supplied hue

    Supplying zero to range would be the same as hue()

    :param hue: hue value between 0.0 and 1.0
    :param range: range value to deviate the left and right hue

    """

    global leds
    for x in range(0, 18, 3):
        rgb = hue_to_rgb((hue + (sweep_range * (x / 3))) % 1)
        rgb.reverse()
        leds[x:x + 3] = rgb
    update()


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

    single_rgb(0, r, g, b, False)
    single_rgb(1, r, g, b, False)
    update()


def mid_rgb(r, g, b):
    """Set the middle backlight to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    single_rgb(2, r, g, b, False)
    single_rgb(3, r, g, b, False)
    update()


def right_rgb(r, g, b):
    """Set the right backlight to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    single_rgb(4, r, g, b, False)
    single_rgb(5, r, g, b, False)
    update()


def single_rgb(led, r, g, b, auto_update=True):
    """A single backlight LED to the supplied r, g, b colour

    The `auto_update` parameter will trigger a write to the LEDs
    after the r, g, b colour has been set. Omit it and manually
    call `update()` to batch multiple LED changes into one update.

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255
    :param auto_update: autmatically update the LEDs

    """

    global leds
    leds[(led * 3)] = b
    leds[(led * 3) + 1] = g
    leds[(led * 3) + 2] = r
    if auto_update:
        update()


def rgb(r, g, b):
    """Set all backlights to supplied r, g, b colour

    :param r: red value between 0 and 255
    :param g: green value between 0 and 255
    :param b: blue value between 0 and 255

    """

    global leds
    leds = [b, g, r] * 6
    update()


def off():
    """Turn off the backlight."""

    rgb(0, 0, 0)


def update():
    """Update backlight with changes to the LED buffer"""

    sn3218.output(leds)
