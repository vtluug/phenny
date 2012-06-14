#!/usr/bin/env python
"""
vtluugwiki.py - Phenny VTLUUG Wiki Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/

modified from Wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re, urllib.request, urllib.parse, urllib.error
import wiki

wikiapi = 'https://vtluug.org/w/api.php?action=query&list=search&srsearch={0}&limit=1&prop=snippet&format=json'
wikiuri = 'https://vtluug.org/wiki/{0}'
wikisearch = 'https://vtluug.org/wiki/Special:Search?' \
                          + 'search={0}&fulltext=Search'

def vtluug(phenny, input): 
    origterm = input.groups()[1]
    if not origterm: 
        return phenny.say('Perhaps you meant ".vtluug VT-Wireless"?')

    term = urllib.parse.unquote(origterm)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')

    w = wiki.Wiki(wikiapi, wikiuri, wikisearch)

    try:
        result = w.search(term)
    except IOError: 
        error = "Can't connect to vtluug.org ({0})".format(wikiuri.format(term))
        return phenny.say(error)

    if result is not None: 
        phenny.say(result)
    else:
        phenny.say('Can\'t find anything in the VTLUUG Wiki for "{0}".'.format(origterm))

vtluug.commands = ['vtluug']
vtluug.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
