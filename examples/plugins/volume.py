import os
import subprocess
import time
from sys import version_info

import dot3k.backlight
from dot3k.menu import MenuIcon
from dot3k.menu import MenuOption


MODE_AUTO = 0
MODE_HEADPHONES = 1
MODE_HDMI = 2

EDIT_VOLUME = 0
EDIT_OUTPUT = 1
EDIT_EXIT = 2


class Volume(MenuOption):
    def __init__(self, backlight=None):
        MenuOption.__init__(self)
        self.output_options = {
            MODE_AUTO: 'Auto',
            MODE_HEADPHONES: 'Headphones',
            MODE_HDMI: 'HDMI'
        }
        self.output_mode = -1
        self.volume = None
        self.backlight = backlight
        self.actual_volume = 0
        self.last_update = 0
        self.edit_mode = EDIT_VOLUME
        self._icons_setup = False

    def setup(self, config):
        MenuOption.setup(self, config)
        self.edit_mode = EDIT_VOLUME
        self.volume = int(self.get_option('Sound', 'volume', 80))
        self.set_volume()
        self.actual_volume = self.get_volume()
        self.output_mode = self.get_mode()

    def setup_icons(self, menu):
        menu.lcd.create_char(0, MenuIcon.arrow_left_right)  # Left/right arrow
        menu.lcd.create_char(1, MenuIcon.arrow_up_down)  # Up/Down arrow
        menu.lcd.create_char(2, MenuIcon.back)
        menu.lcd.create_char(3, MenuIcon.arrow_left)
        menu.lcd.create_char(4, MenuIcon.bar_left)
        menu.lcd.create_char(5, MenuIcon.bar_right)
        menu.lcd.create_char(6, MenuIcon.bar_full)
        menu.lcd.create_char(7, MenuIcon.bar_empty)
        self._icons_setup = True

    def cleanup(self):
        self._icons_setup = False
        dot3k.backlight.set_graph(0)

    def down(self):
        self.edit_mode += 1
        self.edit_mode %= 3

    def left(self):
        if self.backlight is not None:
            self.backlight.set_graph(0)
        return False

    def up(self):
        self.edit_mode -= 1
        self.edit_mode %= 3
        return True

    def get_mode(self):
        mode = subprocess.check_output("amixer cget numid=3 | grep ': values='", shell=True)
        mode = mode.decode().split('=')[1]
        return int(mode)

    def set_mode(self):
        subprocess.check_output("amixer cset numid=3 " + str(self.output_mode), shell=True)

    def get_volume(self):
        actual_volume = subprocess.check_output("amixer get 'PCM' | awk '$0~/%/{print $4}' | tr -d '[]%'", shell=True)
        if version_info[0] >= 3:
            return actual_volume.strip().decode('utf-8')
        else:
            return actual_volume.strip()

    def cleanup(self):
        if self.backlight is not None:
            self.backlight.set_graph(0)

    def set_volume(self):
        self.set_option('Sound', 'volume', str(self.volume))
        devnull = open(os.devnull, 'w')
        subprocess.call(['/usr/bin/amixer', 'sset', "'PCM'", str(self.volume) + '%'], stdout=devnull)
        self.actual_volume = self.get_volume()
        time.sleep(0.01)

    def left(self):
        if self.edit_mode == EDIT_VOLUME:
            self.volume -= 1
            if self.volume < 0:
                self.volume = 0
            self.set_volume()
        elif self.edit_mode == EDIT_OUTPUT:
            self.output_mode += 1
            self.output_mode %= 3
            self.set_mode()
        elif self.edit_mode == EDIT_EXIT:
            return False
        return True

    def right(self):
        if self.edit_mode == EDIT_VOLUME:
            self.volume += 1
            if self.volume > 100:
                self.volume = 100
            self.set_volume()
        elif self.edit_mode == EDIT_OUTPUT:
            self.output_mode -= 1
            self.output_mode %= 3
            self.set_mode()

    def redraw(self, menu):
        if not self._icons_setup:
            self.setup_icons(menu)

        if self.edit_mode == EDIT_VOLUME:
            vol_bar = int(14.0 * float(self.actual_volume) / 100.0)

            menu.write_row(0, chr(1) + ' Change Volume')
            menu.write_row(1, ' ' + chr(0) + 'Volume: ' + str(self.volume))
            menu.write_row(2, chr(4) + (chr(6) * vol_bar) + (chr(7) * (14 - vol_bar)) + chr(5))
        elif self.edit_mode == EDIT_OUTPUT:
            menu.write_row(0, chr(1) + ' Audio Output')
            menu.write_row(1, ' ' + chr(0) + self.output_options[self.output_mode])
            menu.clear_row(2)
        elif self.edit_mode == EDIT_EXIT:
            menu.write_row(0, chr(1) + ' Done?')
            menu.write_row(1, ' ' + chr(3) + 'Exit')
            menu.clear_row(2)

        if self.millis() - self.last_update > 1000:
            self.actual_volume = self.get_volume()
            self.last_update = self.millis()

            if self.backlight is not None:
                self.backlight.set_graph(float(self.actual_volume) / 100.0)
