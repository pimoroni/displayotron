
#Backlight

###hue(hue)
Sets the backlight LEDs to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

###hue_to_rgb(hue)
Converts a hue to RGB brightness values

**Args**
* hue (float): hue value between 0.0 and 1.0

###left_hue(hue)
Set the left backlight to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

###left_rgb(r, g, b)
Set the left backlight to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

###mid_hue(hue)
Set the middle backlight to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

###mid_rgb(r, g, b)
Set the middle backlight to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

###off()
Turns off the backlight.

###rgb(r, g, b)
Sets all backlights to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

###right_hue(hue)
Set the right backlight to supplied hue

**Args**
* hue (float): hue value between 0.0 and 1.0

###right_rgb(r, g, b)
Set the right backlight to supplied r, g, b colour

**Args**
* r (int): red value between 0 and 255
* g (int): green value between 0 and 255
* b (int): blue value between 0 and 255

###set(index, value)
Set a specific LED to a value

**Args**
* index (int): index of the LED from 0 to 18
* value (int): brightness value from 0 to 255

###set_bar(index, value)
Set a value or values to one or more LEDs

**Args**
* index (int): starting index
* value (int or list): a single int, or list of brightness values from 0 to 255

###set_graph(value)
Lights a number of bargraph LEDs depending upon value

**Args**
* value (float): percentage between 0.0 and 1.0
