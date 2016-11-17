#Understanding Bitmaps

The character LCD display consists of a grid of cursor positions and each cursor position consists of a grid of pixels. Any supported character can be written to any cursor position, but how do you create new characters that aren't built into the LCD?

The answer is that you have to define exactly which pixels within a single character position grid should be on and which should be off. This type of LCD does not support greyscale or colored pixels.

First get yourself some graph paper, or open a spreadsheet program and resize the columns and rows to the same size so you have a grid of squares. Notice that on the LCD there are three rows of rectangles, look more closely and notice that each rectangle is made up eight rows of squares, five across.

On your graph paper, draw out your pictures using eight rows of five squares across for each picture. Each square can either be black or white, on or off.

The easiest way to represent this in python is to convert eight character strings to integers using base two. Create strings as a sequence of five ones and zeros using one to represent the black squares and zero to represent the white squares. Convert the strings to integers using the int function, with a parameter to indicate that the strings are base two (i.e. binary, ones and zeros). Arrange the strings into a list with each string of five bits representing one row in one rectangle on the LCD. The five bits will actually be interpreted by Python as the rightmost five bits in each byte (a byte is eight bits) with one byte per row of the character position.

The pacman image is represented here:

```python
pacman = [
[0x0e, 0x1f, 0x1d, 0x1f, 0x18, 0x1f, 0x1f, 0x0e],
[0x0e, 0x1d, 0x1e, 0x1c, 0x18, 0x1c, 0x1e, 0x0f]
]
```

in condensed form using hexadecimal (base sixteen), but base two (binary) is easier to visualize. Here's an example of a static (non-animated) bitmap:

```python
char_map_pacman = [
int('01110', 2),
int('11111', 2),
int('11101', 2),
int('11111', 2),
int('11000', 2),
int('11111', 2),
int('11111', 2),
int('01110', 2),
]
```

And for an animation you would use a list of lists, so each frame is a list of eight strings of eight bits.

```python
anim_map_pacman = [
[ # Frame 1
int('01110', 2),
int('11111', 2),
int('11101', 2),
int('11111', 2),
int('11000', 2),
int('11111', 2),
int('11111', 2),
int('01110', 2),
],
[ # Frame 2
int('01110', 2),
int('11101', 2),
int('11110', 2),
int('11100', 2),
int('11000', 2),
int('11100', 2),
int('11110', 2),
int('01111', 2),
],
# Add more frames as needed, a list of eight integers per frame
]
```
