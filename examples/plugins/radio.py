import atexit
import re
import socket
import subprocess
import time
from sys import version_info

from dot3k.menu import MenuOption


class Radio(MenuOption):
    def __init__(self):
        MenuOption.__init__(self)
        self.ready = False
        self.stations = None
        self.selected_station = 0
        self.selected_option = 0
        self.pid = None
        self.socket = None
        self.current_stream = None
        self.current_state = None
        # Keep track of whether we've started a VLC instance
        self.started_vlc_instance = False
        self.last_update = 0
        self.mode = 'main'
        atexit.register(self.kill)
        self.icons = {
            'play': [0, 24, 30, 31, 30, 24, 0, 0],
            'pause': [0, 27, 27, 27, 27, 27, 0, 0],
            'stop': [0, 31, 31, 31, 31, 31, 0, 0]
        }

    def setup(self, config):
        self.ready = False
        MenuOption.setup(self, config)
        if 'Radio Stations' in self.config.sections():
            self.stations = self.config.options('Radio Stations')
            self.ready = True
            self.start()

    def prev_station(self):
        station = self.selected_station - 1
        if station < 0:
            station = len(self.stations) - 1
        return station

    def next_station(self):
        station = self.selected_station + 1
        if station >= len(self.stations):
            station = 0
        return station

    def next_option(self):
        self.selected_option += 1
        self.selected_option %= 3

    def prev_option(self):
        self.selected_option -= 1
        self.selected_option %= 3

    def down(self):
        if self.mode == 'main':
            self.next_option()
        else:
            self.selected_station = self.next_station()

    def up(self):
        if self.mode == 'main':
            self.prev_option()
        else:
            self.selected_station = self.prev_station()

    def right(self):
        if self.mode == 'main':
            if self.selected_option == 0:
                self.mode = 'list'
            elif self.selected_option == 1:
                self.send('pause')
            elif self.selected_option == 2 and self.current_state == 'playing':
                self.send('stop')
            elif self.selected_option == 2 and self.current_state == 'stopped':
                self.send('play')
        else:
            self.play_selected_station()

    def left(self):
        if self.mode == 'main':
            return False
        else:
            self.mode = 'main'
            return True

    def play_selected_station(self):
        stream = self.config.get(
            'Radio Stations',
            self.stations[self.selected_station]
        )

        if ',' in stream:
            stream = stream.split(',')[1]

        if stream == self.get_current_stream():
            print('Skipping play, sending play/pause toggle')
            self.send("pause")
            return False

        self.send("add " + stream)

    def redraw(self, menu):
        if self.millis() - self.last_update > 500:
            self.get_current_stream()
            self.last_update = self.millis()

        if self.mode == 'list':
            self.redraw_stations(menu)
        elif self.mode == 'main':
            self.redraw_main(menu)

    def redraw_main(self, menu):
        # Row, Text, Icon, Left Margin
        menu.write_option(0, 'Stations', chr(252) if self.selected_option == 0 else ' ', 1)
        menu.write_option(1, 'Pause' if self.current_state != 'paused' else 'Resume',
                          chr(252) if self.selected_option == 1 else ' ', 1)
        menu.write_option(2, 'Stop' if self.current_state != 'stopped' else 'Play',
                          chr(252) if self.selected_option == 2 else ' ', 1)

    def redraw_stations(self, menu):
        if not self.ready:
            menu.clear_row(0)
            menu.write_row(1, 'No stations found!')
            menu.clear_row(2)
            return False

        if len(self.stations) > 2:
            self.draw_station(menu, 0, self.prev_station())

        self.draw_station(menu, 1, self.selected_station)

        if len(self.stations) > 1:
            self.draw_station(menu, 2, self.next_station())

    def draw_station(self, menu, row, index):
        stream = self.config.get('Radio Stations', self.stations[index])
        title = stream.split(',')[0]
        stream = stream.split(',')[1]

        icon = ' '

        if self.selected_station == index:
            icon = chr(252)

        if stream == self.current_stream:
            if self.current_state == 'paused':
                menu.lcd.create_char(0, self.icons['pause'])
                icon = chr(0)
            elif self.current_state == 'playing':
                menu.lcd.create_char(0, self.icons['play'])
                icon = chr(0)
            else:
                menu.lcd.create_char(0, self.icons['stop'])
                icon = chr(0)

        menu.write_option(row, title, icon)

    def kill(self):
        if self.pid is not None and self.started_vlc_instance:
            subprocess.call(['/bin/kill', '-9', str(self.pid)])
            print('Killing VLC process with PID: ' + str(self.pid))

    def send(self, command):
        try:
            if version_info[0] >= 3:
                self.socket.send((command + "\n").encode('utf-8'))
            else:
                self.socket.send(command + "\n")
        except socket.error:
            print('Failed to send command to VLC')

    def get_current_stream(self):
        self.send("status")
        status = self.socket.recv(8192)
        if version_info[0] >= 3:
            status = status.decode('utf-8')
        result = re.search('input:\ (.*)\ ', status)
        state = re.search('state\ (.*)\ ', status)
        if state is not None:
            self.current_state = state.group(1)
        if result is not None:
            self.current_stream = result.group(1)
        else:
            self.current_stream = None
        return self.current_stream

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for attempt in range(10):
            try:
                print("Attempting to connect to VLC")
                self.socket.connect(("127.0.0.1", 9393))
                print("Connection successful!")
                return True
            except socket.error:
                time.sleep(1)
        try:
            self.socket.recv(0)
        except socket.error:
            return False

    def start(self):
        if self.pid is None:
            try:
                return_value = subprocess.check_output(['pidof', 'vlc'])
                if version_info[0] >= 3:
                    self.pid = int(return_value.decode('utf-8').split(' ')[0])
                else:
                    self.pid = int(return_value.decode('utf-8').split(' ')[0])
                print('Found VLC with PID: ' + str(self.pid))
                if self.connect():
                    return True
            except subprocess.CalledProcessError:
                pass

            try:
                return_value = subprocess.check_output(['./vlc.sh'])
                pids = return_value.decode('utf-8').split('\n')[0]
                self.pid = int(pids.split(' ')[0])
                self.started_vlc_instance = True
                print('VLC started with PID: ' + str(self.pid))
            except subprocess.CalledProcessError:
                print('You must have VLC installed to use Dot3k Radio')
                print('Try: sudo apt-get install vlc')
                exit()

        if not self.connect():
            exit("Unable to connect to VLC")
