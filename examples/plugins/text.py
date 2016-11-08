from dot3k.menu import MenuOption


_MODE_CONFIRM = 1
_MODE_ENTRY = 0


class Text(MenuOption):
    def __init__(self):

        self.mode = _MODE_ENTRY
        self.input_prompt = ''

        self.initialized = False
        self.back_icon = chr(0)
        self.entry_char = 0
        self.entry_mode = 0
        self.entry_chars = [
            list('\'|~+-_!?.0123456789' + self.back_icon + ' abcdefghijklmnopqrstuvwxyz' + self.back_icon),
            list('"<>{}()[]:;/\^&*$%#' + self.back_icon + '@ABCDEFGHIJKLMNOPQRSTUVWXYZ' + self.back_icon)]

        self.entry_text = [' '] * 16

        self.confirm = 0
        self.final_text = ''

        self.entry_position = 0

        MenuOption.__init__(self)

        self.is_setup = False

    def set_value(self, value):
        length = len(value)
        self.entry_text = list(value + self.back_icon + (' ' * (16 - length)))
        self.entry_position = length

    def set_prompt(self, value):
        self.input_prompt = value

    def get_value(self):
        return self.final_text

    def update_char(self):
        self.entry_text[self.entry_position] = self.entry_chars[self.entry_mode][self.entry_char]

    def change_case(self):
        self.entry_mode = (self.entry_mode + 1) % len(self.entry_chars)
        self.update_char()

    def next_char(self):
        self.entry_char = (self.entry_char + 1) % len(self.entry_chars[0])
        self.update_char()

    def prev_char(self):
        self.entry_char = (self.entry_char - 1) % len(self.entry_chars[0])
        self.update_char()

    def pick_char(self, pick):
        for x, chars in enumerate(self.entry_chars):
            for y, char in enumerate(chars):
                if char == pick:
                    self.entry_mode = x
                    self.entry_char = y

    def prev_letter(self):
        self.entry_position = (self.entry_position - 1) % len(self.entry_text)
        self.pick_char(self.entry_text[self.entry_position])

    def next_letter(self):
        self.entry_position = (self.entry_position + 1) % len(self.entry_text)
        self.pick_char(self.entry_text[self.entry_position])

    def begin(self):
        self.initialized = False
        self.entry_char = 0
        self.entry_mode = 0
        self.entry_position = 0
        self.mode = _MODE_ENTRY
        self.pick_char(' ')
        self.entry_text = [' '] * 16
        self.set_value('')

    def setup(self, config):
        MenuOption.setup(self, config)

    def cleanup(self):
        self.entry_text = [' '] * 16

    def left(self):
        if self.mode == _MODE_CONFIRM:
            self.confirm = (self.confirm + 1) % 3
            return True
        if self.entry_text[self.entry_position] == self.back_icon:
            return True
        self.prev_letter()
        return True

    def right(self):
        if self.mode == _MODE_CONFIRM:
            self.confirm = (self.confirm - 1) % 3
            return True
        if self.entry_text[self.entry_position] == self.back_icon:
            return True
        self.next_letter()
        return True

    def up(self):
        if self.mode == _MODE_CONFIRM:
            return True
        self.prev_char()
        return True

    def down(self):
        if self.mode == _MODE_CONFIRM:
            return True
        self.next_char()
        return True

    def select(self):
        if self.mode == _MODE_CONFIRM:
            if self.confirm == 1:  # Yes
                return True
            elif self.confirm == 2:  # Quit
                self.cancel_input = True
                self.mode = _MODE_ENTRY
                return True
            else:  # No
                self.mode = _MODE_ENTRY
                return False

        if self.entry_text[self.entry_position] == self.back_icon:
            text = ''.join(self.entry_text)
            self.final_text = text[0:text.index(self.back_icon)].strip()
            self.mode = _MODE_CONFIRM
        else:
            self.change_case()
        return False

    def redraw(self, menu):
        if not self.initialized:
            menu.lcd.create_char(0, [0, 8, 30, 9, 1, 1, 14, 0])  # Back icon
            menu.lcd.create_char(4, [0, 4, 14, 0, 0, 14, 4, 0])  # Up down arrow
            menu.lcd.create_char(5, [0, 0, 10, 27, 10, 0, 0, 0])  # Left right arrow
            self.initialized = True

        if self.mode == _MODE_ENTRY:
            menu.write_row(0, self.input_prompt)
            menu.write_row(1, ''.join(self.entry_text))
            if self.entry_text[self.entry_position] == self.back_icon:
                if self.entry_position > 3:
                    menu.write_row(2, (' ' * (self.entry_position - 3)) + 'END' + chr(4))
                else:
                    menu.write_row(2, (' ' * self.entry_position) + chr(4) + 'END')
            else:
                menu.write_row(2, (' ' * self.entry_position) + chr(4))
        else:
            menu.write_row(0, 'Confirm?')
            menu.write_row(1, self.final_text)
            menu.write_row(2,
                           ' ' + ('>' if self.confirm == 1 else ' ') + 'Yes ' +
                           ('>' if self.confirm == 0 else ' ') + 'No ' +
                           ('>' if self.confirm == 2 else ' ') + 'Quit')
