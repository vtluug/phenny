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
    quote = doc.find_class('block')[0].text_content()
    quote = quote.strip()
    phenny.say(quote)
fml.commands = ['fml']


if __name__ == '__main__':
    print(__doc__.strip())
