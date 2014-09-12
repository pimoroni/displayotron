dot3k
=====

Hardware Requirements
---------------------

You'll need to enable spi.

    sudo raspi-config

Then head into Advanced Options -> SPI -> Yes.

And i2c.

    sudo nano /etc/modprobe.d/raspi-blacklist.conf

And comment out ( place a # before ):

    blacklist i2c-bcm2708

And also:

    sudo nano /etc/modules

Add the line:
   
    i2c-dev

Reboot to make these changes take effect.

Software Requirements
---------------------

Next you should install python-smbus and python-dev via apt:

    sudo apt-get install python-smbus python-dev

And pip, if you don't have it:

    sudo apt-get install python-pip

Then install st7036 and sn3218 using pip:

    sudo pip install st7036 sn3218

You can run the requirements.sh file to do this for you!

Usage
=====

LCD
---

    import dot3k.lcd as lcd
    lcd.write('Hello World!')


Backlight
---------

    import dot3k.backlight as backlight
    backlight.sweep(0.5)
    backlight.update()

Joystick
--------

    import dot3k.joystick as joystick
    @joystick.on(joystick.UP)
    def handle_joystick_up(pin):
        print("Joystick up!")
