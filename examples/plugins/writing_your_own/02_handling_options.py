#!/usr/bin/env python

"""
This example builds upon our hello_world plugin,
now we're going to add some options to cycle though.

Because interfaces can differ widely, there are no helpers
for displaying and cycling through options. You might choose
to lay out icons on a single screen/row or cycle through
multiple lines of text.

In this example, we're going to to the latter!
"""

from dot3k.menu import MenuOption


class HelloWorld(MenuOption):
    """
    First we introduce __init__, this is called when your plugin
    is first instantiated and is where you should create the variables
    you wish to use.

    You *must* also call MenuOption.__init__(self)
    """

    def __init__(self):
        """
        We need somewhere to track which option is selected
        """
        self.selected_option = 0

        """
        We should also keep track of what the options are
        """
        self.options = [
            'Pirate',
            'Monkey',
            'Robot',
            'Ninja',
            'Dolphin'
        ]

        """
        You *must* call the __init__ method on the parent class
        """
        MenuOption.__init__(self)

    """
    These functions let us move between options,
    wrapping around when we reach the lowest or highest

    The use of modulus ( % ) is an easy way to wrap around
    without any pesky, complex logic
    """

    def next_option(self):
        self.selected_option = (self.selected_option + 1) % len(self.options)

    def prev_option(self):
        self.selected_option = (self.selected_option - 1) % len(self.options)

    """
    We'll need to override the up/down control methods
    to call our next/prev methods
    """

    def up(self):
        self.prev_option()

    def down(self):
        self.next_option()

    """
    And these are some handy functions for getting the prev/next/current
    option text for display on the menu.
    """

    def get_current_option(self):
        return self.options[self.selected_option]

    def get_next_option(self):
        return self.options[(self.selected_option + 1) % len(self.options)]

    def get_prev_option(self):
        return self.options[(self.selected_option - 1) % len(self.options)]

    """
    When the menu is redrawn, it calls your plugins
    redraw method and passes an instance of itself.
    """

    def redraw(self, menu):
        menu.write_option(
            row=0,
            margin=1,
            text=self.get_prev_option()
        )

        menu.write_option(
            row=1,
            margin=1,
            icon='>',
            text=self.get_current_option()
        )

        menu.write_option(
            row=2,
            margin=1,
            text=self.get_next_option()
        )


from dot3k.menu import Menu
import dot3k.joystick
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
We'll virtually press "right" to
enter your plugin:

"""
menu.right()

"""
We will also need to handle up/down
to let us select options
"""


@dot3k.joystick.on(dot3k.joystick.UP)
def handle_up(pin):
    menu.up()


@dot3k.joystick.on(dot3k.joystick.DOWN)
def handle_down(pin):
    menu.down()


"""
You can decide when the menu is redrawn, but
you'll usually want to do this:
"""
while 1:
    menu.redraw()
    time.sleep(0.01)
