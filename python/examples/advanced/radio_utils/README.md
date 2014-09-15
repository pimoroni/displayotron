Dot3k Radio Utilities
=====================

volume
------

A simple bash script for changing volume via amixer:

    ./volume 80

control
-------

This utility will allow you to play, pause or stop the radio.

Usage
-----

    ./control play/pause/stop

playstream
----------

This utility will load your radio channel list and let you play any of your feeds, or a totally arbitrary one!

If you play one of your existing streams, Dot3k should update to show the current playing feed.

Usage
-----

  ./playstream <stream number>

or

  ./playstream <stream name>

or

  ./playstream http://feedurl/feed
