#!/usr/bin/env python
# coding=utf-8
"""
translate.py - Phenny Translation Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, urllib.request, urllib.parse, urllib.error
import json
import web

def translate(text, input='auto', output='en'): 
    opener = urllib.request.build_opener()
    opener.addheaders = [(
        'User-Agent', 'Mozilla/5.0' + 
        '(X11; U; Linux i686)' + 
        'Gecko/20071127 Firefox/2.0.0.11'
    )]

    input, output = urllib.parse.quote(input), urllib.parse.quote(output)
    text = urllib.parse.quote(text)

    result = opener.open('http://translate.google.com/translate_a/t?' +
        ('client=t&hl=en&sl=%s&tl=%s&multires=1' % (input, output)) + 
        ('&otf=1&ssel=0&tsel=0&uptl=en&sc=1&text=%s' % text)).read()
    result = result.decode('utf-8')

    while ',,' in result: 
        result = result.replace(',,', ',null,')
    data = json.loads(result)

    try: language = data[-2][0][0]
    except: language = '?'

    return ''.join(x[0] for x in data[0]), language

def tr(phenny, context): 
    """Translates a phrase, with an optional language hint."""
    input, output, phrase = context.groups()

    phrase = phrase

    if (len(phrase) > 350) and (not context.admin): 
        return phenny.reply('Phrase must be under 350 characters.')

    input = input or 'auto'
    input = input.encode('utf-8')
    output = (output or 'en').encode('utf-8')

    if input != output: 
        msg, input = translate(phrase, input, output)
        output = output.decode('utf-8')
        if msg: 
            msg = web.decode(msg) # msg.replace('&#39;', "'")
            msg = '"%s" (%s to %s, translate.google.com)' % (msg, input, output)
        else: msg = 'The %s to %s translation failed, sorry!' % (input, output)

        phenny.reply(msg)
    else: phenny.reply('Language guessing failed, so try suggesting one!')

tr.rule = ('$nick', r'(?:([a-z]{2}) +)?(?:([a-z]{2}) +)?["“](.+?)["”]\? *$')
tr.example = '$nickname: "mon chien"? or $nickname: fr "mon chien"?'
tr.priority = 'low'

def mangle(phenny, input): 
    phrase = input.group(2)
    for lang in ['fr', 'de', 'es', 'it', 'ja']: 
        backup = phrase
        phrase = translate(phrase, 'en', lang)
        if not phrase: 
            phrase = backup
            break
        __import__('time').sleep(0.5)

        backup = phrase
        phrase = translate(phrase, lang, 'en')
        if not phrase: 
            phrase = backup
            break
        __import__('time').sleep(0.5)

    phenny.reply(phrase or 'ERRORS SRY')
mangle.commands = ['mangle']

if __name__ == '__main__': 
    print(__doc__.strip())
