#!/usr/bin/env python

import dot3k.joystick as j
import dot3k.lcd as l
import dot3k.backlight as b
import signal, time


class Menu():

  def __init__(self, structure):
    self.list_location = []
    self.current_position = 0
    self.mode = 'navigate'
    self.menu_options = structure
    #self.redraw()
    #l.create_char(0,[16,24,28,30,30,28,24,16])

  def current_submenu(self):
    """
    Traverse the list of indexes in list_location
    and find the relevant nested dictionary
    """
    menu = self.menu_options
    for location in self.list_location:
      menu = menu[menu.keys()[location]]
    return menu

  def current_value(self):
    return self.current_submenu()[self.current_key()]
    
  def current_key(self):
    """
    Convert the integer current_position into
    a valid key for the currently selected dictionary
    """
    return self.current_submenu().keys()[self.current_position]

  def next_position(self):
    position = self.current_position + 1
    if position >= len(self.current_submenu()):
      position = 0
    return position

  def previous_position(self):
    position = self.current_position - 1
    if position < 0:
      position = len(self.current_submenu()) - 1
    return position

  def select_option(self):
    """
    Navigate into, or handle selected menu option accordingly
    """
    if type(self.current_value()) is dict:
      self.list_location.append( self.current_position )
      self.current_position = 0
    elif isinstance(self.current_value(),MenuOption):
      self.mode = 'adjust'
    if callable(type(self.current_submenu()[self.current_key()])):
      pass

  def prev_option(self):
    """
    Decrement the option pointer,
    select previous menu item
    """
    self.current_position = self.previous_position()

  def next_option(self):
    """
    Increment the option pointer,
    select next menu item
    """
    self.current_position = self.next_position()

  def exit_option(self):
    """
    Exit current submenu and restore position
    in previous menu
    """
    if len(self.list_location) > 0:
      self.current_position = self.list_location.pop()

  def select(self):
    """
    Handle "select" action
    """
    if self.mode == 'navigate':
      self.select_option()
    elif self.mode == 'adjust':
      # The "select" call must return true to exit the adjust
      if self.current_value().select():
        self.mode = 'navigate'
    #self.redraw()

  def up(self):
    if self.mode == 'navigate':
      self.prev_option()
    #self.redraw()

  def down(self):
    if self.mode == 'navigate':
      self.next_option()
    #self.redraw()

  def left(self):
    if self.mode == 'navigate':
      self.exit_option()
    elif self.mode == 'adjust':
      self.current_value().left()
    #self.redraw()

  def right(self):
    if self.mode == 'navigate':
      self.select_option()
    elif self.mode == 'adjust':
      self.current_value().right()
    #self.redraw()

  def redraw(self):
    l.clear()
    if self.mode == 'navigate':
      l.set_cursor_position(1,1) # x, y
      l.write(chr(252))
      l.write(self.current_submenu().keys()[self.current_position])

      if len(self.current_submenu()) > 2:
        l.set_cursor_position(1,0)
        l.write(self.current_submenu().keys()[self.previous_position()])

      if len(self.current_submenu()) > 1:
        l.set_cursor_position(1,2)
        l.write(self.current_submenu().keys()[self.next_position()])

    elif self.mode == 'adjust':
      self.current_value().redraw()

class MenuOption():
   def up(self):
     pass
   def down(self):
     pass
   def left(self):
     pass
   def right(self):
     pass
   def select(self):
     # Must return true to allow exit
     return True
   def redraw(self, lcd):
     pass

class Backlight(MenuOption):
   def __init__(self):
     self.hue = 0

   def right(self):
     self.hue += (1.0/360.0)
     if self.hue > 1:
       self.hue = 0
     b.hue(self.hue)

   def left(self):    
     self.hue -= (1.0/360.0)
     if self.hue < 0:
       self.hue = 1
     b.hue(self.hue)
   
   def redraw(self):
     l.set_cursor_position(1,0)
     l.write('Backlight')
     l.set_cursor_position(1,1)
     l.write('Hue: ' + str(int(self.hue*360)))

class Contrast(MenuOption):
   def __init__(self):
     self.contrast = 0

   def right(self):
     pass

   def left(self):
     pass
   
   def redraw(self):
     l.set_cursor_position(1,0)
     l.write('Contrast')
     l.set_cursor_position(1,1)
     print(self.contrast)
     l.write('Value: ' + str(self.contrast))

my_menu = {
  'Status': {
    'CPU': '',
    'Temp': ''
  },
  'Settings': {
    'Display': {
      'Contrast':Contrast(),
      'Backlight':Backlight()
    }
  }
}

b.rgb(255,255,255)
menu = Menu(my_menu)


@j.on(j.UP)
def handle_up(pin):
  menu.up()
  j.repeat(j.UP,menu.up,0.4)

@j.on(j.DOWN)
def handle_down(pin):
  menu.down()
  j.repeat(j.DOWN,menu.down,0.4)

@j.on(j.LEFT)
def handle_left(pin):
  menu.left()
  j.repeat(j.LEFT,menu.left,0.4,0.9)

@j.on(j.RIGHT)
def handle_right(pin):
  menu.right()
  j.repeat(j.RIGHT,menu.right,0.4,0.9)

@j.on(j.BUTTON)
def handle_button(pin):
  menu.select()

while 1:
  menu.redraw()
  time.sleep(0.05)

# Prevent the script exiting!
signal.pause()
