#!/usr/bin/env python
"""
wuvt.py - Phenny WUVT Module
Copyright 2012, Randy Nance, randynance.info

http://github.com/randynobx/phenny/
"""

from urllib.error import URLError, HTTPError
from tools import GrumbleError
import re
import web

re.MULTILINE
r_play = re.compile(r'^(.*?) - (.*?)$')
r_dj = re.compile(r'Current DJ: </span>\n(.+?)<')

def wuvt(phenny, input) :
    try:
        playing = web.get('http://www.wuvt.vt.edu/playlists/latest_track.php')
        djpage = web.get('http://www.wuvt.vt.edu/playlists/current_dj.php')
    except (URLError, HTTPError):
        raise GrumbleError('Cannot connect to wuvt')
    play= r_play.search(playing)
    song = play.group(2)
    artist = play.group(1)
    dj = r_dj.search(djpage).group(1)

    if song and artist:
        phenny.reply('DJ {0} is currently playing: {1} by {2}'
                .format(dj.strip(), song.strip(), artist.strip()))
    else:
        phenny.reply('Cannot connect to wuvt')
wuvt.commands = ['wuvt']
