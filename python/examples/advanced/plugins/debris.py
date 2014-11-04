from dot3k.menu import MenuOption
import dot3k.backlight
import random, time

class Debris(MenuOption):
  def __init__(self):
    self.debug = False
    self.debris = []
    self.stars = []
    self.running = False
    self.max_debris = 10
    self.max_stars  = 10
    self.last_update = 0
    self.time_start = 0
    self.sprites = [
      [14,31,31,14,0 ,0 ,0 ,0 ], # 0: Debris top of char
      [0 ,0 ,0 ,0 ,14,31,31,14], # 1: Debris bottom of char
      [30,5 ,7 ,30,0 ,0 ,0 ,0 ], # 2: Ship top of char
      [0 ,0 ,0 ,0 ,30,5 ,7, 30], # 3: Ship bottom of char

      [30,5 ,7 ,30,14,31,31,14], # 4: Ship above debris
      [14,31,31,14,30,5 ,7, 30], # 5: Ship below debris
    ]
    self.width  = 16
    self.height = 5 # Two rows per char
  
    self.player_x = 1 # Player horizontal position
    self.player_y = 3 # Player vertical position

    self.current_player_x   = None
    self.current_player_y   = None
    self.current_player_pos = None

    self.fill_debris()

    MenuOption.__init__(self)

  def begin(self):
    self.running = False
    self.reset()
    dot3k.backlight.hue(0.0)

  def reset(self):
    self.player_x = 1
    self.player_y = 3
    self.fill_debris()
    self.fill_stars()
    self.running = True
    self.time_start = 0
    self.last_update = 0
  
  def fill_stars(self):
    self.stars = []
    while len(self.stars) < self.max_stars:
      self.stars.append((random.randint(3,15),random.randint(0,2)))

  def fill_debris(self):
    self.debris = []
    while len(self.debris) < self.max_debris:
      self.debris.append((random.randint(8,15),random.randint(0,self.height)))

  def left(self):
    if not self.running:
      r = int(self.get_option('Backlight','r'))
      g = int(self.get_option('Backlight','g'))
      b = int(self.get_option('Backlight','b'))
      dot3k.backlight.rgb(r,g,b)
      return False
    self.player_x -= 1
    if self.player_x < 0:
      self.player_x = 0
    return True

  def right(self):
    if not self.running:
      self.reset()
      return True
    self.player_x += 1
    if self.player_x > 15:
      self.player_x = 15
    return True

  def up(self):
    self.player_y -= 1
    if self.player_y < 0:
      self.player_y = 0
    if self.debug:
      print("Player up", self.player_y)
    return True
  
  def down(self):
    self.player_y += 1
    if self.player_y > self.height:
      self.player_y = self.height - 1
    if self.debug:
      print("Player down", self.player_y)
    return True

  def update(self, menu):
    if self.time_start == 0:
 
      for idx, sprite in enumerate(self.sprites):
        menu.lcd.create_char(idx, sprite)

      menu.clear_row(0)
      menu.clear_row(1)
      menu.clear_row(2)
      for x in range(3):
        menu.lcd.set_cursor_position(5,1)
        menu.lcd.write('  0' + str(3-x) + '! ')
        time.sleep(0.5)
      dot3k.backlight.hue(0.5)
      self.time_start = self.millis()

    self.current_player_x   = int(self.player_x)
    self.current_player_y   = int(self.player_y / 2)
    self.current_player_pos = (self.player_y % 2)
 
    # Move all stars left
    for idx, star in enumerate(self.stars):
      self.stars[idx] = (star[0] - 0.5, star[1])

    # Move all debris left 1 place
    for idx, rock in enumerate(self.debris):
      self.debris[idx] = (rock[0] - 1, rock[1])
      debris_x   = int(rock[0])
      debris_y   = int(rock[1] / 2)
      debris_pos = (rock[1] % 2)
     
      if (debris_x,debris_y,debris_pos) == (self.current_player_x,self.current_player_y,self.current_player_pos):
        # Boom!
        menu.lcd.set_cursor_position(5,1)
        menu.lcd.write(' BOOM!')

        if self.debug:
          print(debris_x,debris_y,debris_pos)
          print(self.current_player_x, 
                self.current_player_y,
                self.current_player_pos)

          print(self.player_x, self.player_y)
          exit()

        self.running = False
        #time.sleep(1)
        #self.reset()
        return False

    # Remove off-screen debris
    self.debris = list(filter(lambda x: x[0] > -1, self.debris))

    # Remove off-screen stars
    self.stars = list(filter(lambda x: x[0] > -1, self.stars))

    # Create new debris to replace the removed ones
    while len(self.debris) < self.max_debris:
      self.debris.append((15,random.randint(0,self.height)))

    while len(self.stars) < self.max_stars:
      self.stars.append((15,random.randint(0,2)))

    return True

  def redraw(self, menu):
    if not self.running:
      return False
    if self.millis() - self.last_update >= 250:
      if not self.update(menu):
        return False
      self.last_update = self.millis()

    game_time = str(int((self.millis()-self.time_start)/1000)).zfill(3)
    dot3k.backlight.sweep(((self.millis()-self.time_start)/500 % 360)/359.0)

    buffer = []
    for i in range(3):
      buffer.append( [' '] * 16 )

    for idx, rock in enumerate(self.stars):
      buffer[rock[1]][int(rock[0])] = '.'
    
    #player_y      = int(self.player_y / 2)
    #player_x      = self.player_x
    player_sprite = 2 + self.current_player_pos

    buffer[self.current_player_y][self.current_player_x] = chr(player_sprite)

    for idx, rock in enumerate(self.debris):
      debris_x = int(rock[0])
      debris_y = int(rock[1] / 2)
      debris_sprite = (rock[1] % 2)

      if (debris_y, debris_x) == (self.current_player_y, self.current_player_x):
        if (rock[1] % 2) != self.current_player_pos:
          debris_sprite = 2 + player_sprite

      buffer[debris_y][debris_x] = chr(debris_sprite)

    # Draw elapsed seconds
    buffer[0][16-len(game_time):len(game_time)] = game_time

    for idx, row in enumerate(buffer):
      menu.write_row(idx,''.join(row))
 

