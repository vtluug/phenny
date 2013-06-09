#!/usr/bin/python3
"""
short.py - vtluug url shortner
author: andreim <andreim@andreim.net>
"""

from tools import GrumbleError
import web
import json


def short(phenny, input):
    """.short <url> - Shorten a URL."""

    url = input.group(2)
    if not url:
        phenny.reply("No URL provided. CAN I HAS?")
        return

    try:
        r = web.post("http://vtlu.ug/vtluug", {'lurl': url})
    except:
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    phenny.reply(r)
short.rule = (['short'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
