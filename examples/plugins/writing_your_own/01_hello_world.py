#!/usr/bin/env python

"""
Every dot3k.menu plugin is derived from MenuOption
"""

from dot3k.menu import MenuOption


class HelloWorld(MenuOption):
    """
    When the menu is redrawn, it calls your plugins
    redraw method and passes an instance of itself.
    """

    def redraw(self, menu):
        """
        The instance of menu has a couple of useful
        methods which you can use to draw to the screen

        menu.write_row(row_number, text_string) will write
        a simple string to the screen at the row you choose.
        It's a fast, no-frills way of drawing.

        Anything longer than 16 characters will get truncated!
        """
        menu.write_row(0, 'Hello World         Hello?')

        """
        menu.write_option() is a lot more complex, it lets
        you position text with icons, margins and auto-scrolling.

        Let's give it a go with a long string of text!
        """
        menu.write_option(
            row=1,
            text='Hello World! How are you today?',
            scroll=True
        )

        """
        If you're not going to use a row, you should clear it!
        """

        menu.clear_row(2)


from dot3k.menu import Menu
import dot3k.backlight
import dot3k.lcd
import time

"""
Let there be light!
"""
dot3k.backlight.rgb(255, 255, 255)

"""
The menu structure is defined as a nested dictionary,
to "install" your plugin, it should be added like so:

You will also need to pass Menu a reference to the LCD
you wish to draw to.
"""
menu = Menu(
    structure={
        'Hello World': HelloWorld()
    },
    lcd=dot3k.lcd
)

"""
We're not going to handle any input, so go
right ahead and virtually press "right" to
enter your plugin:

"""
menu.right()

"""
You can decide when the menu is redrawn, but
you'll usually want to do this:
"""
while 1:
    menu.redraw()
    time.sleep(0.01)
