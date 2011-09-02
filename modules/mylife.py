#!/usr/bin/python2
"""
mylife.py - various commentary on life
author: Ramblurr <unnamedrambler@gmail.com>
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
        phenny.say("I tried to use .fml, but it was broken. FML"
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
    quote = doc.getroot().find_class('entry')[0][0].text_content()
    quote = quote.strip()
    phenny.say(quote)
mliarab.commands = ['mliarab']


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

def mlib(phenny, input):
    """.mlib"""
    try:
        req = urlopen("http://mylifeisbro.com/random")
    except HTTPError:
        phenny.say("MLIB is out getting a case of Natty. It's chill.")
        return

    doc = lxml.html.parse(req)
    quote = doc.getroot().find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlib.commands = ['mlib']

if __name__ == '__main__':
    print __doc__.strip()

