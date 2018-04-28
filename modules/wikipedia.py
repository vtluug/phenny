#!/usr/bin/env python
"""
wikipedia.py - Phenny Wikipedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import wiki

endpoints = {
    'api': 'https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch={0}&prop=snippet&limit=1',
    'url': 'https://en.wikipedia.org/wiki/{0}',
    'search': 'https://en.wikipedia.org/wiki/Special:Search?search={0}&fulltext=Search',
}

def wik(phenny, input): 
    """.wik <term> - Look up something on Wikipedia."""

    origterm = input.groups()[1]
    if not origterm: 
        return phenny.say('Perhaps you meant ".wik Zen"?')

    origterm = origterm.strip()
    term, section = wiki.parse_term(origterm)

    w = wiki.Wiki(endpoints)
    match = w.search(term)

    if not match:
        phenny.say('Can\'t find anything in Wikipedia for "{0}".'.format(origterm))
        return

    snippet, url = wiki.extract_snippet(match, section)

    phenny.say('"{0}" - {1}'.format(snippet, url))

wik.commands = ['wik']
wik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
