import sys

if sys.version_info[0] >= 3:
    from . import lcd
    from . import backlight
    from . import joystick
else:
    import lcd, backlight, joystick
