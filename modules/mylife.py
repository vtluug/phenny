#!/usr/bin/python3
"""
mylife.py - various commentary on life
author: Ramblurr <unnamedrambler@gmail.com>
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

from urllib.error import HTTPError
import web
import lxml.html

def fml(phenny, input):
    """.fml"""
    try:
        req = web.get("http://www.fmylife.com/random")
    except (HTTPError, IOError):
        phenny.say("I tried to use .fml, but it was broken. FML")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('article')[0][0].text_content()
    phenny.say(quote)
fml.commands = ['fml']

def mlia(phenny, input):
    """.mlia - My life is average."""
    try:
         req = web.get("http://mylifeisaverage.com/")
    except (HTTPError, IOError):
        phenny.say("I tried to use .mlia, but it wasn't loading. MLIA")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('story')[0][0].text_content()
    quote = quote.strip()
    phenny.say(quote)
mlia.commands = ['mlia']

def mlib(phenny, input):
    """.mlib - My life is bro."""
    try:
        req = web.get("http://mylifeisbro.com/random")
    except (HTTPError, IOError):
        phenny.say("MLIB is out getting a case of Natty. It's chill.")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlib.commands = ['mlib']

def mlid(phenny, input):
    """.mlib - My life is Desi."""
    try:
        req = web.get("http://www.mylifeisdesi.com/random")
    except (HTTPError, IOError):
        phenny.say("MLID is busy at the hookah lounge, be back soon.")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlid.commands = ['mlid']

def mlig(phenny, input):
    """.mlig - My life is ginger."""
    try:
        req = web.get("http://www.mylifeisginger.org/random")
    except (HTTPError, IOError):
        phenny.say("Busy eating your soul. Be back soon.")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlig.commands = ['mlig']

def mlih(phenny, input):
    """.mlih - My life is ho."""
    try:
        req = web.get("http://mylifeisho.com/random")
    except (HTTPError, IOError):
        phenny.say("MLIH is giving some dome to some lax bros.")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlih.commands = ['mlih']

def mlihp(phenny, input):
    """.mlihp - My life is Harry Potter."""
    try:
        req = web.get("http://www.mylifeishp.com/random")
    except (HTTPError, IOError):
        phenny.say("This service is not available to Muggles.")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlihp.commands = ['mlihp']

def mlit(phenny, input):
    """.mlit - My life is Twilight."""
    try:
        req = web.get("http://mylifeistwilight.com/random")
    except (HTTPError, IOError):
        phenny.say("Error: Your life is too Twilight. Go outside.")
        return

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('fmllink')[0].text_content()
    phenny.say(quote)
mlit.commands = ['mlit']

if __name__ == '__main__':
    print(__doc__.strip())
