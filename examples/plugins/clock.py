import time

from dot3k.menu import MenuOption


class Clock(MenuOption):
    def __init__(self, backlight=None):
        self.modes = ['date', 'week', 'binary', 'dim', 'bright']
        self.mode = 0
        self.binary = True
        self.running = False

        if backlight is None:
            import dot3k.backlight
            self.backlight = dot3k.backlight
        else:
            self.backlight = backlight

        self.option_time = 0

        self.dim_hour = 20
        self.bright_hour = 8

        self.is_setup = False

        MenuOption.__init__(self)

    def begin(self):
        self.is_setup = False
        self.running = True

    def setup(self, config):
        MenuOption.setup(self, config)
        self.load_options()

    def set_backlight(self, brightness):
        brightness += 0.01
        if brightness > 1.0:
            brightness = 1.0
        r = int(int(self.get_option('Backlight', 'r')) * brightness)
        g = int(int(self.get_option('Backlight', 'g')) * brightness)
        b = int(int(self.get_option('Backlight', 'b')) * brightness)
        if self.backlight is not None:
            self.backlight.rgb(r, g, b)

    def update_options(self):
        self.set_option('Clock', 'dim', str(self.dim_hour))
        self.set_option('Clock', 'bright', str(self.bright_hour))
        self.set_option('Clock', 'binary', str(self.binary))

    def load_options(self):
        self.dim_hour = int(self.get_option('Clock', 'dim', str(self.dim_hour)))
        self.bright_hour = int(self.get_option('Clock', 'bright', str(self.bright_hour)))
        self.binary = self.get_option('Clock', 'binary', str(self.binary)) == 'True'

    def cleanup(self):
        self.running = False
        time.sleep(0.01)
        self.set_backlight(1.0)
        self.is_setup = False

    def left(self):
        if self.modes[self.mode] == 'binary':
            self.binary = False
        elif self.modes[self.mode] == 'dim':
            self.dim_hour = (self.dim_hour - 1) % 24
        elif self.modes[self.mode] == 'bright':
            self.bright_hour = (self.bright_hour - 1) % 24
        else:
            return False
        self.update_options()
        self.option_time = self.millis()
        return True

    def right(self):
        if self.modes[self.mode] == 'binary':
            self.binary = True
        elif self.modes[self.mode] == 'dim':
            self.dim_hour = (self.dim_hour + 1) % 24
        elif self.modes[self.mode] == 'bright':
            self.bright_hour = (self.bright_hour + 1) % 24
        self.update_options()
        self.option_time = self.millis()
        return True

    def up(self):
        self.mode = (self.mode - 1) % len(self.modes)
        self.option_time = self.millis()
        return True

    def down(self):
        self.mode = (self.mode + 1) % len(self.modes)
        self.option_time = self.millis()
        return True

    def redraw(self, menu):
        if not self.running:
            return False

        if self.millis() - self.option_time > 5000 and self.option_time > 0:
            self.option_time = 0
            self.mode = 0

        if not self.is_setup:
            menu.lcd.create_char(0, [0, 0, 0, 14, 17, 17, 14, 0])
            menu.lcd.create_char(1, [0, 0, 0, 14, 31, 31, 14, 0])
            menu.lcd.create_char(2, [0, 14, 17, 17, 17, 14, 0, 0])
            menu.lcd.create_char(3, [0, 14, 31, 31, 31, 14, 0, 0])
            menu.lcd.create_char(4, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            menu.lcd.create_char(5, [0, 0, 10, 27, 10, 0, 0, 0])  # Left right arrow
            self.is_setup = True

        hour = float(time.strftime('%H'))
        brightness = 1.0
        if hour > self.dim_hour:
            brightness = 1.0 - ((hour - self.dim_hour) / (24.0 - self.dim_hour))
        elif hour < self.bright_hour:
            brightness = 1.0 * (hour / self.bright_hour)

        self.set_backlight(brightness)

        menu.write_row(0, time.strftime('  %a %H:%M:%S  '))

        if self.binary:
            binary_hour = str(bin(int(time.strftime('%I'))))[2:].zfill(4).replace('0', chr(0)).replace('1', chr(1))
            binary_min = str(bin(int(time.strftime('%M'))))[2:].zfill(6).replace('0', chr(2)).replace('1', chr(3))
            binary_sec = str(bin(int(time.strftime('%S'))))[2:].zfill(6).replace('0', chr(0)).replace('1', chr(1))
            menu.write_row(1, binary_hour + binary_min + binary_sec)
        else:
            menu.write_row(1, '-' * 16)

        if self.idling:
            menu.clear_row(2)
            return True

        bottom_row = ''

        if self.modes[self.mode] == 'date':
            bottom_row = time.strftime('%b %Y:%m:%d ')
        elif self.modes[self.mode] == 'week':
            bottom_row = time.strftime('   Week: %W')
        elif self.modes[self.mode] == 'binary':
            bottom_row = ' Binary ' + chr(5) + ('Y' if self.binary else 'N')
        elif self.modes[self.mode] == 'dim':
            bottom_row = ' Dim at ' + chr(5) + str(self.dim_hour).zfill(2)
        elif self.modes[self.mode] == 'bright':
            bottom_row = ' Bright at ' + chr(5) + str(self.bright_hour).zfill(2)

        menu.write_row(2, chr(4) + bottom_row)
