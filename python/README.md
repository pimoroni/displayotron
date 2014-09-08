dot3k
=====

Requirements
------------

You should install python-smbus first via apt:

    sudo apt-get install python-smbus


Usage
=====

LCD
---

    import dot3k
    dot3k.lcd.write('Hello World!')


Backlight
---------

    import dot3k
    dot3k.backlight.sweep(0.5)
    dot3k.backlight.update()

Joystick
--------

    import dot3k
    def joystick_up():
        print("Joystick up!")
    dot3k.joystick.up = joystick_up
