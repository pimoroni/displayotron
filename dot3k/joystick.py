import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

JOY_LEFT  = 0
JOY_RIGHT = 0
JOY_UP	  = 0
JOY_DOWN  = 0
JOY_BTN	  = 0

BOUNCE    = 30

def callback_up():
    pass

def callback_down():
    pass

def callback_right():
    pass

def callback_left():
    pass

def callback_button():
    pass

up   = GPIO.setup(JOY_UP,   GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
down = GPIO.setup(JOY_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
left = GPIO.setup(JOY_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
right= GPIO.setup(JOY_RIGHT,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
btn  = GPIO.setup(JOY_BTN,  GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(up,   GPIO.RISING,callback=up,   bouncetime=BOUNCE)
GPIO.add_event_detect(down, GPIO.RISING,callback=down, bouncetime=BOUNCE)
GPIO.add_event_detect(left, GPIO.RISING,callback=left, bouncetime=BOUNCE)
GPIO.add_event_detect(right,GPIO.RISING,callback=right,bouncetime=BOUNCE)
GPIO.add_event_detect(btn,  GPIO.RISING,callback=btn,  bouncetime=BOUNCE)
