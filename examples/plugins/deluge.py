"""
Plugin for Deluge torrent client.
Requires deluge install: sudo apt-get install deluged deluged-console
"""

import subprocess
import threading

import dot3k.backlight
from dot3k.menu import MenuOption


class Deluge(MenuOption):
    def __init__(self):

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

    def reset_timeout(self):
        self.last_event = self.millis()

    def setup(self, config):
        MenuOption.setup(self, config)
        self.load_options()

    def update_options(self):
        pass

    def load_options(self):
        pass

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
        if self.updating:
            return False

        self.updating = True

        torrents = subprocess.check_output('su pi -c "deluge-console info"', shell=True)
        torrents = torrents.strip().split('\n \n')
        torrents = map(lambda x: dict(y.split(': ', 1) for y in x),
                       map(lambda x: x.replace(' Active:', '\nActive:').replace(' Ratio:', '\nRatio:').split('\n'),
                           torrents))

        for torrent in torrents:
            if 'Progress' in torrent.keys():
                torrent['Progress'] = float(torrent['Progress'].split('%')[0])
            else:
                torrent['Progress'] = 100.0

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

            menu.write_option(row=0, icon=(chr(1) if item['State'] == 'Paused' else chr(0)), text=item['Name'],
                              scroll=True)
            menu.write_option(row=1, icon='', margin=0, text=item['Size'], scroll=True)
            menu.write_row(2, item['Active'])

            dot3k.backlight.set_graph(item['Progress'] / 100.0)

        else:
            menu.write_row(0, "No Torrents!")
            menu.clear_row(1)
            menu.clear_row(2)
