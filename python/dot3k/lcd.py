import st7036

lcd = st7036.st7036(register_select_pin=25)
lcd.clear()

write = lcd.write
clear = lcd.clear
set_contrast = lcd.set_contrast
set_display_mode = lcd.set_display_mode
set_cursor_offset = lcd.set_cursor_offset
set_cursor_position = lcd.set_cursor_position
create_animation = lcd.create_animation
update_animations = lcd.update_animations
create_char = lcd.create_char
