from cap1xxx import Cap1166, PID_CAP1166

I2C_ADDR = 0x2c

UP     = 1
DOWN   = 2
LEFT   = 3
RIGHT  = 5
BUTTON = 4
CANCEL = 0

_cap1166 = Cap1166(i2c_addr=I2C_ADDR)
for x in range(6):
    _cap1166.set_led_linking(x,False)

def high_sensitivity():
    _cap1166._write_byte(0x00, 0b11000000)
    _cap1166._write_byte(0x1f, 0b00000000)

def _handle_touch(channel,event):
    print("{}, {}".format(channel, event))

def on(buttons, bounce=-1):
    """
    Decorator. Use with @captouch.on(captouch.UP)
    Args:
      buttons (list): List, or single instance of cap touch button constant
      bounce (int): Maintained for compatibility with Dot3k joystick, unused
    """
    buttons = buttons if isinstance(buttons, list) else [buttons]
    
    def register(handler):
        for button in buttons:
            _cap1166.on(channel=button, event='press', handler=handler)
    
    return register
