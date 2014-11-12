import os, math, psutil, subprocess
import socket, fcntl, struct
from dot3k.menu import MenuOption
import dot3k.backlight

class IPAddress(MenuOption):
  """
  A plugin which gets the IP address for wlan0
  and eth0 and displays them on the screen.
  """

  def get_addr(self, ifname):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
      )[20:24])
    except IOError:
      return 'Not Found!'

  def __init__(self):
    self.mode = 0
    self.wlan0 = self.get_addr('wlan0')
    self.eth0 = self.get_addr('eth0')
    self.is_setup = False
    MenuOption.__init__(self)

  def redraw(self, menu):
    if not self.is_setup:
      menu.lcd.create_char(0,[0,4,14,0,0,14,4,0]) # Up down arrow
      self.is_setup = True

    menu.write_row(0, 'IP Address')
    if self.mode == 0:
      menu.write_row(1, chr(0) + ' Wired:')
      menu.write_row(2, self.eth0)
    else:
      menu.write_row(1, chr(0) + ' Wireless:')
      menu.write_row(2, self.wlan0)

  def down(self):
    self.mode = 1

  def up(self):
    self.mode = 0

  def left(self):
    return False

  def cleanup(self):
    self.is_setup = False

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
