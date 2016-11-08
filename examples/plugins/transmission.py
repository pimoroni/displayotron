"""
Plugin for Transmission torrent client.
Requires Transmission install: sudo apt-get install transmission-daemon

You'll probably also want the command-line client: transmission-cli so you can add and manage torrents.

Auth isn't supported at the moment, so you'll have to:

sudo service transmission-daemon stop
sudo vim /etc/transmission-daemon/settings.json

Find the setting rpc-authentication-required and make sure it's set to false.

Support for pausing/resuming torrents is planned.
"""

import threading

import dot3k.backlight
from dot3k.menu import MenuOption


class Transmission(MenuOption):
    def __init__(self):
        self.host = 'localhost'
        self.port = 9091
        self.client = None

        self.items = []

        self.selected_item = 0

        self.last_update = 0
        self.updating = False

        self.last_event = 0

        MenuOption.__init__(self)

        self.is_setup = False

        self.auto_cycle_timeout = 10000  # Start auto advancing after n/1000 sec of no user interaction
        self.auto_cycle_speed = 10000  # Time between advances

    def begin(self):
        self.reset_timeout()
        self.update(True)

    def connect(self):
        try:
            import transmissionrpc
        except ImportError:
            print("Transmission requires transmissionrpc")
            print("please: sudo pip install transmissionrpc")
            return
        self.client = transmissionrpc.Client(self.host, self.port)

    def reset_timeout(self):
        self.last_event = self.millis()

    def setup(self, config):
        MenuOption.setup(self, config)
        self.load_options()
        self.connect()

    def update_options(self):
        pass

    def load_options(self):
        self.host = self.get_option('Transmission', 'host', self.host)
        self.port = int(self.get_option('Transmission', 'port', self.port))

    def cleanup(self):
        self.is_setup = False

    def select(self):
        self.add_new()
        return False

    def left(self):
        self.reset_timeout()
        return False

    def right(self):
        self.reset_timeout()
        return True

    def up(self):
        self.reset_timeout()
        self.selected_item = (self.selected_item - 1) % len(self.items)
        return True

    def down(self):
        self.reset_timeout()
        self.selected_item = (self.selected_item + 1) % len(self.items)
        return True

    def update(self, force=False):
        # Update only once every 30 seconds
        if self.millis() - self.last_update < 1000 * 30 and not force:
            return False

        self.last_update = self.millis()

        update = threading.Thread(None, self.do_update)
        update.daemon = True
        update.start()

    def do_update(self):
        if self.updating or self.client == None:
            return False

        self.updating = True

        torrents = self.client.get_torrents()

        for torrent in torrents:
            size = 0
            for idx in torrent.files():
                size += torrent.files()[idx]['size']
            size = round(size / 1000.0 / 1000.0 * 10) / 10
            torrent.size = size

        if self.selected_item > len(torrents):
            self.selected_item = 0

        self.reset_timeout()

        self.items = torrents

        self.updating = False

    def redraw(self, menu):
        self.update()

        if self.millis() - self.last_event >= self.auto_cycle_timeout and len(self.items):
            self.selected_item = ((
                                  self.millis() - self.last_event - self.auto_cycle_timeout) / self.auto_cycle_speed) % len(
                self.items)

        if not self.is_setup:
            menu.lcd.create_char(0, [0, 24, 30, 31, 30, 24, 0, 0])  # Play
            menu.lcd.create_char(1, [0, 27, 27, 27, 27, 27, 0, 0])  # Pause

            menu.lcd.create_char(4, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            menu.lcd.create_char(5, [0, 0, 10, 27, 10, 0, 0, 0])  # Left right arrow

            self.is_setup = True

        if len(self.items):
            item = self.items[self.selected_item]

            done = (item.size / 100.0) * item.progress

            menu.write_option(row=0, icon=(chr(1) if item.status == 'stopped' else chr(0)), text=item.name, scroll=True)
            menu.write_option(row=1, icon='', margin=0, text=str(done) + 'MB / ' + str(item.size) + 'MB', scroll=True)
            menu.write_row(2, '')

            dot3k.backlight.set_graph(item.progress / 100.0)

        else:
            menu.write_row(0, "No Torrents!")
            menu.clear_row(1)
            menu.clear_row(2)
