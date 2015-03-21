#!/usr/bin/env python
"""
wuvt.py - WUVT now playing module for phenny
"""

from tools import GrumbleError
import web


def wuvt(phenny, input):
    """.wuvt - Find out what is currently playing on the radio station WUVT."""

    try:
        data = web.get('https://www.wuvt.vt.edu/playlists/latest_track',
                       headers={'Accept': "application/json"})
        trackinfo = web.json(data)
    except:
        raise GrumbleError("Failed to fetch current track from WUVT")

    phenny.say("{dj} is currently playing {title} by {artist}".format(
        dj=trackinfo['dj'].strip(),
        title=trackinfo['title'].strip(),
        artist=trackinfo['artist'].strip()))
wuvt.commands = ['wuvt']
wuvt.example = '.wuvt'
