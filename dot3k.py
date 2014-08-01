import sn3218, st7036, time, copy, colorsys, math, psutil

leds = [0] * 18

def set_backlight(r, g, b):
	leds[0] = leds[3] = leds[6] = int(r * 255)
	leds[2] = leds[5] = leds[8] = int(g * 255)
	leds[1] = leds[4] = leds[7] = int(b * 255)
	sn3218.output(leds)

def set_backlight_hue(hue):
	r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

	leds[0] = leds[3] = leds[6] = int(r * 255)
	leds[2] = leds[5] = leds[8] = int(g * 255)
	leds[1] = leds[4] = leds[7] = int(b * 255)
	sn3218.output(leds)

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

	sn3218.output(leds)	

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


st7036 = st7036.st7036(register_select_pin=25)
st7036.set_cursor_position(2, 1)
st7036.write("test")

cpu_sample_count = 200
cpu_samples = [0] * cpu_sample_count
hue = 0.0
while True:
	hue += 0.01
	set_backlight_hue(hue)

	cpu_samples.append(psutil.cpu_percent() / 100.0)
	cpu_samples.pop(0)

	cpu_avg = sum(cpu_samples) / cpu_sample_count
	set_graph(cpu_avg)

	if hue > 1.0:
		hue = 0.0
