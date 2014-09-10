#!/usr/bin/env python

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu, Backlight, Contrast, MenuOption
import time, os, math, psutil, commands

class SpaceInvader(MenuOption):
  """
  A silly example "plug-in" showing an
  animated space invader.
  """

  def __init__(self):
    self.start = self.millis()
    self.invader = [
      [14,31,21,31,9,18,9,18],
      [14,31,21,31,18,9,18,9]
    ]
    MenuOption.__init__(self)

  def redraw(self):
    now = self.millis()

    x = int((self.start-now)/200 % 16)
    self.lcd.create_char(0, self.invader[int((self.start-now)/400 % 2)])

    self.lcd.set_cursor_position(0,0)
    self.lcd.write('Space Invader!')
    self.lcd.set_cursor_position(x,1)
    self.lcd.write(chr(0))

class GraphCPU(MenuOption):
  """
  A simple "plug-in" example, this gets the CPU load
  and draws it to the LCD when active
  """
  def __init__(self):
    self.cpu_samples = [0,0,0,0,0]
    self.last = self.millis()
    MenuOption.__init__(self)
  
  def redraw(self):
    now = self.millis()
    if now - self.last < 1000:
      return false

    self.cpu_samples.append(psutil.cpu_percent() / 100.0)
    self.cpu_samples.pop(0)
    self.cpu_avg = sum(self.cpu_samples) / len(self.cpu_samples)

    self.lcd.set_cursor_position(1,0)
    self.lcd.write('CPU Load')
    self.lcd.set_cursor_position(1,1)
    self.lcd.write(str(self.cpu_avg) + '%')

class GraphTemp(MenuOption):
  """
  A simple "plug-in" example, this gets the Temperature
  and draws it to the LCD when active
  """
  def __init__(self):
    self.last = self.millis()
    MenuOption.__init__(self)

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

    self.lcd.set_cursor_position(1,0)
    self.lcd.write('Temperature')
    self.lcd.set_cursor_position(1,1)
    self.lcd.write('CPU:' + str(self.get_cpu_temp()))
    self.lcd.set_cursor_position(1,2)
    self.lcd.write('GPU:' + str(self.get_gpu_temp()))


"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""
menu = Menu({
    'Space Invader':SpaceInvader(),
    'Status': {
      'CPU':GraphCPU(),
      'Temp':GraphTemp()
    },
    'Settings': {
      'Display': {
        'Contrast':Contrast(),
        'Backlight':Backlight(backlight)
      }
    }
  },
  lcd)

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.joystick
"""
@joystick.on(joystick.UP)
def handle_up(pin):
  menu.up()
  joystick.repeat(joystick.UP,menu.up,0.4,0.9)

@joystick.on(joystick.DOWN)
def handle_down(pin):
  menu.down()
  joystick.repeat(joystick.DOWN,menu.down,0.4,0.9)

@joystick.on(joystick.LEFT)
def handle_left(pin):
  menu.left()
  joystick.repeat(joystick.LEFT,menu.left,0.4,0.9)

@joystick.on(joystick.RIGHT)
def handle_right(pin):
  menu.right()
  joystick.repeat(joystick.RIGHT,menu.right,0.4,0.9)

@joystick.on(joystick.BUTTON)
def handle_button(pin):
  menu.select()

while 1:
  menu.redraw()
  time.sleep(0.05)