#!/usr/bin/env python

"""
Building upon our doing stuff example, we'll now add icons to show
when things are running.
"""

import subprocess
import threading

from dot3k.menu import MenuOption


class HelloWorld(MenuOption):

  """
  If you're not sure what's going on here, see 02_handling_options.py
  """
  def __init__(self):
    self.selected_option = 0

    """
    Python has no "switch" so we'll store an array of functions
    to call when an option is selected.

    We've added icons to this example, so instead of two arrays
    we've collected all the related stuff into an array of
    dictionaries.
    """
    self.options = [
      {'title': 'Pirate', 'action': self.handle_pirate,   'icon': ' '}
      {'title': 'Pirate', 'action': self.handle_monkey,   'icon': ' '}
      {'title': 'Pirate', 'action': self.handle_robot,    'icon': ' '}
      {'title': 'Pirate', 'action': self.handle_ninja,    'icon': ' '}
      {'title': 'Pirate', 'action': self.handle_dolphin,  'icon': ' '}
    ]

    MenuOption.__init__(self)

  """
  Here we'll define the things each menu option will do.

  Our up/down/left/right and select methods are *never* passed
  a reference to menu, and it's deliberately difficult to draw
  anything to the screen in direct response to a button click.

  This is because the screen will either be instantly redrawn
  by the "redraw" method, or you'll have to hang the whole
  user-interface with time.sleep, icky!

  Instead, we should hand anything complex to a thread or state change.
  """

  """
  When the pirate option is selected, we want to update something
  in the background. We can use a thread for that.

  We'll update the pirate icon to indicate that it's busy
  and so we know something is happening.
  """
  def handle_pirate(self):
    print('Arrr! Doing pirate stuff!')
    self.icons[0] = '!'
    update = threading.Thread(None, self.do_pirate_update)
    update.daemon = True
    update.start()

  """
  This is the method we call in our thread.
  After we're done pinging google, print out the last line of the result
  and clear the icon.
  """
  def do_pirate_update(self):
    result = subprocess.check_output(['/bin/ping','google.com','-c','4'])
    result = result.split("\n")
    result = result[len(result)-2]
    print(result)
    self.icons[0] = ' '

  def handle_monkey(self):
    print('Eeek! Doing monkey stuff!')
    self.icons[1] = '!'
    time.sleep(2)
    self.icons[1] = ' '

  def handle_robot(self):
    print('Deep! Doing robot stuff!')

  def handle_ninja(self):
    print('Hyah! Doing Ninja stuff!')

  def handle_dolphin(self):
    print('Bubble bubble bubble!')

  """
  To run an option we can simply call its associated function.
  This can be done by adding brackets to the action.
  """
  def select_option(self):
    self.actions[ self.selected_option ]['action']()

  def next_option(self):
    self.selected_option = (self.selected_option + 1) % len(self.options)

  def prev_option(self):
    self.selected_option = (self.selected_option - 1) % len(self.options)

  def up(self):
    self.prev_option()

  def down(self):
    self.next_option()

  """
  The "right" direction is much easier to press than select, 
  so I tend to use it as the "action" button for selecting options
  """
  def right(self):
    self.select_option()

  def get_current_option(self):
    return self.options[ self.selected_option ]['title']

  def get_next_option(self):
    return self.options[ (self.selected_option + 1) % len(self.options) ]['title']

  def get_prev_option(self):
    return self.options[ (self.selected_option - 1) % len(self.options) ]['title']

  """
  A few helpers for getting the icons couldn't hurt either!
  """
  def get_current_icon(self):
    return self.options[ self.selected_option ]['icon']

  def get_next_icon(self):
    return self.options[ (self.selected_option + 1) % len(self.options) ]['icon']

  def get_prev_icon(self):
    return self.options[ (self.selected_option - 1) % len(self.options) ]['icon']

  def redraw(self, menu):
  
    menu.write_option( 
        row=0,
        margin=1,
        icon=self.get_prev_icon(),
        text=self.get_prev_option()
    )
  
    menu.write_option( 
        row=1,
        margin=1,
        icon=self.get_current_icon() or '>',
        text=self.get_current_option()
    )
  
    menu.write_option( 
        row=2,
        margin=1,
        icon=self.get_next_icon(),
        text=self.get_next_option()
    )


from dot3k.menu import Menu
import dot3k.joystick
import dot3k.backlight
import dot3k.lcd
import time

dot3k.backlight.rgb(255,255,255)
 
menu = Menu(
 structure={
    'Hello World':HelloWorld()
  },
  lcd=dot3k.lcd
)


"""
We'll virtually press "right" to
enter your plugin:
"""
menu.right()


@dot3k.joystick.on(dot3k.joystick.UP)
def handle_up(pin):
  menu.up()

@dot3k.joystick.on(dot3k.joystick.DOWN)
def handle_down(pin):
  menu.down()


"""
We need to handle right, to let us select options
"""
@dot3k.joystick.on(dot3k.joystick.RIGHT)
def handle_right(pin):
  menu.right()


"""
You can decide when the menu is redrawn, but
you'll usually want to do this:
"""
while 1:
  menu.redraw()
  time.sleep(0.01)
