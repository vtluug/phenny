#!/usr/bin/python3
"""
short.py - vtluug url shortner
author: andreim <andreim@andreim.net>
"""

from urllib.error import HTTPError
import web
import json

def short(phenny, input):
    """.short <url> - Shorten a URL."""

    url = input.group(2)
    if not url:
        phenny.reply("No URL provided. CAN I HAS?")
        return

    try:
        req = web.post("http://vtlu.ug/vtluug", {'lurl': url})
    except (HTTPError, IOError):
        phenny.reply("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return

    phenny.reply(req)
short.rule = (['short'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
