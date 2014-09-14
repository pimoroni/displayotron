import time, ConfigParser, os, atexit

class Menu():
  """
  This class accepts a list of menu items,
  Each key corresponds to a text item displayed on the menu
  Each value can either be:
  * A nested list, for a sub-menu
  * A function, which is called immediately on select
  * A class derived from MenuOption, providing interactive functionality
  """

  def __init__(self, structure, lcd, idle_handler = None, idle_time = 60):
    self.list_location = []
    self.lcd = lcd
    self.current_position = 0
    self.idle_handler = idle_handler
    self.idle_time = idle_time*1000
    self.idle = False
    self.mode = 'navigate'
    self.menu_options = structure

    self.config = ConfigParser.ConfigParser()
    self.config.read(['dot3k.cfg', os.path.expanduser('~/.dot3k.cfg')])

    self.setup_menu(self.menu_options)
   
    self.last_action = self.millis()

    atexit.register(self.save)

  def millis(self):
    return int(round(time.time() * 1000))

  def save(self):
    with open('dot3k.cfg', 'wb') as configfile:
      self.config.write(configfile)
      print('Config saved to dot3k.cfg')

  def setup_menu(self, menu):
    for key in menu:
      value = menu[key]
      if type(value) is dict:
        self.setup_menu(value)
      elif isinstance(value,MenuOption):
        value.setup(self.config)

  def current_submenu(self):
    """
    Traverse the list of indexes in list_location
    and find the relevant nested dictionary
    """
    menu = self.menu_options
    for location in self.list_location:
      menu = menu[menu.keys()[location]]
    return menu

  def current_value(self):
    return self.current_submenu()[self.current_key()]
    
  def current_key(self):
    """
    Convert the integer current_position into
    a valid key for the currently selected dictionary
    """
    return self.current_submenu().keys()[self.current_position]

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
    if type(self.current_value()) is dict:
      self.list_location.append( self.current_position )
      self.current_position = 0
    elif isinstance(self.current_value(),MenuOption):
      self.mode = 'adjust'
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

    if self.mode == 'navigate':
      self.select_option()
    elif self.mode == 'adjust':
      # The "select" call must return true to exit the adjust
      if self.current_value().select():
        self.mode = 'navigate'

  def up(self):
    self.last_action = self.millis()
    if self.idle:
      self.idle = False
      self.idle_handler.cleanup()
      self.idle_handler.idling = False
      return True

    if self.mode == 'navigate':
      self.prev_option()
    elif self.mode == 'adjust':
      self.current_value().up()

  def down(self):
    self.last_action = self.millis()
    if self.idle:
      self.idle = False
      self.idle_handler.cleanup()
      self.idle_handler.idling = False
      return True

    if self.mode == 'navigate':
      self.next_option()
    elif self.mode == 'adjust':
      self.current_value().down()

  def left(self):
    self.last_action = self.millis()
    if self.idle:
      self.idle = False
      self.idle_handler.cleanup()
      self.idle_handler.idling = False
      return True

    if self.mode == 'navigate':
      self.exit_option()
    elif self.mode == 'adjust':
      if not self.current_value().left():
        self.current_value().cleanup()
        self.mode = 'navigate'

  def right(self):
    self.last_action = self.millis()
    if self.idle:
      self.idle = False
      self.idle_handler.cleanup()
      self.idle_handler.idling = False
      return True

    if self.mode == 'navigate':
      self.select_option()
    elif self.mode == 'adjust':
      self.current_value().right()

  def clear_row(self,row):
    self.lcd.set_cursor_position(0,row)
    self.lcd.write(' '*16)
  
  def write_row(self,row,text):
    self.lcd.set_cursor_position(0,row)
    while len(text) < 16:
      text += ' '
    self.lcd.write(text[0:16])

  def write_option(self,row,text,icon=' ',margin=1):
     
    current_row = ''

    current_row += icon
   
    while len(current_row) < margin:
      current_row += ' '

    current_row += text
    
    self.write_row(row,current_row)

  def get_menu_item(self, index):
    return self.current_submenu().keys()[index]

  def redraw(self): 
    if self.can_idle() and isinstance(self.idle_handler,MenuOption):
      if self.idle == False:
        self.idle_handler.idling = True
        self.idle_handler.begin()
      self.idle = True
      self.idle_handler.redraw(self)
      return False

    if self.mode == 'navigate':
      self.write_option(1,self.get_menu_item(self.current_position),chr(252))

      if len(self.current_submenu()) > 2:
        self.write_option(0, self.get_menu_item(self.previous_position()))
      else:
        self.clear_row(0)

      if len(self.current_submenu()) > 1:
        self.write_option(2, self.get_menu_item(self.next_position()))
      else:
        self.clear_row(2)
      

    # Call the redraw function of the endpoint Class
    elif self.mode == 'adjust':
      self.current_value().redraw(self)

  def can_idle(self):
    if self.millis() - self.last_action >= self.idle_time:
      if self.mode == 'navigate':
        return True
      if self.mode == 'adjust' and self.current_value().can_idle:
        return True
    return False
 

class MenuOption():
  def __init__(self):
    self.idling = False
    self.can_idle = False
    self.config = None
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
    if self.config != None:
      if not section in self.config.sections():
        self.config.add_section(section)
      self.config.set(section, option, value)

  def get_option(self, section, option, default = None):
    if not section in self.config.sections():
      self.config.add_section(section)
    if option in self.config.options(section):
      return self.config.get(section, option)
    elif default == None:
      return False
    else:
      self.config.set(section, option, str(default))
      return default
