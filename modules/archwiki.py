#!/usr/bin/env python
"""
archwiki.py - Phenny ArchWiki Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/

modified from Wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re, urllib.request, urllib.parse, urllib.error
import web
import json

wikiapi = 'https://wiki.archlinux.org/api.php?action=query&list=search&srsearch=%s&limit=1&prop=snippet&format=json'
wikiuri = 'https://wiki.archlinux.org/index.php/%s'
wikisearch = 'https://wiki.archlinux.org/index.php/Special:Search?' \
                          + 'search=%s&fulltext=Search'

r_tr = re.compile(r'(?ims)<tr[^>]*>.*?</tr>')
r_content = re.compile(r'(?ims)</p>\n</div>.*?<!-- end content -->')
r_paragraph = re.compile(r'(?ims)<p[^>]*>.*?</p>|<li(?!n)[^>]*>.*?</li>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')
r_redirect = re.compile(
    r'(?ims)class=.redirectText.>\s*<a\s*href=./wiki/([^"/]+)'
)

abbrs = ['etc', 'ca', 'cf', 'Co', 'Ltd', 'Inc', 'Mt', 'Mr', 'Mrs', 
            'Dr', 'Ms', 'Rev', 'Fr', 'St', 'Sgt', 'pron', 'approx', 'lit', 
            'syn', 'transl', 'sess', 'fl', 'Op'] \
    + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ') \
    + list('abcdefghijklmnopqrstuvwxyz')
t_sentence = r'^.{5,}?(?<!\b%s)(?:\.(?=[\[ ][A-Z0-9]|\Z)|\Z)'
r_sentence = re.compile(t_sentence % r')(?<!\b'.join(abbrs))

def unescape(s): 
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&amp;', '&')
    s = s.replace('&#160;', ' ')
    return s

def text(html): 
    html = r_tag.sub('', html)
    html = r_whitespace.sub(' ', html)
    return unescape(html).strip()

def archwiki(term, last=False): 
    global wikiapi, wikiuri
    url = wikiapi % term
    bytes = web.get(url)
    result = json.loads(bytes)
    result = result['query']['search']
    if len(result) <= 0:
        return None
    term = result[0]['title']
    term = term.replace(' ', '_')
    snippet = text(result[0]['snippet'])
    return "%s - %s" % (snippet, wikiuri % term)

def awik(phenny, input): 
    origterm = input.groups()[1]
    if not origterm: 
        return phenny.say('Perhaps you meant ".awik dwm"?')
    origterm = origterm

    term = urllib.parse.unquote(origterm)
    term = term[0].upper() + term[1:]
    term = term.replace(' ', '_')

    try: result = archwiki(term)
    except IOError: 
        error = "Can't connect to wiki.archlinux.org (%s)" % (wikiuri % term)
        return phenny.say(error)

    if result is not None: 
        phenny.say(result)
    else: phenny.say('Can\'t find anything in the ArchWiki for "%s".' % origterm)

awik.commands = ['awik']
awik.priority = 'high'

if __name__ == '__main__': 
    print(__doc__.strip())
