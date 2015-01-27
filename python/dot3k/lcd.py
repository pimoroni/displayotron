import st7036

lcd = st7036.st7036(register_select_pin=25)
lcd.clear()

def write(value):
    """Write a string to the current cursor position.

    Args:
        value (string): The string to write
    """
    lcd.write(value)
    
def clear():
    """Clears the display and resets the cursor."""    
    lcd.clear()
    
def set_contrast(contrast):
    """Sets the display contrast.

    Args:
        contrast (int): contrast value
    Raises:
        TypeError: if contrast is not an int
        ValueError: if contrast is not in the range 0..0x3F
    """     
    lcd.set_contrast(contrast)
    
def set_display_mode(enable=True, cursor=False, blink=False):
    """Sets the display mode.

    Args:
        enable (boolean): enable display output
        cursor (boolean): show cursor
        blink (boolean): blink cursor (if shown)
    """
    lcd.set_display_mode(enable, cursor, blink)
    
def set_cursor_offset(offset):
    """Sets the cursor position in DRAM

    Args:
        offset (int): DRAM offset to place cursor
    """    
    lcd.set_cursor_offset(offset)
    
def set_cursor_position(column, row):
    """Sets the cursor position in DRAM based on a row and column offset.

    Args:
        column (int): column to move the cursor to
        row (int): row to move the cursor to
    Raises:
     ValueError: if row and column are not within defined screen size
    """
    lcd.set_cursor_position(column, row)
    
def create_animation(anim_pos, anim_map, frame_rate):
    """Create a custom animation. These are saved in the same memory locations as custom characters.

    Args:
        char_pos (int): Value from 0-7, to save anim in dot3k memory
        anim_map (list): List of (List of 8, 8-bit integers describing the character)
        frame_rate (int): Animation speed in frames-per-second
    """
    lcd.create_animation(anim_pos, anim_map, frame_rate)
    
def update_animations():
    """Advances all registered animations by one frame."""
    lcd.update_animations()
    
def create_char(char_pos, char_map):
    """Create a custom character.
    
    Args:
        char_pos (int): Value from 0-7, to save char in dot3k memory
        char_map (list): List of 8, 8-bit integers describing the character
    """
    lcd.create_char(char_pos, char_map)
