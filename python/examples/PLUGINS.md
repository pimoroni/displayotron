Dot3k Plugin Guide
==================

So, you want to make a plugin, huh?

Dot3k has a handy class, MenuOption, you can inherit from to build menu plugins.

When a menu plugin is run, it'll take over the screen and all joystick input will be passed to it.

Example
-------

This super simple example is what you need to get something displaying from your plugin on the Dot3k LCD. Easy!

    class MyPlugin(MenuOption):
      def redraw(self):
        self.lcd.write('Hello World')

Methods
-------

MenuOption has the following methods which you can override:

* up - called when the joystick is pressed up, or the menu gets the up command.
* down - as above, but for down!
* left - as above, but you should return true if you want to prevent the menu exiting your plugin
* right - yup, this is called when you press right.
* select - by default this returns true and causes the menu to exit your plugin, return false to prevent
* redraw - called every draw pass, you can draw to self.lcd here, the lcd will start blank
* setup - lcd and config are passed to this method by default, you should overide like so:

    def setup(self, lcd, config):
      MenuOption.setup(self, lcd, config)
      # Your stuff

Options
-------

MenuOption also includes the methods set_option and get_option for saving and loading options from dot3k.cfg.

The Menu class will automatically save the current settings to dot3k.cfg when it exits.
