Basic Examples
==============

hello_world.py
--------------

Just a simple "Hello World"


backlight.py
------------

Shows you how to set individual RGB LEDs, or all of them at once


bargraph.py
-----------

Shows how to display a percentage on the bargraph, or control the LEDs individually


hue.py
-----------

Sets the backlight to a hue using colorsys


ipaddr.py
-----------

Displays hostname and eth0/wlan0 IP addresses


joystick.py
-----------

Basic example showing event-driven joystick handling. You can watch for up/down/left/right/click events with a Python decorator ( @joystick.on(joystick.UP) ) and respond accordingly without having to poll.


mouse.py
--------

You're on a Model A+ and you only have a keyboard? Never fear, dot3k mouse is here!

To run this example, you'll need to install python-uinput and some dependencies:

    sudo apt-get install libudev-dev
    sudo pip install python-uinput

You also need to make sure the uinput module is running on your Pi:

    sudo modprobe uinput

Then run mouse.py and move the joystick on your dot3k to control the mouse.
