#!/usr/bin/env bash
su pi -c "/usr/bin/vlc -I rc --rc-fake-tty --rc-host=127.0.0.1:9393 > /dev/null" > /dev/null &
sleep 0.5
su pi -c "/bin/pidof vlc"
