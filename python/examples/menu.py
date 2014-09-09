#!/usr/bin/env python

import dot3k.joystick as j
import dot3k.lcd as l
import dot3k.backlight as b
import signal, time, ConfigParser, os

config = ConfigParser.ConfigParser()
config.read(['dot3k.cfg', os.path.expanduser('~/.dot3k.cfg')])

class Menu():

  def __init__(self, structure):
    self.list_location = []
    self.current_position = 0
    self.mode = 'navigate'
    self.menu_options = structure
    #self.redraw()
    #l.create_char(0,[16,24,28,30,30,28,24,16])
    
    @j.on(j.UP)
    def handle_up(pin):
      self.up()
      j.repeat(j.UP,self.up,0.4,0.9)

    @j.on(j.DOWN)
    def handle_down(pin):
      self.down()
      j.repeat(j.DOWN,self.down,0.4,0.9)

    @j.on(j.LEFT)
    def handle_left(pin):
      self.left()
      j.repeat(j.LEFT,self.left,0.4,0.9)

    @j.on(j.RIGHT)
    def handle_right(pin):
      self.right()
      j.repeat(j.RIGHT,self.right,0.4,0.9)

    @j.on(j.BUTTON)
    def handle_button(pin):
      self.select()

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
    elif callable(self.current_submenu()[self.current_key()]):
      self.current_submenu()[self.current_key()]()

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
    elif self.mode == 'adjust':
      self.current_value().up()
    #self.redraw()

  def down(self):
    if self.mode == 'navigate':
      self.next_option()
    elif self.mode == 'adjust':
      self.current_value().down()
    #self.redraw()

  def left(self):
    if self.mode == 'navigate':
      self.exit_option()
    elif self.mode == 'adjust':
      if not self.current_value().left():
        self.mode = 'navigate'
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
   def millis(self):
     return int(round(time.time() * 1000))
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

import colorsys
class Backlight(MenuOption):
   def __init__(self):
     self.hue = 0
     self.sat = 100
     self.val = 100
     self.mode = 0
     self.modes = ['h','s','v','r','g','b']
     self.from_hue()

   def from_hue(self):
     rgb = colorsys.hsv_to_rgb(self.hue,self.sat/100.0,self.val/100.0)
     self.r = int(255*rgb[0])
     self.g = int(255*rgb[1])
     self.b = int(255*rgb[2])
 
   def from_rgb(self):
     self.hue = colorsys.rgb_to_hsv(self.r/255.0,self.g/255.0,self.b/255.0)[0]

   def update_bl(self):
     if not 'Backlight' in config.sections():
       config.add_section('Backlight')
     config.set('Backlight','r',str(self.r))
     config.set('Backlight','g',str(self.g))
     config.set('Backlight','b',str(self.b))
     config.set('Backlight','h',str(int(self.hue*359)))
     config.set('Backlight','s',str(self.sat))
     config.set('Backlight','v',str(self.val))
     b.rgb(self.r,self.g,self.b)

   def right(self):
     self.mode+=1
     if self.mode >= len(self.modes):
       self.mode = 0
     return True

   def left(self):
     self.mode-=1
     if self.mode < 0:
       self.mode = len(self.modes)-1
     return True

   def up(self):
     if self.mode == 0:
       self.hue += (1.0/359.0)
       if self.hue > 1:
         self.hue = 0
       self.from_hue()

     elif self.mode == 1: # sat
       self.sat += 1
       if self.sat > 100:
         self.sat = 0
         self.from_hue()
 
     elif self.mode == 2: # val
       self.val += 1
       if self.val > 100:
         self.val = 0
       self.from_hue()

     else: # rgb
       if self.mode == 3: #r
         self.r += 1
         if self.r > 255:
           self.r = 0
       elif self.mode == 4: #g
         self.g += 1
         if self.g > 255:
           self.g = 0
       elif self.mode == 5: #b
         self.b += 1
         if self.b > 255:
           self.b = 0
   
       self.from_rgb()
       
     self.update_bl()
     return True

   def down(self):    
     if self.mode == 0:
       self.hue -= (1.0/359.0)
       if self.hue < 0:
         self.hue = 1
       self.from_hue()

     elif self.mode == 1: # sat
       self.sat -= 1
       if self.sat < 0:
         self.sat = 100
       self.from_hue()

     elif self.mode == 2: #val
       self.val -= 1
       if self.val < 0:
         self.val = 100
       self.from_hue()

     else: # rgb
       if self.mode == 3: #r
         self.r -= 1
         if self.r < 0:
           self.r = 255
       elif self.mode == 4: #g
         self.g -= 1
         if self.g < 0:
           self.g = 255
       elif self.mode == 5: #b
         self.b -= 1
         if self.b < 0:
           self.b = 255

       self.from_rgb()

     self.update_bl()
     return True
   
   def redraw(self):
     l.set_cursor_position(0,0)
     l.write('Backlight')
     l.set_cursor_position(0,1)
     l.write('HSV: ' + str(int(self.hue*359)).zfill(3) + ' ' + str(self.sat).zfill(3) + ' ' + str(self.val).zfill(3) )
     l.set_cursor_position(0,2) 

     l.write('RGB: ' + str(self.r).zfill(3) + ' ' + str(self.g).zfill(3) + ' ' + str(self.b).zfill(3))
     if self.mode == 0: # hue
       l.set_cursor_position(4,1)
     elif self.mode == 1: # sat
       l.set_cursor_position(8,1)
     elif self.mode == 2: # val
       l.set_cursor_position(12,1)
     elif self.mode == 3: # r
       l.set_cursor_position(4,2)
     elif self.mode == 4: # g
       l.set_cursor_position(8,2)
     elif self.mode == 5: # b
       l.set_cursor_position(12,2)
     l.write(chr(252))
 
