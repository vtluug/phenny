#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
lastfmn.py - lastfm module
author: Casey Link <unnamedrambler@gmail.com>
"""

import random

import configparser, os
import http.client
from urllib.parse import quote as urlquote
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import etree
from datetime import datetime

APIKEY = "f8f2a50033d7385e547fccbae92b2138"
APIURL = "http://ws.audioscrobbler.com/2.0/?api_key="+APIKEY+"&"
AEPURL = "http://www.davethemoonman.com/lastfm/aep.php?format=txt&username="

config = configparser.RawConfigParser()
config.optionxform = str
config_filename = ""

def setup(self):
    fn = self.nick + '-' + self.config.host + '.lastfm.db'
    global config_filename
    config_filename = os.path.join(os.path.expanduser('~/.phenny'), fn)
    if not os.path.exists(config_filename):
        try: f = open(config_filename, 'w')
        except OSError: pass
        else:
            f.write('')
            f.close()

    config_file = config.read(config_filename)
    if not config.has_section("Nick2User"):
        config.add_section("Nick2User")
    if not config.has_section("User2Nick"):
        config.add_section("User2Nick")
    if not config.has_section("Nick2Verb"):
        config.add_section("Nick2Verb")

def lastfm_set(phenny, input):
    cmd = input.group(2)
    if not cmd or len(cmd.strip()) == 0:
        phenny.say("commands: user, verb")
        phenny.say("set <username>: associates your IRC nick with your last.fm username.")
        phenny.say("example: lastfm-set user joebob")
        phenny.say("verb <past>,<present>: customizes the verbs used when displaying your now playing info.")
        phenny.say("example: lastfm-set verb listened to, is listening to")
        return
    if cmd == "user":
        value = input.group(5)
        if len(value) == 0:
            phenny.say("um.. try again. the format is 'lastfm-set user username'")
            return
        set_username(input.nick, value)
        phenny.say("ok, i'll remember that %s is %s on lastfm" % (input.nick, value))
        return
    if cmd == "verb":
        past = input.group(3)
        present = input.group(4)
        if len(past) == 0 or len(present) == 0:
            phenny.say("umm.. try again. the format is 'lastfm-set verb past phrase, present phrase' example: 'lastfm-set verb listened to, listening to'")
            return
        set_verb(input.nick, past, present)
        phenny.say("ok, i'll remember that %s prefers '%s' and '%s'" % (input.nick, past, present))
        return

lastfm_set.rule = (['lastfm-set'], r'(\S+)\s+(?:(.*?),(.*)|(\S+))')

def now_playing(phenny, input):
    nick = input.nick
    user = ""
    arg = input.group(2)
    if not arg or len(arg.strip()) == 0:
        user = resolve_username(nick) # use the sender
        if not user: #nick didnt resolve
            user = nick
    else: # use the argument
        user = resolve_username(arg.strip())
        if not user: # user didnt resolve
            user = arg
    user = user.strip()
    try:
        req = urlopen("%smethod=user.getrecenttracks&user=%s" % (APIURL, urlquote(user)))
    except HTTPError as e:
        if e.code == 400:
            phenny.say("%s doesn't exist on last.fm, perhaps they need to set user" % (user))
            return
        else:
            phenny.say("uhoh. try again later, mmkay?")
            return
    except http.client.BadStatusLine:
        phenny.say("uhoh. try again later, mmkay?")
        return
    doc = etree.parse(req)
    root = doc.getroot()
    recenttracks = list(root)
    if len(recenttracks) == 0:
        phenny.say("%s hasn't played anything recently. this isn't you? try lastfm-set" % (user))
        return
    tracks = list(recenttracks[0])
    #print(etree.tostring(recenttracks[0]))
    if len(tracks) == 0:
        phenny.say("%s hasn't played anything recently. this isn't you? try lastfm-set" % (user))
        return
    first = tracks[0]
    now = True if first.get("nowplaying") == "true" else False
    tags = {}
    for e in first.getiterator():
        tags[e.tag] = e

    track = tags['name'].text.strip()

    artist = tags['artist'].text.strip()

    album = "unknown"
    if tags['album'].text:
        album = tags['album'].text

    date = None
    stamp = None
    if not now:
        date = tags['date'].get("uts")
        stamp = int(date)

    if now:
        present = get_verb(nick)[1]
        phenny.say("%s %s \"%s\" by %s on %s" %(user.strip(), present.strip(), track, artist, album ))
        return
    else:
        past = get_verb(nick)[0]
        phenny.say("%s %s \"%s\" by %s on %s %s" %(user.strip(), past.strip(), track, artist, album, pretty_date(stamp)))

now_playing.commands = ['np']

def tasteometer(phenny, input):
    input1 = input.group(2)
    if not input1 or len(input1) == 0:
        phenny.say("tasteometer: compares two users' musical taste")
        phenny.say("syntax: .taste user1 user2")
        return
    input2 = input.group(3)
    user1 = resolve_username(input1)
    if not user1:
        user1 = input1
    user2 = resolve_username(input2)
    if not user2:
        user2 = input2
    if not user2 or len(user2) == 0:
        user2 = resolve_username(input.nick)
        if not user2:
            user2 = input.nick
    try:
        req = urlopen("%smethod=tasteometer.compare&type1=user&type2=user&value1=%s&value2=%s" % (APIURL, urlquote(user1), urlquote(user2)))
    except (HTTPError, http.client.BadStatusLine) as e:
        if e.code == 400:
            phenny.say("uhoh, someone doesn't exist on last.fm, perhaps they need to set user")
            return
        else:
            phenny.say("uhoh. try again later, mmkay?")
            return
    doc = etree.parse(req)
    root = doc.getroot()
    score = root.xpath('comparison/result/score')
    if len(score) == 0:
        phenny.say("something isn't right. have those users scrobbled?")
        return

    score = float(score[0].text)
    rating = ""
    if score >= 0.9:
        rating = "Super"
    elif score >= 0.7:
        rating = "Very High"
    elif score >= 0.5:
        rating = "High"
    elif score >= 0.3:
        rating = "Medium"
    elif score >= 0.1:
        rating = "Low"
    else:
        rating = "Very Low"

    artists = root.xpath("comparison/result/artists/artist/name")
    common_artists = ""
    names = []
    if len(artists) == 0:
        common_artists = ". they don't have any artists in common."
    else:
        list(map(lambda a: names.append(a.text) ,artists))
        common_artists = "and music they have in common includes: %s" % ", ".join(names)

    phenny.say("%s's and %s's musical compatibility rating is %s %s" % (user1, user2, rating, common_artists))

tasteometer.rule = (['taste'], r'(\S+)(?:\s+(\S+))?')

def save_config():
    configfile  = open(config_filename, 'w')
    config.write(configfile)
    configfile.close()

def set_verb(nick, past, present):
    verbs = "%s,%s" % (past,present)
    config.set("Nick2Verb", nick, verbs )
    save_config()

def get_verb(nick):
    if config.has_option("Nick2Verb", nick):
        return config.get("Nick2Verb", nick).split(',')
    return ["listened to","is listening to"]

def set_username(nick, username):
    old_user = resolve_username(nick)
    if old_user:
        config.remove_option("User2Nick", old_user)
    config.set("Nick2User", nick, username)
    config.set("User2Nick", username, nick)
    save_config()

def resolve_username(nick):
    if config.has_option("Nick2User", nick):
        return config.get("Nick2User", nick)
    return None

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( second_diff // 60 ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( second_diff // 3600 ) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago"
    return str(day_diff // 365) + " years ago"

if __name__ == '__main__':
    print(__doc__.strip())
