#!/usr/bin/env python
# coding=utf-8
"""
calc.py - Phenny Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import web

subs = [
    ('£', 'GBP '),
    ('€', 'EUR '),
    ('\$', 'USD '),
    (r'\n', '; '),
    ('&deg;', '°'),
    (r'\/', '/'),
]


def c(phenny, input):
    """DuckDuckGo calculator."""
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    q = input.group(2)

    try:
        r = web.get(
            'https://api.duckduckgo.com/?q={}&format=json&no_html=1'
            '&t=mutantmonkey/phenny'.format(web.quote(q)))
    except web.HTTPError:
        raise GrumbleError("Couldn't parse the result from DuckDuckGo.")

    data = web.json(r)
    if data['AnswerType'] == 'calc':
        answer = data['Answer'].split('=')[-1].strip()
    else:
        answer = None

    if answer:
        phenny.say(answer)
    else:
        phenny.reply('Sorry, no result.')
c.commands = ['c']
c.example = '.c 5 + 3'


if __name__ == '__main__':
    print(__doc__.strip())
