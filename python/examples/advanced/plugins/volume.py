from dot3k.menu import MenuOption
import dot3k.backlight
import subprocess, os, sys
class Volume(MenuOption):

  def __init__(self):
    MenuOption.__init__(self)
    self.volume = None
    self.actual_volume = 0
    self.last_update = 0

  def setup(self, config):
    MenuOption.setup(self, config)
    self.volume = int(self.get_option('Sound','volume',80))
    self.set_volume()
    self.actual_volume = self.get_volume()
  
  def left(self):
    dot3k.backlight.set_graph(0)
    return False

  def get_volume(self):
    actual_volume = subprocess.check_output("amixer get 'PCM' | awk '$0~/%/{print $4}' | tr -d '[]%'", shell=True)
    if sys.version_info[0] >= 3:
        return actual_volume.strip().decode('utf-8')
    else:
        return actual_volume.strip()
   
  def set_volume(self):
    self.set_option('Sound','volume',str(self.volume))
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

  def redraw(self, menu):
    menu.write_row(0,'Volume: ' + str(self.actual_volume))
    menu.write_row(1,'Target: ' + str(self.volume))
    menu.write_row(2,'#' * int(16.0 * float(self.actual_volume)/100.0))

    if self.millis() - self.last_update > 1000:
      self.actual_volume = self.get_volume()
      self.last_update = self.millis()

      dot3k.backlight.set_graph(float(self.actual_volume)/100.0)


