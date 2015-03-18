#LCD

```python
write(value)
```
Writes a string to the LCD at the current cursor position.

You can use chr(0) to chr(7) to place custom characters and animations.

**Args**
* value (string): The string to write

```python
clear()
```
Clears the display

```python
set_contrast(contrast)
```
Sets the display contrast

**Args**
* contrast (int): contrast value
* Must be in the range 0 to 63

```python
set_cursor_position(column, row)
```
Sets the cursor position to column,row

**Args**
* column (int): column ( horizontal ) position from 0 to 15
* row (int): row ( vertical ) position from 0 to 2

```python
create_char(char_pos, char_map)
```
Create a custom character and save into dot3k memory.

**Args**
* char_pos (int): Value from 0-7
* char_map (list): LIst of 8, 8-bit integers describing the character

```python
create_animation(anim_pos, anim_map, frame_rate):
```
Create a custom animation. These are saved in the same memory locations as characters and will overwrite a slot used by create_char.

**Args**
* char_pos (int): Value from 0-7, to save animation in dot3k memory
* anim_map (list): List of 8, 8-bit integers describing the animation
* frame_rate (int): Animation speed in FPS

```python
update_animations()
```
Advances all animations by one frame- this updates the character corresponding to each animation with the correct frame.

#Backlight

```python
use_rbg()
```
Changes the backlight driver to RBG mode ( instead of RGB ) for early Display-o-Tron boards with reversed B/G channels. Call once after importing dot3k.backlight.

```python
hue(hue)
```
Sets the backlight LEDs to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

```python
hue_to_rgb(hue)
```
Converts a hue to RGB brightness values

**Args**
* hue (float): hue value between 0.0 and 1.0

```python
left_hue(hue)
```
Set the left backlight to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

```python
left_rgb(r, g, b)
```
Set the left backlight to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
mid_hue(hue)
```
Set the middle backlight to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

```python
mid_rgb(r, g, b)
```
Set the middle backlight to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
off()
```
Turns off the backlight.

```python
rgb(r, g, b)
```
Sets all backlights to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
right_hue(hue)
```
Set the right backlight to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

```python
right_rgb(r, g, b)
```
Set the right backlight to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

```python
set(index, value)
```
Set a specific LED to a value

**Args**
* index (int): index of the LED from 0 to 18
* value (int): brightness value from 0 to 255

```python
set_bar(index, value)
```
Set a value or values to one or more LEDs

**Args**
* index (int): starting index
* value (int or list): a single int, or list of brightness values from 0 to 255

```python
set_graph(value)
```
Lights a number of bargraph LEDs depending upon value

**Args**
* value (float): percentage between 0.0 and 1.0
