from dot3k.menu import MenuOption
import re, subprocess, socket, atexit, time, os, math
class Radio(MenuOption):

  def __init__(self):
    MenuOption.__init__(self)
    self.selected_station = 0
    self.active_station = None
    self.pid = None
    self.socket = None
    self.current_stream = None
    self.current_state = None
    self.last_update = 0
    atexit.register(self.kill)
    self.icons = {
      'play': [0,24,30,31,30,24,0,0],
      'pause':[0,27,27,27,27,27,0,0],
      'stop': [0,31,31,31,31,31,0,0]
    }

  def setup(self, config):
    self.ready = False
    MenuOption.setup(self, config)
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

  def redraw(self, menu):
    if not self.ready:
      menu.clear_row(0)
      menu.write_row(1,'No stations found!')
      menu.clear_row(2)
      return False 
  
    if self.millis() - self.last_update > 500:
      self.get_current_stream()
      self.last_update = self.millis()

    if len(self.stations) > 2:
      self.draw_station(menu, 0, self.prev_station())

    self.draw_station(menu, 1, self.selected_station)

    if len(self.stations) > 1:
      self.draw_station(menu, 2, self.next_station())

  def draw_station(self, menu, row, index):
    stream = self.config.get('Radio Stations',self.stations[index])
    title = stream.split(',')[0]
    stream = stream.split(',')[1]

    icon = ' '

    if self.selected_station == index:
      icon = chr(252)

    if stream == self.current_stream:
      if self.current_state == 'paused':
        menu.lcd.create_char(0,self.icons['pause'])
        icon = chr(0)
      elif self.current_state == 'playing':
        menu.lcd.create_char(0,self.icons['play'])
        icon = chr(0)
      else:
        menu.lcd.create_char(0,self.icons['stop'])
        icon = chr(0)
    
    menu.write_option(row, title, icon)

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
     state = re.search('state\ (.*)\ ',status)
     if state != None:
       self.current_state = state.group(1)
     if result != None:
       self.current_stream = result.group(1)
     else:
       self.current_stream = None
     return self.current_stream
  
  def start(self):
    if self.pid == None:
      try:
        return_value = subprocess.check_output(['./vlc.sh'])
        pids = return_value.split('\n')[0]
        self.pid = int(pids.split(' ')[0])

        print('VLC started with PID: ' + str(self.pid))  
      except subprocess.CalledProcessError:
        print('You must have VLC installed to use Dot3k Radio')
        print('Try: sudo apt-get install vlc')
        exit()
      
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
