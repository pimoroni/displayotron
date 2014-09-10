from dot3k.menu import MenuOption
import subprocess, os
class Volume(MenuOption):

  def __init__(self):
    self.volume = None
    self.actual_volume = 0
    self.last_update = 0

  def setup(self, lcd, config):
    MenuOption.setup(self, lcd, config)
    self.volume = int(self.get_option('Sound','volume',80))
    self.set_volume()
    self.actual_volume = self.get_volume()

  def get_volume(self):
    actual_volume = subprocess.check_output("amixer get 'PCM' | awk '$0~/%/{print $4}' | tr -d '[]%'", shell=True)
    return actual_volume.strip()
   
  def set_volume(self):
    self.set_option('Sound','volume',self.volume)
    devnull = open(os.devnull, 'w')
    subprocess.call(['/usr/bin/amixer','sset',"'PCM'", str(self.volume) + '%'], stdout=devnull)
    self.actual_volume = self.get_volume()

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
    self.lcd.write('Volume: ')
    self.lcd.write(str(self.actual_volume))
    self.lcd.write('%')
    self.lcd.set_cursor_position(0,1)
    self.lcd.write('Target: ')
    self.lcd.write(str(self.volume))
    self.lcd.write('%')

    vol = '#' * int(16.0 * float(self.actual_volume)/100.0)
    self.lcd.set_cursor_position(0,2)
    self.lcd.write(vol)

    if self.millis() - self.last_update > 1000:
      self.actual_volume = self.get_volume()
      self.last_update = self.millis()
