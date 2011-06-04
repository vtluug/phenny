#!/usr/bin/env python
"""
halbot.py - A module to connect to Halpy AI module
Copyright (c) 2011 Dafydd Crosby - http://www.dafyddcrosby.com

Licensed under the Eiffel Forum License 2.
"""
from megahal import *
megahal = MegaHAL()

def learn(phenny,input):
    """Listens in on the room, gradually learning new phrases"""
    megahal.learn(input.group())
learn.rule = r'(.*)'
learn.priority = 'low'

def megahalbot(phenny, input):
    """Responds when someone mentions the bot nickname"""
    # Clean the input so Halpy does not get confused
    inp = input.group().replace(phenny.nick,'')
    inp = inp.replace("\'","")
    inp = inp.replace("\"","")

    phenny.say(input.nick + ": " + megahal.get_reply(inp))
    megahal.sync()
megahalbot.rule = r'(.*)$nickname(.*)'
megahalbot.priority = 'low'
