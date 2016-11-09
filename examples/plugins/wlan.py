"""
Plugin for managing connections to wifi networks
"""

import subprocess
import threading
from sys import exit

try:
    import wifi
except ImportError:
    exit("This library requires the wifi module\nInstall with: sudo pip install wifi")

from dot3k.menu import MenuOption


class Wlan(MenuOption):
    def __init__(self, backlight=None, interface='wlan0'):
        self.items = []
        self.interface = interface

        self.wifi_pass = ""

        self.selected_item = 0

        self.connecting = False
        self.scanning = False
        self.has_error = False
        self.error_text = ""

        self.backlight = backlight

        MenuOption.__init__(self)

        self.is_setup = False

    def run_cmd(self, cmd):
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout = result.stdout.read().decode()
        stderr = result.stderr.read().decode()

        return (stdout, stderr)
        #print("stdout >> ", stdout)
        #print("stderr >> ", stderr)

    def begin(self):
        self.has_errror = False
        pass

    def setup(self, config):
        MenuOption.setup(self, config)

    def update_options(self):
        pass

    def cleanup(self):
        if self.backlight is not None:
            self.backlight.set_graph(0)
        self.is_setup = False
        self.has_error = False

    def select(self):
        return True

    def left(self):
        return False

    def right(self):
        self.connect()
        return True

    def up(self):
        if len(self.items):
            self.selected_item = (self.selected_item - 1) % len(self.items)
        return True

    def down(self):
        if len(self.items):
            self.selected_item = (self.selected_item + 1) % len(self.items)
        return True

    @property
    def current_network(self):
        if self.selected_item < len(self.items):
            return self.items[self.selected_item]

        return None

    def input_prompt(self):
        return 'Password:'

    def connect(self):
        network = self.current_network
        scheme = wifi.Scheme.find(self.interface, network.ssid)
        if scheme is None:
            self.request_input()
        else: 
            print("Connecting to {}".format(self.current_network.ssid))
            t = threading.Thread(None, self.perform_connection)
            t.daemon = True
            t.start()

    def initial_value(self):
        return ""

    def receive_input(self, value):
        self.wifi_pass = value

        print("Connecting to {}".format(self.current_network.ssid))
        print("Using Password: \"{}\"".format(self.wifi_pass))

        t = threading.Thread(None, self.perform_connection)
        t.daemon = True
        t.start()

    def perform_connection(self):
        self.connecting = True
        network = self.current_network
        scheme = wifi.Scheme.find(self.interface, network.ssid)
        new = False

 
        if scheme is None:
            new = True
            scheme = wifi.Scheme.for_cell(
                self.interface,
                network.ssid,
                network,
                passkey=self.wifi_pass)
            scheme.save()

        try:
            scheme.activate()
        except wifi.scheme.ConnectionError as e:
            self.error('Connection Failed!')
            print(e)
            self.connecting = False
            if new:
                scheme.delete()
            return

        self.connecting = False

    def clear_error(self):
        self.has_error = False
        self.error_text = ""

    def error(self, text):
        self.has_error = True
        self.error_text = text

    def scan(self):
        update = threading.Thread(None, self.do_scan)
        update.daemon = True
        update.start()

    def do_scan(self):
        if self.scanning:
            return False

        self.scanning = True

        result = self.run_cmd(["sudo ifup {}".format(self.interface)])

        if "Ignoring unknown interface" in result[1]:
            self.error("{} not found!".format(self.interface))
            self.scanning = False
            return

        try:
            result = wifi.scan.Cell.all(self.interface)
            self.items = result
            print(result)

        except wifi.scan.InterfaceError as e:
            self.error("Interface Error!")
            print(e)


        self.scanning = False

    def redraw(self, menu):
        if self.has_error:
            menu.write_option(row=0, text='Error:')
            menu.write_option(row=1, text=self.error_text)
            menu.clear_row(2)
            return True

        if self.scanning:
            menu.clear_row(0)
            menu.write_option(row=1, text='Scanning...')
            menu.clear_row(2)
            return True

        if self.connecting:
            menu.clear_row(0)
            menu.write_option(row=1, text='Connecting...')
            menu.clear_row(2)
            return True

        if not self.is_setup:
            menu.lcd.create_char(0, [0, 24, 30, 31, 30, 24, 0, 0])  # Play
            menu.lcd.create_char(1, [0, 27, 27, 27, 27, 27, 0, 0])  # Pause

            menu.lcd.create_char(4, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            menu.lcd.create_char(5, [0, 0, 10, 27, 10, 0, 0, 0])  # Left right arrow

            self.scan()

            self.is_setup = True

        if self.current_network is not None:
            item = self.current_network

            status = 'Open'
            if item.encrypted:
                status = 'Secured: ' + str(item.encryption_type)

            menu.write_option(row=0, text=str(item.ssid), scroll=True)
            menu.write_option(row=1, icon='', text=status, scroll=True)
            menu.write_option(row=2, text='CH' + str(item.channel) + ' ' + item.frequency)

            signal = float(item.quality.split('/')[0])
            noise = float(item.quality.split('/')[1])

            if self.backlight is not None:
                self.backlight.set_graph(signal / noise)

        else:
            menu.clear_row(0)
            menu.write_row(1, "No networks found!")
            menu.clear_row(2)
