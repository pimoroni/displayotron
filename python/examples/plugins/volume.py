from dot3k.menu import MenuOption
import subprocess, os
class Volume(MenuOption):

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