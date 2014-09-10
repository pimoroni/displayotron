#!/usr/bin/env python

import dot3k.joystick as joystick
import dot3k.lcd as lcd
import dot3k.backlight as backlight
from dot3k.menu import Menu, Backlight, Contrast, MenuOption
import re, subprocess, socket, atexit, time, os, math

class DotVolume(MenuOption):

  def __init__(self):
    self.volume = None

  def setup(self, lcd, config):
    MenuOption.setup(self, lcd, config)
    self.volume = int(self.get_option('Sound','volume',80))
    self.set_volume()

  def set_volume(self):
    self.set_option('Sound','volume',self.volume)
    devnull = open(os.devnull, 'w')
    subprocess.call(['/usr/bin/amixer','sset',"'PCM'", str(self.volume) + '%'], stdout=devnull)

  def down(self):
    self.volume -= 1
    if self.volume < 0:
      self.volume = 0
    self.set_volume()

  def up(self):
    self.volume += 1
    if self.volume > 100:
      self.volume = 100
    self.set_volume()

  def redraw(self):
    lcd.write('Volume')
    lcd.set_cursor_position(0,1)
    lcd.write('PCM: ')
    lcd.write(str(self.volume))
    lcd.write('%')

    vol = '#' * int(16.0 * self.volume/100.0)
    lcd.set_cursor_position(0,2)
    lcd.write(vol)

class DotRadio(MenuOption):

  def __init__(self):
    MenuOption.__init__(self)
    self.selected_station = 0
    self.active_station = None
    self.pid = None
    self.socket = None
    self.current_stream = None
    self.last_update = 0
    atexit.register(self.kill)

  def setup(self, lcd, config):
    self.ready = False
    MenuOption.setup(self, lcd, config)
    if 'Radio Stations' in self.config.sections():
      self.stations = self.config.options('Radio Stations')
      self.ready = True
      self.start()

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
  
    if self.millis() - self.last_update > 500:
      self.get_current_stream()
      self.last_update = self.millis()

    if len(self.stations) > 2:
      self.draw_station(0, self.prev_station())

    self.draw_station(1, self.selected_station)

    if len(self.stations) > 1:
      self.draw_station(2, self.next_station())

  def draw_station(self, row, index):
    stream = self.config.get('Radio Stations',self.stations[index])
    title = stream.split(',')[0]
    stream = stream.split(',')[1]

    if self.selected_station ==  index:
      self.lcd.set_cursor_position(0, row)
      self.lcd.write(chr(252))

    #if self.active_station == index:
    if stream == self.current_stream:
      self.lcd.set_cursor_position(0, row)
      self.lcd.write('*')

    self.lcd.set_cursor_position(1, row)
    self.lcd.write(title)

  def kill(self):
    if self.pid != None:
      subprocess.call(['/bin/kill','-9',str(self.pid)])
      print('Killing VLC process with PID: ' + str(self.pid))

  def send(self, command):
    try:
      self.socket.send(command + "\n")
    except socket.error:
      print('Failed to send command to VLC')

  def get_current_stream(self):
     self.send("status")
     status = self.socket.recv(8192)
     result = re.search('input:\ (.*)\ ',status)
     if result != None:
       self.current_stream = result.group(1)
     else:
       self.current_stream = None
     return self.current_stream
  
  def start(self):
    if self.pid == None:
      return_value = subprocess.check_output(['./vlc.sh'])
      self.pid = int(return_value.split('\n')[0])    

      print('VLC started with PID: ' + str(self.pid))  
      
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      for attempt in range(10):
        try:
          print("Attempting to connect to VLC")
          self.socket.connect(("127.0.0.1",9393))
          break
        except socket.error:
          time.sleep(0.5)
      try:
        self.socket.recv(0)
      except socket.error:
        exit("Unable to connect to VLC")
  
  def right(self):
    #if self.active_station == self.selected_station:
         #self.kill()

    stream = self.config.get(
	'Radio Stations',
	self.stations[self.selected_station]
	)

    if ',' in stream:
      stream = stream.split(',')[1]
 
    if stream == self.get_current_stream():
      print('Skipping play, sending play/pause toggle')
      #devnull = open(os.devnull, 'w')
      #subprocess.call('/bin/echo pause | /bin/netcat 127.0.0.1 9393', shell=True, stdout=devnull)
      self.send("pause")
      return False

    #subprocess.call('/bin/echo "add ' + stream + '" | /bin/netcat 127.0.0.1 9393', shell=True, stdout=open(os.devnull,'w'))
    self.send("add " + stream)
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
    'Volume':DotVolume(),
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
