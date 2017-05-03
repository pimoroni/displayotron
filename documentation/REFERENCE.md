# Display-o-tron Function Reference

## LCD

For Display-o-Tron HAT:

```python
from dothat import lcd
```

For Display-o-Tron 3000:

```python
from dot3k import lcd
```

### Methods

```python
lcd.write(value)
```
Writes a string to the LCD at the current cursor position.

You can use chr(0) to chr(7) to place custom characters and animations.

* value (string): The string to write

```python
lcd.clear()
```
Clears the display

```python
lcd.set_contrast(contrast)
```
Sets the display contrast

* contrast (int): contrast value
* Must be in the range 0 to 63

```python
lcd.set_cursor_position(column, row)
```
Sets the cursor position to column,row

* column (int): column ( horizontal ) position from 0 to 15
* row (int): row ( vertical ) position from 0 to 2

```python
lcd.set_cursor_offset(offset)
```
Sets the cursor position in DRAM

* offset (int): DRAM offset to place cursor

```python
lcd.set_display_mode(enable, cursor, blink)
```
Sets the display mode

* enable (boolean): enable display output
* cursor (boolean): show cursor
* blink (boolean): blink cursor (if shown)

```python
lcd.create_char(char_pos, char_map)
```
Create a custom character and save into dot3k memory.

* char_pos (int): Value from 0-7
* char_map (list): LIst of 8, 8-bit integers describing the character

```python
lcd.create_animation(anim_pos, anim_map, frame_rate):
```
Create a custom animation. These are saved in the same memory locations as characters and will overwrite a slot used by create_char.

* char_pos (int): Value from 0-7, to save animation in dot3k memory
* anim_map (list): List of 8, 8-bit integers describing the animation
* frame_rate (int): Animation speed in FPS

```python
lcd.update_animations()
```
Advances all animations by one frame- this updates the character corresponding to each animation with the correct frame.

## Backlight

For Display-o-Tron HAT:

```python
from dothat import backlight
```

For Display-o-Tron 3000:

```python
from dot3k import backlight
```

### Methods

```python
backlight.use_rbg()
```
Applies to the Dot3k only. Changes the backlight driver to RBG mode ( instead of RGB ) for early Display-o-Tron boards with reversed B/G channels. Call once after importing dot3k.backlight.

```python
backlight.hue(hue)
```
Sets the backlight LEDs to supplied hue

* hue (float): hue value between 0.0 and 1.0

```python
backlight.hue_to_rgb(hue)
```
Converts a hue to RGB brightness values

* hue (float): hue value between 0.0 and 1.0

```python
backlight.left_hue(hue)
```
Set the left backlight to supplied hue

* hue (float): hue value between 0.0 and 1.0

```python
backlight.left_rgb(r, g, b)
```
Set the left backlight to supplied r, g, b colour. Will set the left-most two LEDs on DotHAT.

* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
backlight.mid_hue(hue)
```
Set the middle backlight to supplied hue. Will set the middle two LEDs on DotHAT.

* hue (float): hue value between 0.0 and 1.0

```python
backlight.mid_rgb(r, g, b)
```
Set the middle backlight to supplied r, g, b colour. Will set the right-most two LEDs on DotHAT.

* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
backlight.off()
```
Turns off the backlight.

```python
backlight.rgb(r, g, b)
```
Sets all backlights to supplied r, g, b colour

* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
backlight.right_hue(hue)
```
Set the right backlight to supplied hue

* hue (float): hue value between 0.0 and 1.0

```python
backlight.right_rgb(r, g, b)
```
Set the right backlight to supplied r, g, b colour

* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
backlight.single_rgb(index, r, g, b)
```
Set a specific backlight supplied r, g, b colour.

* index (int): index of the LED from 0 to 5 (or 0 to 2 on Dot3k)
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
backlight.set(index, value)
```
Set a specific LED to a value

* index (int): index of the LED from 0 to 18
* value (int): brightness value from 0 to 255

```python
backlight.set_bar(index, value)
```
Set a value or values to one or more LEDs

* index (int): starting index
* value (int or list): a single int, or list of brightness values from 0 to 255

```python
backlight.set_graph(value)
```
Lights a number of bargraph LEDs depending upon value

* value (float): percentage between 0.0 and 1.0

```python
backlight.sweep(hue, range)
```
Sets the backlight LEDs to a gradient centred on supplied hue

Supplying zero to range would be the same as hue()

* hue (float): hue value between 0.0 and 1.0
* range (float): range value to deviate the left and right hue

```python
backlight.update()
```
Update backlight with changes to the LED buffer

## Touch

For Display-o-Tron HAT only:

```python
from dothat import touch
```

### Constants

Constants are defined for all the buttons, giving them friendly names like so:

```python
touch.UP
touch.DOWN
touch.LEFT
touch.RIGHT
touch.BUTTON
touch.CANCEL
```

### Methods

```python
touch.high_sensitivity()
```

Call once to enable high sensitivty mode.

```python
touch.enable_repeat(enable)
```

Pass true to enable repeat events (held buttons will re-trigger).

* enable (boolean): enable or disable repeat

```python
touch.on(buttons, bounce=1)
```

Used as a decorator to bind a function to a particular button, you should generally use it like so:

```
@touch.on(touch.LEFT)
def touch_left(channel, event):
    print(channel, event)
```

* buttons - list of, or single, button constant, one of: touch.UP, touch.DOWN, ... etc

```python
touch.bind_defaults(menu)
```

Pass an instance of a dot3k.menu class to bind all the default functions automatically for each button. This is much neater than creating your own button handlers. Binds Up, Down, Left, Right, Menu and Cancel.
