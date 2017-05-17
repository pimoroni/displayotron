from sys import exit

try:
    import st7036
except ImportError:
    exit("This library requires the st7036 module\nInstall with: sudo pip install st7036")


ROWS = 3
COLS = 16

lcd = st7036.st7036(register_select_pin=25)
lcd.clear()


def write(value):
    """Write a string to the current cursor position.

    :param value: The string to write
    """

    lcd.write(value)


def clear():
    """Clear the display and reset the cursor."""

    lcd.clear()


def set_contrast(contrast):
    """Set the display contrast.

    Raises TypeError if contrast is not an int
    Raises ValueError if contrast is not in the range 0..0x3F

    :param contrast: contrast value

    """

    lcd.set_contrast(contrast)


def set_display_mode(enable=True, cursor=False, blink=False):
    """Set the display mode.

    :param enable: enable display output: True/False
    :param cursor: show cursor: True/False
    :param blink: blink cursor (if shown): True/False

    """

    lcd.set_display_mode(enable, cursor, blink)


def set_cursor_offset(offset):
    """Set the cursor position in DRAM

    :param offset: DRAM offset to place cursor

    """

    lcd.set_cursor_offset(offset)


def set_cursor_position(column, row):
    """Set the cursor position in DRAM

    Calculates the cursor offset based on a row and column offset.

    Raises ValueError if row and column are not within defined screen size

    :param column: column to move the cursor to
    :param row: row to move the cursor to

    """

    lcd.set_cursor_position(column, row)


def create_animation(anim_pos, anim_map, frame_rate):
    """Create an animation in a given custom character slot

    Each definition should be a list of 8 bytes describing the custom character for that frame,

    :param anim_pos: Character slot from 0 to 7 to store animation
    :param anim_map: A list of custom character definitions
    :param frame_rate: Speed of animation in frames-per-second

    """

    lcd.create_animation(anim_pos, anim_map, frame_rate)


def update_animations():
    """Update animations onto the LCD

    Uses wall time to figure out which frame is current for
    each animation, and then updates the animations character
    slot to the contents of that frame.

    Only one frame, the current one, is ever stored on the LCD.

    """

    lcd.update_animations()


def create_char(char_pos, char_map):
    """Create a character in the LCD memory

    The st7036 has 8 slots for custom characters.

    A char is defined as a list of 8 integers with the
    upper 5 bits setting the state of each row of pixels.

    Note: These slots are also used for animations!

    :param char_pos: Char slot to use (0-7)
    :param char_map: List of 8 integers containing bitmap

    """

    lcd.create_char(char_pos, char_map)
