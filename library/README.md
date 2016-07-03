# Display-o-Tron 3000

## Installing

We've created a super-easy installation script that will install all pre-requisites and get your Dot3k up and running in a jiffy, just type this into a terminal or LXTerminal:

```bash
curl get.pimoroni.com/dot3k | bash
```

## Usage

### LCD

```python
from dot3k import lcd
lcd.write('Hello World!')
```

### Backlight

```python
from dot3k import backlight
backlight.sweep(0.5)
backlight.update()
```

### Joystick

```python
from dot3k import joystick
@joystick.on(joystick.UP)
def handle_joystick_up(pin):
    print("Joystick up!")
```