class Contrast(MenuOption):
   def __init__(self):
     self.contrast = 30

   def right(self):
     self.contrast+=1
     if self.contrast > 63:
       self.contrast = 0
     l.set_contrast(self.contrast)
     return True

   def left(self):
     self.contrast-=1
     if self.contrast < 0:
       self.contrast = 63
     l.set_contrast(self.contrast)
     return True
   
   def redraw(self):
     l.set_cursor_position(1,0)
     l.write('Contrast')
     l.set_cursor_position(1,1)
     l.write('Value: ' + str(self.contrast))

import math, psutil 
class GraphCPU(MenuOption):
  def __init__(self):
    self.cpu_samples = [0,0,0,0,0]
    self.last = self.millis()
  
  def redraw(self):
    now = self.millis()
    if now - self.last < 1000:
      return false

    self.cpu_samples.append(psutil.cpu_percent() / 100.0)
    self.cpu_samples.pop(0)
    self.cpu_avg = sum(self.cpu_samples) / len(self.cpu_samples)
    l.set_cursor_position(1,0)
    l.write('CPU Load')
    l.set_cursor_position(1,1)
    l.write(str(self.cpu_avg) + '%')

import commands
class GraphTemp(MenuOption):
  def __init__(self):
    self.last = self.millis()

  def get_cpu_temp(self):
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000

  def get_gpu_temp(self):
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    return float(gpu_temp)

  def redraw(self):
    now = self.millis()
    if now - self.last < 1000:
      return false

    l.set_cursor_position(1,0)
    l.write('Temperature')
    l.set_cursor_position(1,1)
    l.write('CPU:' + str(self.get_cpu_temp()))
    l.set_cursor_position(1,2)
    l.write('GPU:' + str(self.get_gpu_temp()))

def save_settings():
  print('Config saved to dot3k.cfg')
  with open('dot3k.cfg', 'wb') as configfile:
    config.write(configfile)


"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""
my_menu = {
  'Status': {
    'CPU':GraphCPU(),
    'Temp':GraphTemp()
  },
  'Settings': {
    'Display': {
      'Contrast':Contrast(),
      'Backlight':Backlight()
    },
    'Save':save_settings
  }
}

l.set_contrast(40)
b.rgb(255,255,255)
menu = Menu(my_menu)

while 1:
  menu.redraw()
  time.sleep(0.05)
 
# Prevent the script exiting!
signal.pause()
