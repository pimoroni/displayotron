import sn3218, colorsys, math
import cap1xxx

cap = cap1xxx.Cap1166(i2c_addr=0x2C)
cap._write_byte(0x00, 0b00000000)
cap._write_byte(0x1f, 0b00010000)

R_RAMPRATES   = 0x94 # Always 0b00000000 for 0ms/0ms
R_MODE        = 0x81 # Always 0b00000000 for Direct
R_MODE_2      = 0x82 # Always 0b00000000 for Direct
R_DIRECT_DUTY = 0x93 # Always 0bXXXX0000 for XXXX = Brightness, 0000 = Min = Off
R_POLARITY    = 0x73 # 1 for ON 0 for OFF
R_STATE       = 0x74 # Always 0 except for brightness controlled LED

NUM_LEDS      = 6
STEP_VALUE    = 16

leds = [0x00] * 18 # B G R, B G R, B G R, B G R, B G R, B G R

# set gamma correction for backlight to normalise brightness
g_channel_gamma = [int(value / 1.6) for value in sn3218.default_gamma_table]
r_channel_gamma = [int(value / 1.4) for value in sn3218.default_gamma_table]

for x in range(0,18,3):
    sn3218.channel_gamma(x+1, g_channel_gamma)
    sn3218.channel_gamma(x+2, r_channel_gamma)

sn3218.enable()

def use_rbg():
    """
    Swaps the Green and Blue channels on the LED backlight
  
    Use if you have a first batch Display-o-Tron 3K
    """
    pass

def graph_off():
    cap._write_byte(R_DIRECT_POLARITY, 0b00000000)
    cap._write_byte(R_DIRECT_STATE, 0b00000000)

def set_graph(percentage):
    """
    Lights a number of bargraph LEDs depending upon value
    
    Args:
        value (float): percentage between 0.0 and 1.0

    Todo:
        Reimplement using CAP
    """
    cap._write_byte(R_RAMPRATES, 0b00000000)
    cap._write_byte(R_MODE,      0b00000000)
    cap._write_byte(R_MODE_2,    0b00000000)

    total_value = STEP_VALUE*NUM_LEDS
    actual_value = int(total_value * percentage)
    set_polarity = 0b00000000
    set_state    = 0b00000000
    set_duty     = 0 # Value from 0 to 15
    for x in range(NUM_LEDS):
        if actual_value >= STEP_VALUE:
            set_polarity |= 1 << x
        if actual_value < STEP_VALUE and actual_value > 0:
            set_state |= 1 << x
            set_duty = actual_value << 4
        actual_value -= STEP_VALUE
    cap._write_byte(R_DIRECT_DUTY, set_duty)
    cap._write_byte(R_POLARITY,    set_polarity)
    cap._write_byte(R_STATE,       set_state)

def set(index, value):
    """
    Set a specific LED to a value
    
    Args:
        index (int): index of the LED from 0 to 18
        value (int): brightness value from 0 to 255
    """
    leds[index] = value
    update()

def set_bar(index, value):
    """
    Set a value or values to one or more LEDs
    
    Args:
        index (int): starting index
        value (int or list): a single int, or list of brightness values from 0 to 255
    """
    pass
    
def hue_to_rgb( hue ):
    """
    Converts a hue to RGB brightness values
    
    Args:
        hue (float): hue value between 0.0 and 1.0
    """
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

    return [int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)]

def hue( hue ):
    """
    Sets the backlight LEDs to supplied hue
    
    Args:
        hue (float): hue value between 0.0 and 1.0
    """
    col_rgb = hue_to_rgb( hue )
    rgb( col_rgb[0], col_rgb[1], col_rgb[2] )


def sweepfull( hue, sweep_range = 0.0833 ):
    global leds
    for x in range(0,18,3):
        rgb = hue_to_rgb( (hue + (sweep_range*(x/3))) % 1 )
        rgb.reverse()
        leds[x:x+3] = rgb
    update()
        

def sweep( hue, range = 0.08 ):
    """
    Sets the backlight LEDs to a gradient centered on supplied hue
    
    Supplying zero to range would be the same as hue()
    
    Args:
        hue (float): hue value between 0.0 and 1.0
        range (float): range value to deviate the left and right hue
    """
    left_hue( (hue-range) % 1 )
    mid_hue( hue )
    right_hue( (hue+range) % 1 )

def left_hue( hue ):
    """
    Set the left backlight to supplied hue
    
    Args:
        hue (float): hue value between 0.0 and 1.0
    """
    col_rgb = hue_to_rgb( hue )
    left_rgb( col_rgb[0], col_rgb[1], col_rgb[2] )
    update()

def mid_hue( hue ):
    """
    Set the middle backlight to supplied hue
    
    Args:
        hue (float): hue value between 0.0 and 1.0
    """
    col_rgb = hue_to_rgb( hue )
    mid_rgb( col_rgb[0], col_rgb[1], col_rgb[2] )
    update()

def right_hue( hue ):
    """
    Set the right backlight to supplied hue
    
    Args:
        hue (float): hue value between 0.0 and 1.0
    """
    col_rgb = hue_to_rgb( hue )
    right_rgb( col_rgb[0], col_rgb[1], col_rgb[2] )
    update()

def left_rgb( r, g, b ):
    """
    Set the left backlight to supplied r, g, b colour
    
    Args:
        r (int): red value between 0 and 255
        g (int): green value between 0 and 255
        b (int): blue value between 0 and 255
    """
    single_rgb(0, r, g, b)
    single_rgb(1, r, g, b)
    update()

def mid_rgb( r, g, b ):
    """
    Set the middle backlight to supplied r, g, b colour
    
    Args:
        r (int): red value between 0 and 255
        g (int): green value between 0 and 255
        b (int): blue value between 0 and 255
    """
    single_rgb(2, r, g, b)
    single_rgb(3, r, g, b)
    update()

def right_rgb( r, g, b ):
    """
    Set the right backlight to supplied r, g, b colour
    
    Args:
        r (int): red value between 0 and 255
        g (int): green value between 0 and 255
        b (int): blue value between 0 and 255
    """
    single_rgb(4, r, g, b)
    single_rgb(5, r, g, b)
    update()


def single_rgb( led, r, g, b ):
    global leds
    leds[led]   = b
    leds[led+1] = g
    leds[led+2] = r

def rgb( r, g, b ):
    """
    Sets all backlights to supplied r, g, b colour
    
    Args:
        r (int): red value between 0 and 255
        g (int): green value between 0 and 255
        b (int): blue value between 0 and 255
    """
    global leds
    leds = [b, g, r] * 6
    update()
    
def off():
    """
    Turns off the backlight.
    """
    rgb(0,0,0)

def update():
    """
    Update backlight with changes to the LED buffer
    """
    sn3218.output(leds)
