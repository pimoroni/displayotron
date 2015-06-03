from cap1xxx import Cap1166, Detect, PID_CAP1166

I2C_ADDR = 0x2c

UP     = 1
DOWN   = 2
LEFT   = 3
RIGHT  = 5
BUTTON = 4
CANCEL = 0

_cap1166 = None

if Detect(I2C_ADDR, PID_CAP1166):
    _cap1166 = Cap1166(I2C_ADDR)
    _cap1166.enable_led_linking(0b00000000)
else:
    print("Display-o-Tron 4000 Cap Touch Not Found!")

def _handle_touch(channel,event):
    print("{}, {}".format(channel, event))

#for channel in range(6):
#    for event in ['press','release','held']:
#        _cap1166.on(channel=channel, event=event, handler=_handle_touch)

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
