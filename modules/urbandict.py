#!/usr/bin/python3
"""
urbandict.py - urban dictionary module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.parse import quote as urlquote
from urllib.error import HTTPError
import web
import json

def urbandict(phenny, input):
    """.urb <word> - Search Urban Dictionary for a definition."""

    word = input.group(2)
    if not word:
        phenny.say(".urb <word> - Search Urban Dictionary for a definition.")
        return

    try:
        req = web.get("http://www.urbandictionary.com/iphone/search/define?term={0}".format(urlquote(word)))
        data = json.loads(req)
    except (HTTPError, IOError, ValueError):
        phenny.say("Urban Dictionary slemped out on me. Try again in a minute.")
        return

    if data['result_type'] == 'no_results':
        phenny.say("No results found for {0}".format(word))
        return

    result = data['list'][0]
    url = 'http://www.urbandictionary.com/define.php?term={0}'.format(urlquote(word))

    response = "{0} - {1}".format(result['definition'].strip()[:256], url)
    phenny.say(response)
urbandict.rule = (['urb'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
