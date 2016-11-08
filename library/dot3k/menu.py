import atexit
import os
import threading
import time
from collections import OrderedDict
from sys import version_info

if version_info[0] >= 3:
    import configparser as ConfigParser
else:
    import ConfigParser


_MODE_NAV = 'navigate'
_MODE_ADJ = 'adjust'
_MODE_TXT = 'entry'


class MenuIcon:
    arrow_left = [0, 0, 8, 24, 8, 0, 0, 0]
    arrow_right = [0, 0, 2, 3, 2, 0, 0, 0]
    arrow_up = [0, 4, 14, 0, 0, 0, 0, 0]
    arrow_down = [0, 0, 0, 0, 0, 14, 4, 0]
    arrow_left_right = [0, 0, 10, 27, 10, 0, 0, 0]
    arrow_up_down = [0, 4, 14, 0, 0, 14, 4, 0]
    play = [0, 24, 30, 31, 30, 24, 0, 0]
    pause = [0, 27, 27, 27, 27, 27, 0, 0]
    back = [0, 8, 30, 9, 1, 1, 14, 0]
    bar_left = [0, 3, 2, 2, 2, 2, 3, 0]
    bar_right = [0, 24, 8, 8, 8, 8, 24, 0]
    bar_full = [0, 31, 0, 31, 31, 0, 31, 0]
    bar_empty = [0, 32, 0, 0, 0, 0, 32, 0]


class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True

    def start(self):
        if not self.isAlive():
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive():
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class AsyncWorker(StoppableThread):
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while not self.stop_event.is_set():
            if self.todo() is False:
                self.stop_event.set()
                break


