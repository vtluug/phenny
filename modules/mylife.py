#!/usr/bin/python2
"""
mylife.py - various commentary on life
author: Ramblurr <unnamedrambler@gmail.com>
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

from urllib import quote as urlquote
from urllib2 import urlopen, HTTPError
import lxml.html

def fml(phenny, input):
    """.fml"""
    try:
        req = urlopen("http://www.fmylife.com/random")
    except HTTPError:
        phenny.say("I tried to use .fml, but it was broken. FML")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('article')[0][0].text_content()
    phenny.say(quote)
fml.commands = ['fml']

def mlia(phenny, input):
    """.mlia - My life is average."""
    try:
         req = urlopen("http://mylifeisaverage.com/")
    except HTTPError:
        phenny.say("I tried to use .mlia, but it wasn't loading. MLIA")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('story')[0][0].text_content()
    quote = quote.strip()
    phenny.say(quote)
mlia.commands = ['mlia']

def mliarab(phenny, input):
    """.mliarab - My life is Arabic."""
    try:
         req = urlopen("http://mylifeisarabic.com/random/")
    except HTTPError:
        phenny.say("The site you requested, mylifeisarabic.com, has been banned \
                  in the UAE. You will be reported to appropriate authorities")
        return

    doc = lxml.html.parse(req)
    quotes = doc.getroot().find_class('entry')
    quote = random.choice(quotes)[0].text_content()
    quote = quote.strip()
    phenny.say(quote)
mliarab.commands = ['mliar', 'mliarab']

def mlib(phenny, input):
    """.mlib - My life is bro."""
    try:
        req = urlopen("http://mylifeisbro.com/random")
    except HTTPError:
        phenny.say("MLIB is out getting a case of Natty. It's chill.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlib.commands = ['mlib']

def mlic(phenny, input):
    """.mlic - My life is creepy."""
    try:
        req = urlopen("http://mylifeiscreepy.com/random")
    except HTTPError:
        phenny.say("Error: Have you checked behind you?")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('oldlink')[0].text_content()
    quote = quote.strip()
    phenny.say(quote)
mlic.commands = ['mlic']

def mlid(phenny, input):
    """.mlib - My life is Desi."""
    try:
        req = urlopen("http://www.mylifeisdesi.com/random")
    except HTTPError:
        phenny.say("MLID is busy at the hookah lounge, be back soon.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlid.commands = ['mlid']

def mlig(phenny, input):
    """.mlig - My life is ginger."""
    try:
        req = urlopen("http://www.mylifeisginger.org/random")
    except HTTPError:
        phenny.say("Busy eating your soul. Be back soon.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlig.commands = ['mlig']

def mlih(phenny, input):
    """.mlih - My life is ho."""
    try:
        req = urlopen("http://mylifeisho.com/random")
    except HTTPError:
        phenny.say("MLIH is giving some dome to some lax bros.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlih.commands = ['mlih']

def mlihp(phenny, input):
    """.mlihp - My life is Harry Potter."""
    try:
        req = urlopen("http://www.mylifeishp.com/random")
    except HTTPError:
        phenny.say("This service is not available to Muggles.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlihp.commands = ['mlihp']

def mlit(phenny, input):
    """.mlit - My life is Twilight."""
    try:
        req = urlopen("http://mylifeistwilight.com/random")
    except HTTPError:
        phenny.say("Error: Your life is too Twilight. Go outside.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('fmllink')[0].text_content()
    phenny.say(quote)
mlit.commands = ['mlit']

if __name__ == '__main__':
    print __doc__.strip()

