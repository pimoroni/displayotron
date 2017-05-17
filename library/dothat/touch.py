from sys import exit

try:
    from cap1xxx import Cap1166, PID_CAP1166
except ImportError:
    exit("This library requires the cap1xxx module\nInstall with: sudo pip install cap1xxx")


I2C_ADDR = 0x2c

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 5
BUTTON = 4
CANCEL = 0

_cap1166 = Cap1166(i2c_addr=I2C_ADDR)
_cap1166._write_byte(0x26, 0b00111111)  # Force recalibration

for x in range(6):
    _cap1166.set_led_linking(x, False)

def high_sensitivity():
    """Switch to high sensitivity mode

    This predetermined high sensitivity mode is for using
    touch through 3mm perspex or similar materials.

    """

    _cap1166._write_byte(0x00, 0b11000000)
    _cap1166._write_byte(0x1f, 0b00000000)

def enable_repeat(enable):
    """Enable touch hold repeat

    If enable is true, repeat will be enabled. This will
    trigger new touch events at the set repeat_rate when
    a touch input is held.

    :param enable: enable/disable repeat: True/False

    """

    if enable:
        _cap1166.enable_repeat(0b11111111)
    else:
        _cap1166.enable_repeat(0b00000000)

def set_repeat_rate(rate):
    """Set hold repeat rate

    Repeat rate values are clamped to the nearest 35ms,
    values from 35 to 560 are valid.

    :param rate: time in ms from 35 to 560

    """

    _cap1166.set_repeat_rate(rate)

def on(buttons, bounce=-1):
    """Handle a press of one or more buttons

    Decorator. Use with @captouch.on(UP)

    :param buttons: List, or single instance of cap touch button constant
    :param bounce: Maintained for compatibility with Dot3k joystick, unused

    """
    buttons = buttons if isinstance(buttons, list) else [buttons]

    def register(handler):
        for button in buttons:
            _cap1166.on(channel=button, event='press', handler=handler)
            _cap1166.on(channel=button, event='held', handler=handler)

    return register


def bind_defaults(menu):
    """Bind the default controls to a menu instance

    This should be used in conjunction with a menu class instance
    to bind touch inputs to the default controls.

    """
    @on(UP)
    def handle_up(ch, evt):
        menu.up()

    @on(DOWN)
    def handle_down(ch, evt):
        menu.down()

    @on(LEFT)
    def handle_left(ch, evt):
        menu.left()

    @on(RIGHT)
    def handle_right(ch, evt):
        menu.right()

    @on(BUTTON)
    def handle_button(ch, evt):
        menu.select()

    @on(CANCEL)
    def handle_cancel(ch, evt):
        menu.cancel()