class Menu:
    """
    This class accepts a list of menu items,
    Each key corresponds to a text item displayed on the menu
    Each value can either be:
    * A nested list, for a sub-menu
    * A function, which is called immediately on select
    * A class derived from MenuOption, providing interactive functionality
    """

    def __init__(self, *args, **kwargs):
        """
        structure, lcd, idle_handler = None, idle_time = 60
        """
        self.menu_options = OrderedDict()
        self.lcd = None
        self.idle_handler = None
        self.input_handler = None
        self.idle_time = 60 * 1000
        self.config_file = 'dot3k.cfg'

        # Track displayed text for auto-scroll
        self.last_text = ['', '', '']
        self.last_change = [0, 0, 0]

        if len(args) > 0 and args[0] is not None:
            self.menu_options = args[0]
        if len(args) > 1:
            self.lcd = args[1]
        if len(args) > 2:
            self.idle_handler = args[2]
        if len(args) > 3:
            self.idle_time = args[3] * 1000

        if 'structure' in kwargs.keys() and kwargs['structure'] is not None:
            self.menu_options = kwargs['structure']
        if 'lcd' in kwargs.keys():
            self.lcd = kwargs['lcd']
        if 'idle_handler' in kwargs.keys():
            self.idle_handler = kwargs['idle_handler']
        if 'idle_time' in kwargs.keys():
            self.idle_time = kwargs['idle_time'] * 1000
        if 'input_handler' in kwargs.keys():
            self.input_handler = kwargs['input_handler']
        if 'config_file' in kwargs.keys():
            self.config_file = kwargs['config_file']

        self.list_location = []
        self.current_position = 0
        self.idle = False
        self.mode = _MODE_NAV

        self.config = ConfigParser.ConfigParser()
        self.config.read([self.config_file, os.path.expanduser('~/.' + self.config_file)])

        if type(self.menu_options) is dict or type(self.menu_options) is OrderedDict:
            self._setup_menu(self.menu_options)

        self.last_action = self.millis()
        self._thread = AsyncWorker(self._update)
        atexit.register(self.save)

    def run(self):
        self._thread.start()
        atexit.register(self.stop)

    def stop(self):
        self._thread.stop()

    def _update(self):
        self.redraw()
        time.sleep(0.05)

    def millis(self):
        return int(round(time.time() * 1000))

    def add_item(self, path, handler):
        if not type(path) is list:
            path = path.split('/')
        loc = self.menu_options
        last = path.pop()

        while len(path) > 0:
            key = path.pop(0)
            if key not in loc:
                loc[key] = OrderedDict()
            loc = loc[key]

        loc[last] = handler

        if isinstance(loc[last], MenuOption):
            loc[last].setup(self.config)

    def save(self):
        if version_info[0] >= 3:
            with open('dot3k.cfg', 'wt', encoding='utf-8') as configfile:
                self.config.write(configfile)
        else:
            with open('dot3k.cfg', 'wb') as configfile:
                self.config.write(configfile)
        print('Config saved to dot3k.cfg')

    def _setup_menu(self, menu):
        for key in menu:
            value = menu[key]
            if type(value) is dict or type(value) is OrderedDict:
                self._setup_menu(value)
            elif isinstance(value, MenuOption):
                value.setup(self.config)

    def current_submenu(self):
        """
        Traverse the list of indexes in list_location
        and find the relevant nested listionary
        """
        menu = self.menu_options
        for location in self.list_location:
            menu = menu[list(menu.keys())[location]]
        return menu

    def current_value(self):
        return self.current_submenu()[self.current_key()]

    def current_key(self):
        """
        Convert the integer current_position into
        a valid key for the currently selected listionary
        """
        return list(self.current_submenu().keys())[self.current_position]

    def next_position(self):
        position = self.current_position + 1
        position %= len(self.current_submenu())
        return position

    def previous_position(self):
        position = self.current_position - 1
        position %= len(self.current_submenu())
        return position

    def select_option(self):
        """
        Navigate into, or handle selected menu option accordingly
        """
        if type(self.current_value()) is dict or type(self.current_value()) is OrderedDict:
            self.list_location.append(self.current_position)
            self.current_position = 0
        elif isinstance(self.current_value(), MenuOption):
            self.mode = _MODE_ADJ
            self.current_value().begin()
        elif callable(self.current_submenu()[self.current_key()]):
            self.current_submenu()[self.current_key()]()

    def prev_option(self):
        """
        Decrement the option pointer,
        select previous menu item
        """
        self.current_position = self.previous_position()

    def next_option(self):
        """
        Increment the option pointer,
        select next menu item
        """
        self.current_position = self.next_position()

    def exit_option(self):
        """
        Exit current submenu and restore position
        in previous menu
        """
        if len(self.list_location) > 0:
            self.current_position = self.list_location.pop()

    def start_input(self):
        if self.input_handler is None:
            return False

        self.current_value().text_entry = False
        self.input_handler.begin()
        self.input_handler.set_value(self.current_value().initial_value())
        self.input_handler.set_prompt(self.current_value().input_prompt())
        self.mode = _MODE_TXT

    def finish_input(self):
        if self.input_handler.cancel_input:
            self.current_value().cancel_input()
            self.input_handler.cancel_input = False
            self.input_handler.cleanup()
            self.mode = _MODE_ADJ
        else:
            self.current_value().receive_input(self.input_handler.get_value())
            self.input_handler.cleanup()
            self.mode = _MODE_ADJ

    def select(self):
        """
        Handle "select" action
        """
        self.last_action = self.millis()
        if self.idle:
            self.idle = False
            self.idle_handler.cleanup()
            self.idle_handler.idling = False
            return True

        if self.mode == _MODE_NAV:
            self.select_option()
        elif self.mode == _MODE_ADJ:
            # The "select" call must return true to exit the adjust
            if self.current_value().select() is True:
                self.mode = _MODE_NAV
        elif self.mode == _MODE_TXT:
            if self.input_handler.select():
                self.finish_input()

    def cancel(self):
        self.last_action = self.millis()
        if self.idle:
            self.idle = False
            self.idle_handler.cleanup()
            self.idle_handler.idling = False
            return True

        if self.mode == _MODE_NAV:
            self.exit_option()
        if self.mode == _MODE_ADJ:
            self.current_value().cleanup()
            self.mode = _MODE_NAV

    def up(self):
        self.last_action = self.millis()
        if self.idle:
            self.idle = False
            self.idle_handler.cleanup()
            self.idle_handler.idling = False
            return True

        if self.mode == _MODE_NAV:
            self.prev_option()
        elif self.mode == _MODE_ADJ:
            self.current_value().up()
        elif self.mode == _MODE_TXT:
            self.input_handler.up()

    def down(self):
        self.last_action = self.millis()
        if self.idle:
            self.idle = False
            self.idle_handler.cleanup()
            self.idle_handler.idling = False
            return True

        if self.mode == _MODE_NAV:
            self.next_option()
        elif self.mode == _MODE_ADJ:
            self.current_value().down()
        elif self.mode == _MODE_TXT:
            self.input_handler.down()

    def left(self):
        self.last_action = self.millis()
        if self.idle:
            self.idle = False
            self.idle_handler.cleanup()
            self.idle_handler.idling = False
            return True

        if self.mode == _MODE_NAV:
            self.exit_option()
        elif self.mode == _MODE_ADJ:
            if not self.current_value().left():
                self.current_value().cleanup()
                self.mode = _MODE_NAV
        elif self.mode == _MODE_TXT:
            self.input_handler.left()

    def right(self):
        self.last_action = self.millis()
        if self.idle:
            self.idle = False
            self.idle_handler.cleanup()
            self.idle_handler.idling = False
            return True

        if self.mode == _MODE_NAV:
            self.select_option()
        elif self.mode == _MODE_ADJ:
            self.current_value().right()
        elif self.mode == _MODE_TXT:
            self.input_handler.right()

    def clear_row(self, row):
        self.lcd.set_cursor_position(0, row)
        self.lcd.write(' ' * self.lcd.COLS)

    def write_row(self, row, text):
        self.lcd.set_cursor_position(0, row)
        while len(text) < self.lcd.COLS:
            text += ' '
        self.lcd.write(text[0:self.lcd.COLS])

    def write_option(self, *args, **kwargs):

        row = 0
        text = ''
        icon = ''
        margin = 0
        scroll = False

        scroll_padding = '  '
        scroll_delay = 2000
        scroll_repeat = 10000
        scroll_speed = 200

        if len(args) > 0:
            row = args[0]
        if len(args) > 1:
            text = args[1]
        if len(args) > 2:
            icon = args[2]
        if len(args) > 3:
            margin = args[3]

        if 'row' in kwargs.keys():
            row = kwargs['row']
        if 'text' in kwargs.keys():
            text = kwargs['text']
        if 'icon' in kwargs.keys():
            icon = kwargs['icon']
        if 'margin' in kwargs.keys():
            margin = kwargs['margin']

        if 'scroll' in kwargs.keys() and kwargs['scroll'] == True:
            scroll = True
        if 'scroll_speed' in kwargs.keys():
            scroll_speed = kwargs['scroll_speed']
        if 'scroll_repeat' in kwargs.keys():
            scroll_repeat = kwargs['scroll_repeat']
        if 'scroll_delay' in kwargs.keys():
            scroll_delay = kwargs['scroll_delay']
        if 'scroll_padding' in kwargs.keys():
            scroll_padding = kwargs['scroll_padding']

        if icon == None:
            icon = ''

        if margin == None:
            margin = 0

        current_row = ''

        if self.last_text[row] != text:
            self.last_text[row] = text
            self.last_change[row] = self.millis()

        if scroll:
            text += scroll_padding

        if scroll and self.millis() - self.last_change[row] > scroll_delay:
            pos = int(((self.millis() - self.last_change[row] - scroll_delay) / scroll_speed) % len(text))
            text = text[pos:] + text[:pos]
            if pos == len(text) - 1:
                self.last_change[row] = self.millis() + scroll_repeat

        current_row += icon

        while len(current_row) < margin:
            current_row += ' '

        current_row += text

        self.write_row(row, current_row)

    def get_menu_item(self, index):
        return list(self.current_submenu().keys())[index]

    def redraw(self):
        if self.can_idle() and isinstance(self.idle_handler, MenuOption):
            if not self.idle:
                self.idle_handler.idling = True
                self.idle_handler.begin()
            self.idle = True
            self.idle_handler.redraw(self)
            return False

        if self.mode == _MODE_NAV:
            self.write_option(
                row=1,
                text=self.get_menu_item(self.current_position),
                icon=chr(252),
                margin=1
            )

            if len(self.current_submenu()) > 2:
                self.write_option(
                    row=0,
                    text=self.get_menu_item(self.previous_position()),
                    margin=1
                )
            else:
                self.clear_row(0)

            if len(self.current_submenu()) > 1:
                self.write_option(
                    row=2,
                    text=self.get_menu_item(self.next_position()),
                    margin=1
                )
            else:
                self.clear_row(2)


        # Call the redraw function of the endpoint Class
        elif self.mode == _MODE_ADJ:
            self.current_value().redraw(self)
            if self.current_value().text_entry:
                self.start_input()

        elif self.mode == _MODE_TXT:
            self.input_handler.redraw(self)

    def can_idle(self):
        if self.millis() - self.last_action >= self.idle_time:
            if self.mode == _MODE_NAV:
                return True
            if self.mode == _MODE_ADJ and self.current_value().can_idle:
                return True
        return False


