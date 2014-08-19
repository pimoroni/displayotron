import st7036
import numpy
import time

st7036 = st7036.st7036(register_select_pin=25)

st7036.clear()

char_w = 5
char_h = 8

buffer = numpy.array([[0]*(16*char_w)]*(3*char_h))

buffer[3,0] = 1
buffer[4,5] = 1
buffer[4,6] = 1
buffer[4,8] = 1
buffer[23,79] = 1
buffer[10,10] = 1
buffer[11,11] = 1
buffer[12,12] = 1

while True:
    for y in range(0,3):
        for x in range(0,2):
            st7036.set_cursor_position((x*8),y)
            for c in range(0, 8):

                b_y = (y*char_h)
                b_x = ((x*8)+c)*5

                p = buffer[b_y:b_y+char_h, b_x:b_x+char_w]

                portion = []

                for row in p:
                    r = 0
                    if row[4]: r = r + 1
                    if row[3]: r = r + 2
                    if row[2]: r = r + 4
                    if row[1]: r = r + 8
                    if row[0]: r = r + 16
                    portion.append( r )

                if portion == [0]*8:
                    st7036.write(' ')
                else:
                    st7036.create_char(c, portion)
                    st7036.set_cursor_position(0,0)
                    st7036.set_cursor_position((x*8)+c,y)
                    st7036.write(chr(c))
            time.sleep(0.1)
