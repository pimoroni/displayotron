Dot3k Plugin Guide
==================

So, you want to make a plugin, huh?

Dot3k has a handy class, MenuOption, you can inherit from to build menu plugins.

When a menu plugin is run, it'll take over the screen and all joystick input will be passed to it.

Example
-------

This super simple example is what you need to get something displaying from your plugin on the Dot3k LCD. Easy!

    class MyPlugin(MenuOption):
      def redraw(self, menu):
        menu.clear_row(0)
        menu.write_row(1,'Hello World')
        menu.clear_row(2)

Every time redraw is called, the parent menu sends itself and lets you call write_row, clear_row or write_option to draw things to the LCD.

You should always call menu.clear_row() on any rows you don't use.

menu.write_row and menu.write_option will always truncate any text that doesn't fit on the screen. You can implement a scrolling marquee, but doing this automatically is on the feature roadmap!

Methods
-------

MenuOption has the following methods which you can override:

* up - called when the joystick is pressed up, or the menu gets the up command.
* down - as above, but for down!
* left - as above, but you should return true if you want to prevent the menu exiting your plugin
* right - yup, this is called when you press right.
* select - by default this returns true and causes the menu to exit your plugin, return false to prevent
* redraw - called every draw pass, you can draw using menu.write_row here, make sure to clear_row rows you don't use
* begin - called when the menu enters your plugin, use to start games, reset things, etc
* setup - the config is passed to this method by default, you should overide like so:

    def setup(self, config):
      MenuOption.setup(self, config)
      # Your stuff

Options
-------

MenuOption also includes the methods set_option and get_option for saving and loading options from dot3k.cfg.

The Menu class will automatically save the current settings to dot3k.cfg when it exits.
