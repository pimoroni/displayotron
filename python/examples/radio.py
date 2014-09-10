#!/usr/bin/env python

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu, Backlight, Contrast, MenuOption
import subprocess, atexit, time, os, math, psutil, commands

class DotRadio(MenuOption):

  def __init__(self):
    MenuOption.__init__(self)
    self.selected_station = 0
    self.active_station = None
    self.pid = None
    atexit.register(self.kill)

  def setup(self, lcd, config):
    self.ready = False
    MenuOption.setup(self, lcd, config)
    if 'Radio Stations' in self.config.sections():
      self.stations = self.config.options('Radio Stations')
      self.ready = True

  def prev_station(self):
    station = self.selected_station-1
    if station < 0:
      station = len(self.stations) - 1
    return station

  def next_station(self):
    station = self.selected_station+1
    if station >= len(self.stations):
      station = 0
    return station

  def down(self):
    self.selected_station = self.next_station()

  def up(self):
    self.selected_station = self.prev_station()

  def redraw(self):
    if not self.ready:
      lcd.write('No stations found!')
      return False 

    if len(self.stations) > 2:
      self.draw_station(0, self.prev_station())

    self.draw_station(1, self.selected_station)

    if len(self.stations) > 1:
      self.draw_station(2, self.next_station())

  def draw_station(self, row, index):
    if self.selected_station ==  index:
      self.lcd.set_cursor_position(0, row)
      self.lcd.write(chr(252))

    if self.active_station == index:
      self.lcd.set_cursor_position(0, row)
      self.lcd.write('*')

    self.lcd.set_cursor_position(1, row)
    self.lcd.write(self.stations[index])

  def kill(self):
    if self.pid != None:
      subprocess.call(['/bin/kill','-9',str(self.pid)])
      print('Killing VLC process with PID: ' + str(self.pid))

  def right(self):
    if self.active_station == self.selected_station:
      print('Skipping play, already playing')
      return False

    self.kill()
 
    stream = self.config.get(
	'Radio Stations',
	self.stations[self.selected_station]
	)

    return_value = subprocess.check_output(['./vlc.sh', stream, "-I", "dummy"])
    self.pid = int(return_value.split('\n')[0])    

    print('VLC started with PID: ' + str(self.pid))  
  
    self.active_station = self.selected_station

"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""
menu = Menu({
    'Radio':DotRadio(),
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
