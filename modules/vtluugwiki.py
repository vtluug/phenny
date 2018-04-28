#!/usr/bin/env python
"""
vtluugwiki.py - Phenny VTLUUG Wiki Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/

modified from Wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import wiki

endpoints = {
    'api': 'https://vtluug.org/w/api.php?action=query&list=search&srsearch={0}&limit=1&prop=snippet&format=json',
    'url': 'https://vtluug.org/wiki/{0}',
    'search': 'https://vtluug.org/wiki/Special:Search?search={0}&fulltext=Search',
}

def vtluug(phenny, input): 
    """.vtluug <term> - Look up something on the VTLUUG wiki."""

    origterm = input.groups()[1]
    if not origterm: 
        return phenny.say('Perhaps you meant ".vtluug VT-Wireless"?')

    term, section = wiki.parse_term(origterm)

    w = wiki.Wiki(endpoints)
    match = w.search(term)

    if not match:
        phenny.say('Can\'t find anything in the VTLUUG Wiki for "{0}".'.format(term))
        return

    snippet, url = wiki.extract_snippet(match, section)

    phenny.say('"{0}" - {1}'.format(snippet, url))

vtluug.commands = ['vtluug']
vtluug.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
