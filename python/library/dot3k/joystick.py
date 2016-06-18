import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LEFT = 17
RIGHT = 22

if GPIO.RPI_REVISION == 1:
    UP = 21
else:
    UP = 27

DOWN = 9
BUTTON = 4

BOUNCE = 300

repeat_status = {
    UP: False,
    DOWN: False,
    LEFT: False,
    RIGHT: False,
    BUTTON: False
}


def on(buttons, bounce=BOUNCE):
    """
    Decorator. Use with @joystick.on(joystick.UP)
    Args:
      buttons (list): List, or single instance of joystick button constant
      bounce (int): Debounce time in milliseconds
    """
    buttons = buttons if isinstance(buttons, list) else [buttons]

    def register(handler):
        for button in buttons:
            GPIO.remove_event_detect(button)
            GPIO.add_event_detect(button, GPIO.FALLING, callback=handler, bouncetime=bounce)

    return register


def millis():
    return int(round(time.time() * 1000))


def repeat(button, handler, delay=0.1, ramp=1.0):
    """
    If you want to hold a direction and have it auto-repeat,
    call this within a joystick direction handler.
    Args:
      button (int): Joystick button constant to watch
      handler (function): Function to call every repeat
      delay (float): Delay, in seconds, before repeat starts and between each repeat
      ramp (float): Multiplier applied to delay after each repeat, 1.0=linear speed up
    """
    if repeat_status[button]:
        return False
    repeat_status[button] = True
    last_trigger = millis()
    while GPIO.input(button) == 0:
        m = millis()
        if m - last_trigger >= (delay * 1000):
            handler()
            delay *= ramp
            last_trigger = m
    repeat_status[button] = False


up = GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
down = GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
left = GPIO.setup(LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
right = GPIO.setup(RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
button = GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
