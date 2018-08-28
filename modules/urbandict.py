#!/usr/bin/python3
"""
urbandict.py - urban dictionary module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from tools import GrumbleError
import web
import json


def urbandict(phenny, input):
    """.urb <word> - Search Urban Dictionary for a definition."""

    word = input.group(2)
    if not word:
        phenny.say(urbandict.__doc__.strip())
        return

    try:
        data = web.get(
            "http://api.urbandictionary.com/v0/define?term={0}".format(
                web.quote(word)))
        data = json.loads(data)
    except:
        raise GrumbleError(
            "Urban Dictionary slemped out on me. Try again in a minute.")

    results = data['list']

    if not results:
        phenny.say("No results found for {0}".format(word))
        return

    result = results[0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(
        web.quote(word))

    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    phenny.say(response)
urbandict.name = 'urb'
urbandict.rule = (['urb'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
