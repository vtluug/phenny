#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
wargame.py - wargame module for the vtluug wargame
http://wargame.vtluug.org
author: Casey Link <unnamedrambler@gmail.com>
"""

import random

import configparser, os
from urllib.parse import quote as urlquote
from urllib.request import urlopen
from urllib.error import HTTPError
from lxml import etree
from lxml import objectify
from datetime import datetime
import re


APIURL = "http://wargame.vtluug.org/scoreboard.xml"

class server(object):
    def __init__(self, name):
        self.name = name
        self.players = []
    def __str__(self):
        s = "%s - %d players: " %(self.name, len(self.players))
        s += ", ".join([str(p) for p in self.players])
        return s

class player(object):
    def __init__(self, name):
        self.name = name
        self.score = "-1"
        self.isOwner = False
    def __str__(self):
        return "%s%s: %s points" %(self.name, " (Current King)" if self.isOwner else "", self.score)
    def __cmp__(self, other):
        if int(self.score) < int(other.score):
            return -1
        elif int(self.score) == int(other.score):
            return 0
        else:
            return 1


def parse_player(player_element):
    p = player( player_element.attrib.get("name") )
    p.score = player_element.attrib.get("score")
    p.isOwner = player_element.attrib.get("isOwner") == "True"
    return p

def parse_server(server_element):
    s = server( server_element.name.text )
    for player_e in server_element.players.player:
            s.players.append( parse_player( player_e ) )
    s.players.sort()
    s.players.reverse()
    return s

def wargame(phenny, input):

    if input.group(2) is not None:
        rest = input.group(2)
        m = re.match("^scores\s+(\S+)\s*$",rest)
        if m is not None and len( m.groups() )  == 1:
            return wargame_scores(phenny, m.group(1))
        m = re.match("^scores\s*$",rest)
        if m is not None:
            return wargame_scores(phenny, "Total")
        m = re.match("^help\s*$",rest)
        if m is not None:
            phenny.say("VTLUUG King of the Root - http://wargame.vtluug.org'")
            phenny.say("syntax: '.wargame' to see network status and target list'")
            phenny.say("syntax: '.wargame scores <target name>' to get current scores for a target'")
            return
        else:
            phenny.say("hmm.. I don't know what you mean. try '.wargame help'")
            return
    try:
        req = urlopen(APIURL)
    except HTTPError as e:
            phenny.say("uhoh. try again later, mmkay?")
            return
    root = objectify.parse(req).getroot()
    online = root.attrib.get("online") == "True"
    updated = root.attrib.get("updated")

    servers = []
    for server_e in root.servers.server:
        servers.append( parse_server( server_e ) )

    phenny.say( "wargame network is %s. last updated %s. available targets: %s" % ( "ONLINE" if online else "OFFLINE", updated, ", ".join([s.name for s in servers])) )
def wargame_scores(phenny, s_name):
    try:
        req = urlopen(APIURL)
    except HTTPError as e:
            phenny.say("uhoh. try again later, mmkay?")
            return
    root = objectify.parse(req).getroot()
    online = root.attrib.get("online") == "True"
    updated = root.attrib.get("updated")

    servers = {}
    for server_e in root.servers.server:
        s = parse_server( server_e )
        servers[s.name] = s
    if not s_name in servers:
        phenny.say("sorry, i couldn't find %s" % ( s_name ))
        return

    phenny.say( str(servers[s_name]) )


wargame.commands = ['wargame']