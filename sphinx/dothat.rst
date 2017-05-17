.. role:: python(code)
   :language: python

.. toctree::
   :titlesonly:
   :maxdepth: 0

Display-o-Tron HAT
------------------

This documentation will guide you through the methods available in the Display-o-Tron HAT library.

At A Glance
===========

.. raw:: html

    <div id="ataglance">

.. automoduleoutline:: dothat.lcd
   :members:

.. automoduleoutline:: dothat.backlight
   :members:

.. automoduleoutline:: dothat.touch
   :members:

.. raw:: html

    </div>

LCD
===

.. automethod:: dothat.lcd.clear

.. automethod:: dothat.lcd.create_animation

.. automethod:: dothat.lcd.create_char

.. automethod:: dothat.lcd.set_contrast

.. automethod:: dothat.lcd.set_cursor_offset

.. automethod:: dothat.lcd.set_cursor_position

.. automethod:: dothat.lcd.set_display_mode

.. automethod:: dothat.lcd.update_animations

.. automethod:: dothat.lcd.write

Backlight
=========

.. automethod:: dothat.backlight.hue

.. automethod:: dothat.backlight.hue_to_rgb

.. automethod:: dothat.backlight.left_hue

.. automethod:: dothat.backlight.left_rgb

.. automethod:: dothat.backlight.mid_hue

.. automethod:: dothat.backlight.mid_rgb

.. automethod:: dothat.backlight.off

.. automethod:: dothat.backlight.rgb

.. automethod:: dothat.backlight.right_hue

.. automethod:: dothat.backlight.right_rgb

.. automethod:: dothat.backlight.set

.. automethod:: dothat.backlight.set_bar

.. automethod:: dothat.backlight.set_graph

.. automethod:: dothat.backlight.single_rgb

.. automethod:: dothat.backlight.sweep

.. automethod:: dothat.backlight.update

.. automethod:: dothat.backlight.use_rbg

Touch
=====

.. automethod:: dothat.touch.bind_defaults

.. automethod:: dothat.touch.enable_repeat

.. automethod:: dothat.touch.high_sensitivity

.. automethod:: dothat.touch.on

.. automethod:: dothat.touch.set_repeat_rate