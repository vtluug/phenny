#!/usr/bin/env python
"""
wiktionary.py - Phenny Wiktionary Module
Copyright 2009, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web
import json

uri = 'http://en.wiktionary.org/w/index.php?title=%s&printable=yes'
wikiapi = 'http://en.wiktionary.org/w/api.php?action=query&titles={0}&prop=revisions&rvprop=content&format=json'
#r_tag = re.compile(r'<[^>]+>')
r_ul = re.compile(r'(?ims)<ul>.*?</ul>')
r_li = re.compile(r'^# ')
r_img = re.compile(r'\[\[Image:.*\]\]')
r_link1 = re.compile(r'\[\[([A-Za-z0-9\-_ ]+?)\]\]')
r_link2 = re.compile(r'\[\[([A-Za-z0-9\-_ ]+?)\|(.+?)\]\]')
r_context = re.compile(r'{{context\|(.+?)}}')
r_template1 = re.compile(r'{{.+?\|(.+?)}}')
r_template2 = re.compile(r'{{(.+?)}}')

def text(html): 
    text = r_li.sub('', html).strip()
    text = r_img.sub('', text)
    text = r_link1.sub(r'\1', text)
    text = r_link2.sub(r'\2', text)
    text = r_context.sub(r'\1:', text)
    text = r_template1.sub(r'\1:', text)
    text = r_template2.sub(r'\1:', text)
    return text

def wiktionary(word): 
    bytes = web.get(wikiapi.format(web.quote(word)))
    pages = json.loads(bytes)
    pages = pages['query']['pages']
    pg = next(iter(pages))

    try:
        result = pages[pg]['revisions'][0]['*']
    except KeyError:
        return '', ''

    mode = None
    etymology = None
    definitions = {}
    for line in result.splitlines(): 
        if line == '===Etymology===':
            mode = 'etymology'
        elif 'Noun' in line: 
            mode = 'noun'
        elif 'Verb' in line: 
            mode = 'verb'
        elif 'Adjective' in line: 
            mode = 'adjective'
        elif 'Adverb' in line: 
            mode = 'adverb'
        elif 'Interjection' in line: 
            mode = 'interjection'
        elif 'Particle' in line: 
            mode = 'particle'
        elif 'Preposition' in line: 
            mode = 'preposition'
        elif len(line) == 0:
            mode = None

        elif mode == 'etymology':
            etymology = text(line)
        elif mode is not None and '#' in line:
            definitions.setdefault(mode, []).append(text(line))

        if '====Synonyms====' in line: 
            break
    return etymology, definitions

parts = ('preposition', 'particle', 'noun', 'verb', 
    'adjective', 'adverb', 'interjection')

def format(word, definitions, number=2): 
    result = '%s' % word
    for part in parts: 
        if part in definitions: 
            defs = definitions[part][:number]
            result += ' \u2014 ' + ('%s: ' % part)
            n = ['%s. %s' % (i + 1, e.strip(' .')) for i, e in enumerate(defs)]
            result += ', '.join(n)
    return result.strip(' .,')

def w(phenny, input): 
    if not input.group(2):
        return phenny.reply("Nothing to define.")
    word = input.group(2)
    etymology, definitions = wiktionary(word)
    if not definitions: 
        phenny.say("Couldn't get any definitions for %s." % word)
        return

    result = format(word, definitions)
    if len(result) < 150: 
        result = format(word, definitions, 3)
    if len(result) < 150: 
        result = format(word, definitions, 5)

    if len(result) > 300: 
        result = result[:295] + '[...]'
    phenny.say(result)
w.commands = ['w']
w.example = '.w bailiwick'

if __name__ == '__main__': 
    print(__doc__.strip())
