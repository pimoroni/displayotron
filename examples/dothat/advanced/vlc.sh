#!/usr/bin/env bash

su pi -c "/usr/bin/vlc -I rc --rc-fake-tty --rc-host=0.0.0.0:9393 > /dev/null" > /dev/null &
sleep 0.5
su pi -c "/bin/pidof vlc"
