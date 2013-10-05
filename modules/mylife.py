#!/usr/bin/python3
"""
mylife.py - various commentary on life
author: Ramblurr <unnamedrambler@gmail.com>
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from tools import GrumbleError
import web
import lxml.html


def fml(phenny, input):
    """.fml - Grab something from fmylife.com."""
    try:
        req = web.get("http://www.fmylife.com/random")
    except:
        raise GrumbleError("I tried to use .fml, but it was broken. FML")

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('article')[0][0].text_content()
    phenny.say(quote)
fml.commands = ['fml']


def mlia(phenny, input):
    """.mlia - My life is average."""
    try:
         req = web.get("http://mylifeisaverage.com/")
    except:
        raise GrumbleError("I tried to use .mlia, but it wasn't loading. MLIA")

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('story')[0][0].text_content()
    quote = quote.strip()
    phenny.say(quote)
mlia.commands = ['mlia']


def mlib(phenny, input):
    """.mlib - My life is bro."""
    try:
        req = web.get("http://mylifeisbro.com/random")
    except:
        raise GrumbleError("MLIB is out getting a case of Natty. It's chill.")

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlib.commands = ['mlib']


def mlig(phenny, input):
    """.mlig - My life is ginger."""
    try:
        req = web.get("http://www.mylifeisginger.org/random")
    except:
        raise GrumbleError("Busy eating your soul. Be back soon.")

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlig.commands = ['mlig']


def mlih(phenny, input):
    """.mlih - My life is ho."""
    try:
        req = web.get("http://mylifeisho.com/random")
    except:
        raise GrumbleError("MLIH is giving some dome to some lax bros.")

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('storycontent')[0][0].text_content()
    phenny.say(quote)
mlih.commands = ['mlih']


def mlihp(phenny, input):
    """.mlihp - My life is Harry Potter."""
    try:
        req = web.get("http://www.mylifeishp.com/random")
    except:
        raise GrumbleError("This service is not available to Muggles.")

    doc = lxml.html.fromstring(req)
    quote = doc.find_class('oldlink')[0].text_content()
    phenny.say(quote)
mlihp.commands = ['mlihp']


if __name__ == '__main__':
    print(__doc__.strip())
