from dot3k.menu import MenuOption
import dot3k.backlight
import time

class Text(MenuOption):
  def __init__(self):

    self.mode        = 'entry'

    self.initialized = False
    self.back_icon   = chr(0)
    self.entry_char  = 0
    self.entry_mode  = 0
    self.entry_chars = [list('\'|~+-_!?.0123456789'+self.back_icon+' abcdefghijklmnopqrstuvwxyz' + self.back_icon),
					   list('"<>{}()[]:;/\^&*$%#'+self.back_icon+'@ABCDEFGHIJKLMNOPQRSTUVWXYZ'  + self.back_icon)]

    self.entry_text  = [' ']*16

    self.confirm = False
    self.final_text = ''

    self.entry_position = 0

    MenuOption.__init__(self)
    
    self.is_setup = False

  def set_value(self, value):
    length = len(value)
    self.entry_text = list(value + self.back_icon + (' '*(16-length)))
    self.entry_position = length

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
    self.entry_char  = 0
    self.entry_mode  = 0
    self.entry_position = 0
    self.mode        = 'entry'
    self.pick_char(' ')
    self.entry_text  = [' ']*16
    self.set_value('Booblie!')

  def setup(self, config):
    MenuOption.setup(self, config)

  def cleanup(self):
    self.entry_text  = [' ']*16
   
  def left(self):
    if self.mode == 'confirm':
      self.confirm = True
      return True
    if self.entry_text[self.entry_position] == self.back_icon:
      return True
    self.prev_letter()
    return True

  def right(self):
    if self.mode == 'confirm':
      self.confirm = False
      return True
    if self.entry_text[self.entry_position] == self.back_icon:
      return True
    self.next_letter()
    return True

  def up(self):
    if self.mode == 'confirm':
      return True
    self.prev_char()
    return True
  
  def down(self):
    if self.mode == 'confirm':
      return True
    self.next_char()
    return True

  def select(self):
    if self.mode == 'confirm':
      if self.confirm:
        return True
      else:
        self.mode = 'entry'
        return False

    if self.entry_text[self.entry_position] == self.back_icon:
      text = ''.join(self.entry_text)
      self.final_text = text[0:text.index(self.back_icon)].strip()
      self.mode = 'confirm'
    else:
      self.change_case()
    return False
  
  def redraw(self, menu):
    if not self.initialized:
      menu.lcd.create_char(0,[0,8,30,9,1,1,14,0])  # Back icon
      menu.lcd.create_char(4,[0,4,14,0,0,14,4,0]) # Up down arrow
      menu.lcd.create_char(5,[0,0,10,27,10,0,0,0]) # Left right arrow
      self.initialized = True

    if self.mode == 'entry':
      menu.clear_row(0)
      menu.write_row(1,''.join(self.entry_text))
      menu.write_row(2,(' ' * self.entry_position) + chr(4))
    else:
      menu.write_row(0,'Confirm?')
      menu.write_row(1,self.final_text)
      menu.write_row(2,'  ' + ('>' if self.confirm else ' ') + 'Yes    ' + ('>' if not self.confirm else ' ') + 'No   ')
