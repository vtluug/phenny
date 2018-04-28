#!/usr/bin/env python
"""
archwiki.py - Phenny ArchWiki Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/

modified from Wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import wiki

endpoints = {
    'api': 'https://wiki.archlinux.org/api.php?action=query&list=search&srsearch={0}&limit=1&format=json',
    'url': 'https://wiki.archlinux.org/index.php/{0}',
    'search': 'https://wiki.archlinux.org/index.php/Special:Search?search={0}&fulltext=Search',
}

def awik(phenny, input): 
    """.awik <term> - Look up something on the ArchWiki."""

    origterm = input.group(1)
    if not origterm:
        return phenny.say('Perhaps you meant ".awik dwm"?')

    term, section = wiki.parse_term(origterm)

    w = wiki.Wiki(endpoints)
    match = w.search(term)

    if not match:
        phenny.say('Can\'t find anything in the ArchWiki for "{0}".'.format(term))
        return

    snippet, url = wiki.extract_snippet(match, section)

    phenny.say('"{0}" - {1}'.format(snippet, url))

awik.commands = ['awik']
awik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
