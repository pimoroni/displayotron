# Display-o-Tron HAT Examples

Display-o-Tron HAT is the HAT version of Display-o-Tron 3000, it replaces the 3 zone RGB backlight with a whopping 6 zones, sports a 6-LED vertical bargraph and has 6 touch sensitive buttons in place of the joystick.

## Using The Touch Buttons

The example file `basic/captouch.py` demonstrates how you can use the new `captouch` library to get touch input into your projects. It's almost a drop-in replacement for the `joystick` library except that it includes one new button: `cancel`.

`cancel` is the touch button on the top left of Display-o-Tron HAT and is used for exiting menus that want to make full use of the up/down/left/right/select buttons. 

## Touch Reference

#### Import The Library

```python
import dothat.touch
```

#### Enable/disable auto-repeat

```python
dothat.touch.enable_repeat()
```

#### Enable High-Sensitivity mode

Great for using the touch buttons through a lid:

```python
dothat.touch.high_sensitivity()
```

#### Bind menu defaults

Bind all the default actions to a `dot3k.menu` instance:

```python
dothat.touch.bind_defaults(my_custom_menu)
```

#### Bind a single action

```python
@dothat.touch.on(dothat.touch.LEFT)
def handle_left(channel, event):
    print("Left Pressed!")
```

`channel` will be a number from 0 to 5 corresponding to `dothat.touch.LEFT/UP/DOWN/etc`

`event` will either be `press` or `held` depending on whether an initial touch has been detected, or a continuous hold.

## Using The Backlight

The backlight works in exactly the same was as it did on Display-o-Tron 3000, however it now has 6 zones instead of 3, for 100% more rainbow.

The methods `left_rgb`, `mid_rgb` and `right_rgb` still work, however they each control two LEDs instead of one. The recommended way to set a single RGB channel ( from 0 to 5 ) is now `single_rgb( channel, r, g, b )`.

## Backlight Reference

#### Import The Library

```python
import dothat.backlight
```

#### Set a single RGB LED

Set a single channel to an RGB colour of your choice:

```python
dothat.backlight.single_rgb(channel, r, g, b)
```

`channel` should be a number between 0 and 5, where 0 is the left-most RGB LEd and 5 is the right-most.

`r`, `g` and `b` should be numbers between 0 and 255, representing the intensity of red, green and blue light respectively.

#### Set all RGB LEDs

Set all channels to the same RGB colour:

```python
dothat.backlight.rgb(r,g,b)
```

Again, `r`, `g`, and `b` should be numbers between 0 and 255. `255,0,255` would be a lovely purple!

#### Turn all LEDS off

```python
dothat.backlight.off()
```

#### Display a percentage on the 6-LED graph

```python
dothat.backlight.set_graph(0.5) # 50%
```

Pass a number between 0 and 1 to set all the graph LEDs either on, off, or somewhere in between.

#### Set a single LED

```python
dothat.backlight.set(channel, brightness)
```

`channel` should be a value from 0 to 18. The LED channels go in the order: `bgrbgrbgrbgrbgrbgr`
