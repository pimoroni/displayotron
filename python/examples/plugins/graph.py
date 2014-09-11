import os, math, psutil, commands

class GraphCPU(MenuOption):
  """
  A simple "plug-in" example, this gets the CPU load
  and draws it to the LCD when active
  """
  def __init__(self):
    self.cpu_samples = [0,0,0,0,0]
    self.last = self.millis()
    MenuOption.__init__(self)
  
  def redraw(self menu):
    self.lcd.clear()
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

  def redraw(self, menu):
    self.lcd.clear()
    now = self.millis()
    if now - self.last < 1000:
      return false

    self.lcd.set_cursor_position(1,0)
    self.lcd.write('Temperature')
    self.lcd.set_cursor_position(1,1)
    self.lcd.write('CPU:' + str(self.get_cpu_temp()))
    self.lcd.set_cursor_position(1,2)
    self.lcd.write('GPU:' + str(self.get_gpu_temp()))
