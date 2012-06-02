#!/usr/bin/python3
"""
urbandict.py - urban dictionary module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import urllib.request
from urllib.error import HTTPError
from tools import GrumbleError
import web
import json

def urbandict(phenny, input):
    """.urb <word> - Search Urban Dictionary for a definition."""

    word = input.group(2)
    if not word:
        phenny.say(urbandict.__doc__.strip())
        return

    # create opener
    opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', web.Grab().version),
        ('Referer', "http://m.urbandictionary.com"),
    ]

    try:
        req = opener.open("http://api.urbandictionary.com/v0/define?term={0}"
                .format(web.quote(word)))
        data = req.read().decode('utf-8')
        data = json.loads(data)
    except (HTTPError, IOError, ValueError):
        raise GrumbleError(
                "Urban Dictionary slemped out on me. Try again in a minute.")

    if data['result_type'] == 'no_results':
        phenny.say("No results found for {0}".format(word))
        return

    result = data['list'][0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(web.quote(word))

    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    phenny.say(response)
urbandict.rule = (['urb'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
