from dothat import lcd
from dothat import backlight
import time

backlight.rgb(0,255,255)
lcd.clear()
lcd.set_contrast(50)

while True:
    tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    tempF = str(tempC)
    lcd.set_cursor_position(0, 0)
    lcd.write(tempF)
    time.sleep(1)
