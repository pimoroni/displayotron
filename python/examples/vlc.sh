#!/usr/bin/env bash
su pi -c "/usr/bin/vlc $1 $2 $3 > /dev/null" > /dev/null &
su pi -c "/bin/pidof vlc"