class MenuOption:
    def __init__(self):
        self.idling = False
        self.can_idle = False
        self.config = None
        self.text_entry = False

    """
    These helper functions let you start
    the input_handler of the parent menu
    and receive the text that the user inputs
    """

    def initial_value(self):
        # Return a value to start with
        return ''

    def receive_input(self, value):
        # Return false to reject input
        return True

    def request_input(self):
        self.text_entry = True

    def cancel_input(self):
        # Called if input is cancelled by handler
        pass

    def input_prompt(self):
        return 'Input text:'

    """
    These helper functions are for
    input handler plugins
    """

    def set_value(self, value):
        pass

    def get_value(self):
        return ''

    def set_prompt(self, value):
        pass

    def millis(self):
        return int(round(time.time() * 1000))

    def up(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def select(self):
        # Must return true to allow exit
        return True

    def begin(self):
        pass

    def redraw(self, menu):
        pass

    def setup(self, config):
        self.config = config

    def cleanup(self):
        # Undo any backlight or other changes
        pass

    def set_option(self, section, option, value):
        if self.config is not None:
            if section not in self.config.sections():
                self.config.add_section(section)
            self.config.set(section, option, value)

    def get_option(self, section, option, default=None):
        if section not in self.config.sections():
            self.config.add_section(section)
        if option in self.config.options(section):
            return self.config.get(section, option)
        elif default is None:
            return False
        else:
            self.config.set(section, option, str(default))
            return default
