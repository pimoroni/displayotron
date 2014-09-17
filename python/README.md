# dot3k

## Hardware Requirements

You'll need to enable spi.

```bash
sudo raspi-config
```

Then head into `Advanced Options -> SPI -> Yes`.

And i2c.

```bash
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```

And comment out (place a `#` before):

```
blacklist i2c-bcm2708
```

And also:

```bash
sudo nano /etc/modules
```

Add the line:
   
```
i2c-dev
```

Reboot to make these changes take effect:

```bash
sudo reboot
```

## Software Requirements

Next you should install python-smbus and python-dev via apt:

```bash
sudo apt-get install python-smbus python-dev
```

And pip, if you don't have it:

```bash
sudo apt-get install python-pip
```

Then install st7036 and sn3218 using pip:

```bash
sudo pip install st7036 sn3218
```

You can run the `requirements.sh` file to do this for you!

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
