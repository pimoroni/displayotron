Advanced Examples
=================

radio.py
--------

This is a fully functioning internet radio for your Raspberry Pi, using dot3k.menu and a Radio/Volume plugin.

You'll need VLC installed:

    sudo apt-get install vlc

Then run with:

    sudo ./radio.py

Radio picks up its presets from dot3k.cfg next to it, or ~/.dot3k.cfg, you can add new presets by editing the config file and adding them under the [Radio Stations] section like so:

    [Radio Stations]
    mystation = Friendly Title,http://feedurl/feed
    myotherstation = Another Friendly Title,http://feedurl/otherfeed

In order for radio.py to detect the current playing feed, you'll need to use the final feed ( that you get redirected to in VLC ).

If you have an existing instance of VLC running, radio.py will try to connect to it. You can start VLC with the bash script ( also used in radio.py ):

    sudo ./vlc.sh

The remote utilities playstream and playshoutcast will work even if radio.py isn't running.

menu.py
------

Make sure you install psutil:

    sudo pip install psutil

A demonstration of menu building and plugins. Shows CPU usage and Temp, contrast configuration, backlight configuration and a basic animation example.


backlight.py
------------

Basic example showing the range of backlight colours.

animations.py
-------------

Silly example showing a whole host of tiny animations, and the kitchen sink!
