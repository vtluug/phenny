#!/usr/bin/env python
"""
wikipedia.py - Phenny Wikipedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web
import wiki

wikiapi = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={0}&limit=1&prop=snippet&format=json'
wikiuri = 'https://en.wikipedia.org/wiki/{0}'
wikisearch = 'https://en.wikipedia.org/wiki/Special:Search?' \
                          + 'search={0}&fulltext=Search'

def wik(phenny, input): 
    """.wik <term> - Look up something on Wikipedia."""

    origterm = input.groups()[1]
    if not origterm: 
        return phenny.say('Perhaps you meant ".wik Zen"?')

    term = web.unquote(origterm)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')

    w = wiki.Wiki(wikiapi, wikiuri, wikisearch)

    try:
        result = w.search(term)
    except web.ConnectionError:
        error = "Can't connect to en.wikipedia.org ({0})".format(wikiuri.format(term))
        return phenny.say(error)

    if result is not None: 
        phenny.say(result)
    else:
        phenny.say('Can\'t find anything in Wikipedia for "{0}".'.format(origterm))

wik.commands = ['wik']
wik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
