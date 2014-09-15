import sn3218, colorsys, math

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

"""
Lights a number of bargraph LEDs depending upon value

Args:
    value (float): percentage between 0.0 and 1.0
"""
def set_graph(value):
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

"""
Set a specific LED to a value

Args:
    index (int): index of the LED from 0 to 18
    value (int): brightness value from 0 to 255
"""
def set(index, value):
	leds[index] = value

"""
Set a value or values to one or more LEDs

Args:
    index (int): starting index
    value (int or list): a single int, or list of brightness values from 0 to 255
"""
def set_bar(index, value):
	if isinstance(value, int):
		set(LED_L_B + 1 + index, value)
	if isinstance(value, list):
		for i, v in enumerate(value):
				set(LED_L_B + 1 + ((index + i)%9), v)
	update()

"""
Converts a hue to RGB brightness values

Args:
    hue (float): hue value between 0.0 and 1.0
"""	
def hue_to_rgb( hue ):
	rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

	return [int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)]

"""
Sets the backlight LEDs to supplied hue

Args:
    hue (float): hue value between 0.0 and 1.0
"""
def hue( hue ):
	col_rgb = hue_to_rgb( hue )
	rgb( col_rgb[0], col_rgb[1], col_rgb[2] )

"""
Sets the backlight LEDs to a gradient centered on supplied hue

Supplying zero to range would be the same as hue()

Args:
    hue (float): hue value between 0.0 and 1.0
    range (float): range value to deviate the left and right hue
"""
def sweep( hue, range = 0.08 ):
	left_hue( (hue-range) % 1 )
	mid_hue( hue )
	right_hue( (hue+range) % 1 )


"""
Set the left backlight to supplied hue

Args:
    hue (float): hue value between 0.0 and 1.0
"""
def left_hue( hue ):
	col_rgb = hue_to_rgb( hue )
	left_rgb( col_rgb[0], col_rgb[1], col_rgb[2] )
	update()

"""
Set the middle backlight to supplied hue

Args:
    hue (float): hue value between 0.0 and 1.0
"""
def mid_hue( hue ):
	col_rgb = hue_to_rgb( hue )
	mid_rgb( col_rgb[0], col_rgb[1], col_rgb[2] )
	update()

"""
Set the right backlight to supplied hue

Args:
    hue (float): hue value between 0.0 and 1.0
"""
def right_hue( hue ):
	col_rgb = hue_to_rgb( hue )
	right_rgb( col_rgb[0], col_rgb[1], col_rgb[2] )
	update()

"""
Set the left backlight to supplied r, g, b colour

Args:
    r (int): red value between 0 and 255
    g (int): green value between 0 and 255
    b (int): blue value between 0 and 255
"""
def left_rgb( r, g, b ):
	set(LED_L_R, r)
	set(LED_L_B, b)
	set(LED_L_G, g)
	update()

"""
Set the middle backlight to supplied r, g, b colour

Args:
    r (int): red value between 0 and 255
    g (int): green value between 0 and 255
    b (int): blue value between 0 and 255
"""
def mid_rgb( r, g, b ):
	set(LED_M_R, r)
	set(LED_M_B, b)
	set(LED_M_G, g)
	update()

"""
Set the right backlight to supplied r, g, b colour

Args:
    r (int): red value between 0 and 255
    g (int): green value between 0 and 255
    b (int): blue value between 0 and 255
"""
def right_rgb( r, g, b ):
	set(LED_R_R, r)
	set(LED_R_B, b)
	set(LED_R_G, g)
	update()

"""
Sets all backlights to supplied r, g, b colour

Args:
    r (int): red value between 0 and 255
    g (int): green value between 0 and 255
    b (int): blue value between 0 and 255
"""
def rgb( r, g, b ):
	left_rgb( r, g, b )
	mid_rgb( r, g, b )
	right_rgb( r, g, b)

"""
Update backlight with changes to the LED buffer
"""
def update():
	sn3218.output(leds)
