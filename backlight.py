import sn3218, colorsys, math

LED_R_R = 0x00
LED_R_B = 0x01
LED_R_G = 0x02

LED_M_R = 0x03
LED_M_B = 0x04
LED_M_G = 0x05

LED_L_R = 0x06
LED_L_B = 0x07
LED_L_G = 0x08

leds = [0x00] * 18

# set gamma correction for backlight to normalise brightness
g_channel_gamma = [value / 6 for value in sn3218.default_gamma_table]
sn3218.channel_gamma(2, g_channel_gamma)
sn3218.channel_gamma(5, g_channel_gamma)
sn3218.channel_gamma(8, g_channel_gamma)

r_channel_gamma = [value / 2 for value in sn3218.default_gamma_table]
sn3218.channel_gamma(0, r_channel_gamma)
sn3218.channel_gamma(3, r_channel_gamma)
sn3218.channel_gamma(6, r_channel_gamma)

w_channel_gamma = [value / 12 for value in sn3218.default_gamma_table]
for i in range(9, 18):
	sn3218.channel_gamma(i, w_channel_gamma)

sn3218.enable()

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

def set(index, value):
	leds[index] = value

def setBar(index, value):
	if isinstance(value, int):
		set(LED_L_G + 1 + index, value)
	if isinstance(value, list):
		for i, v in enumerate(value):
				set(LED_L_G + 1 + ((index + i)%9), v)
	update()
	
def hue_to_rgb( hue ):
	rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

	return [int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)]

def hue( hue ):
	rgb = hue_to_rgb( hue )
	RGB( rgb[0], rgb[1], rgb[2] )

def sweep( hue, range = 0.08 ):
	leftHue( (hue-range) % 1 )
	midHue( hue )
	rightHue( (hue+range) % 1 )

def leftHue( hue ):
	rgb = hue_to_rgb( hue )
	leftRGB( rgb[0], rgb[1], rgb[2] )
	update()

def midHue( hue ):
	rgb = hue_to_rgb( hue )
	midRGB( rgb[0], rgb[1], rgb[2] )
	update()

def rightHue( hue ):
	rgb = hue_to_rgb( hue )
	rightRGB( rgb[0], rgb[1], rgb[2] )
	update()

def leftRGB( r, g, b ):
	set(LED_L_R, r)
	set(LED_L_B, b)
	set(LED_L_G, g)
	update()

def midRGB( r, g, b ):
	set(LED_M_R, r)
	set(LED_M_B, b)
	set(LED_M_G, g)
	update()

def rightRGB( r, g, b ):
	set(LED_R_R, r)
	set(LED_R_B, b)
	set(LED_R_G, g)
	update()

def RGB( r, g, b ):
	leftRGB( r, g, b )
	midRGB( r, g, b )
	rightRGB( r, g, b)

def update():
	sn3218.output(leds)
