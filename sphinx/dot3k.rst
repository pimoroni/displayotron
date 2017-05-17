.. role:: python(code)
   :language: python

.. toctree::
   :titlesonly:
   :maxdepth: 0

Display-o-Tron 3000
-------------------

This documentation will guide you through the methods available in the Display-o-Tron 3000 and Display-o-Tron HAT libraries.

At A Glance
===========

.. raw:: html

    <div id="ataglance">

.. automoduleoutline:: dot3k.lcd
   :members:

.. automoduleoutline:: dot3k.backlight
   :members:

.. automoduleoutline:: dot3k.joystick
   :members:

.. raw:: html

    </div>

LCD
===

.. automethod:: dot3k.lcd.clear

.. automethod:: dot3k.lcd.clear

.. automethod:: dot3k.lcd.create_animation

.. automethod:: dot3k.lcd.create_char

.. automethod:: dot3k.lcd.set_contrast

.. automethod:: dot3k.lcd.set_cursor_offset

.. automethod:: dot3k.lcd.set_cursor_position

.. automethod:: dot3k.lcd.set_display_mode

.. automethod:: dot3k.lcd.update_animations

.. automethod:: dot3k.lcd.write

Backlight
=========

.. automethod:: dot3k.backlight.hue

.. automethod:: dot3k.backlight.hue_to_rgb

.. automethod:: dot3k.backlight.left_hue

.. automethod:: dot3k.backlight.left_rgb

.. automethod:: dot3k.backlight.mid_hue

.. automethod:: dot3k.backlight.mid_rgb

.. automethod:: dot3k.backlight.off

.. automethod:: dot3k.backlight.rgb

.. automethod:: dot3k.backlight.right_hue

.. automethod:: dot3k.backlight.right_rgb

.. automethod:: dot3k.backlight.set

.. automethod:: dot3k.backlight.set_bar

.. automethod:: dot3k.backlight.set_graph

.. automethod:: dot3k.backlight.sweep

.. automethod:: dot3k.backlight.update

.. automethod:: dot3k.backlight.use_rbg

Joystick
========

.. automethod:: dot3k.joystick.millis

.. automethod:: dot3k.joystick.on

.. automethod:: dot3k.joystick.repeat