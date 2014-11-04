import os, math, psutil, subprocess
from dot3k.menu import MenuOption
import dot3k.backlight

class GraphCPU(MenuOption):
  """
  A simple "plug-in" example, this gets the CPU load
  and draws it to the LCD when active
  """
  def __init__(self):
    self.cpu_samples = [0,0,0,0,0]
    self.last = self.millis()
    MenuOption.__init__(self)
  
  def redraw(self, menu):
    now = self.millis()
    if now - self.last < 1000:
      return false

    self.cpu_samples.append(psutil.cpu_percent())
    self.cpu_samples.pop(0)
    self.cpu_avg = sum(self.cpu_samples) / len(self.cpu_samples)

    menu.write_row(0, 'CPU Load')
    menu.write_row(1, str(self.cpu_avg) + '%')
    menu.write_row(2, '#' * int(16*(self.cpu_avg/100.0)))
    
    dot3k.backlight.set_graph(self.cpu_avg/100.0)

  def left(self):
    dot3k.backlight.set_graph(0)
    return False

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
    proc = subprocess.Popen( ['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE )
    out, err = proc.communicate()
    gpu_temp = out.replace( 'temp=', '' ).replace( '\'C', '' )
    return float(gpu_temp)

  def redraw(self, menu):
    now = self.millis()
    if now - self.last < 1000:
      return false
    
    menu.write_row(0,'Temperature')
    menu.write_row(1,'CPU:' + str(self.get_cpu_temp()))
    menu.write_row(2,'GPU:' + str(self.get_gpu_temp()))
