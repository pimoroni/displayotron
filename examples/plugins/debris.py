import random
import time

from dot3k.menu import MenuOption


class Debris(MenuOption):
    def __init__(self, backlight=None):
        if backlight is None:
            import dot3k.backlight
            self.backlight = dot3k.backlight
        else:
            self.backlight = backlight

        self.debug = False
        self.star_seed = 'thestarsmydestination'
        self.debris_seed = 'piratemonkeyrobotninja'
        self.debris = []
        self.stars = []
        self.running = False
        self.max_debris = 10
        self.max_stars = 10
        self.last_update = 0
        self.time_start = 0
        self.sprites = [
            [14, 31, 31, 14, 0, 0, 0, 0],  # 0: Debris top of char
            [0, 0, 0, 0, 14, 31, 31, 14],  # 1: Debris bottom of char
            [30, 5, 7, 30, 0, 0, 0, 0],  # 2: Ship top of char
            [0, 0, 0, 0, 30, 5, 7, 30],  # 3: Ship bottom of char

            [30, 5, 7, 30, 14, 31, 31, 14],  # 4: Ship above debris
            [14, 31, 31, 14, 30, 5, 7, 30],  # 5: Ship below debris

            [0, 14, 31, 31, 31, 31, 14, 0]  # 6: Giant debris
        ]
        self.width = 16
        self.height = 5  # Two rows per char

        self.player_x = 1  # Player horizontal position
        self.player_y = 3  # Player vertical position

        self.current_player_x = None
        self.current_player_y = None
        self.current_player_pos = None

        self.fill_debris()

        MenuOption.__init__(self)

    def begin(self):
        self.running = False
        self.reset()
        self.backlight.hue(0.0)

    def reset(self):
        self.player_x = 1
        self.player_y = 3
        self.fill_debris()
        self.fill_stars()
        self.running = True
        self.time_start = 0
        self.last_update = 0

    def fill_stars(self):
        random.seed(self.star_seed)
        self.stars = []
        while len(self.stars) < self.max_stars:
            new = (random.randint(0, 15), random.randint(0, 2))
            if not new in self.stars:
                self.stars.append(new)

    def fill_debris(self):
        random.seed(self.debris_seed)
        self.debris = []
        while len(self.debris) < self.max_debris:
            new = (random.randint(5, 15), random.randint(0, self.height))
            if not new in self.debris:
                self.debris.append(new)
        print(self.debris)

    def left(self):
        if not self.running:
            r = int(self.get_option('Backlight', 'r'))
            g = int(self.get_option('Backlight', 'g'))
            b = int(self.get_option('Backlight', 'b'))
            self.backlight.rgb(r, g, b)
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
                menu.lcd.set_cursor_position(5, 1)
                menu.lcd.write('  0' + str(3 - x) + '! ')
                time.sleep(0.5)
            self.backlight.hue(0.5)
            self.time_start = self.millis()

        # Move all stars left
        for idx, star in enumerate(self.stars):
            self.stars[idx] = (star[0] - 0.5, star[1])

        # Move all debris left 1 place
        for idx, rock in enumerate(self.debris):
            self.debris[idx] = (rock[0] - 1, rock[1])
            debris_x = int(rock[0])
            debris_y = int(rock[1])

            if debris_x < 0:
                continue

            if debris_x == self.player_x and debris_y == self.player_y:
                # Boom!
                menu.lcd.set_cursor_position(5, 1)
                menu.lcd.write(' BOOM!')

                if self.debug:
                    print(debris_x, debris_y)
                    print(self.player_x,
                          self.player_y)
                    exit()

                self.running = False
                return False

        # Remove off-screen debris
        self.debris = list(filter(lambda x: x[0] > -1, self.debris))

        # Remove off-screen stars
        self.stars = list(filter(lambda x: x[0] > -1, self.stars))

        # Create new debris to replace the removed ones
        while len(self.debris) < self.max_debris:
            self.debris.append((15, random.randint(0, self.height)))

        while len(self.stars) < self.max_stars:
            self.stars.append((15, random.randint(0, 2)))

        return True

    def redraw(self, menu):
        if not self.running:
            return False
        if self.millis() - self.last_update >= 250:
            if not self.update(menu):
                return False
            self.last_update = self.millis()

        game_time = str(int((self.millis() - self.time_start) / 1000)).zfill(3)
        self.backlight.sweep(((self.millis() - self.time_start) / 500 % 360) / 359.0)

        buffer = []
        for i in range(3):
            buffer.append([' '] * 16)

        for idx, rock in enumerate(self.stars):
            buffer[rock[1]][int(rock[0])] = '.'

        player_v = (self.player_y % 2)

        buffer[int(self.player_y / 2)][self.player_x] = chr(2 + player_v)

        for idx, rock in enumerate(self.debris):
            debris_x = int(rock[0])
            debris_y = int(rock[1])
            debris_v = (debris_y % 2)

            debris_sprite = debris_v

            if int(debris_y / 2) == int(self.player_y / 2) and debris_x == self.player_x and debris_v != player_v:
                debris_sprite = 4 + player_v

            current = buffer[int(debris_y / 2)][debris_x]

            if current == chr(0) or current == chr(1):
                debris_sprite = 6  # Giant Debris!

            buffer[int(debris_y / 2)][debris_x] = chr(debris_sprite)

        # Draw elapsed seconds
        buffer[0][16 - len(game_time):len(game_time)] = game_time

        for idx, row in enumerate(buffer):
            menu.write_row(idx, ''.join(row))
