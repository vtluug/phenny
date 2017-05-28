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
from modules.search import generic_google

subs = [
    ('£', 'GBP '),
    ('€', 'EUR '),
    ('\$', 'USD '),
    (r'\n', '; '),
    ('&deg;', '°'),
    (r'\/', '/'),
]

r_google_calc = re.compile(r'calculator-40.gif.*? = (.*?)<')
r_google_calc_exp = re.compile(r'calculator-40.gif.*? = (.*?)<sup>(.*?)<')

def c(phenny, input):
    """Google calculator."""
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    q = input.group(2)
    bytes = generic_google(q)
    m = r_google_calc_exp.search(bytes)
    if not m:
        m = r_google_calc.search(bytes)
   
    if not m:
        num = None
    elif m.lastindex == 1:
        num = web.decode(m.group(1))
    else:
        num = "^".join((web.decode(m.group(1)), web.decode(m.group(2))))

    if num:
        phenny.say(num)
    else:
        phenny.reply("Sorry, no result.")


# def c(phenny, input):
#     """DuckDuckGo calculator."""
#     if not input.group(2):
#         return phenny.reply("Nothing to calculate.")
#     q = input.group(2)
#
#     try:
#         r = web.get(
#             'https://api.duckduckgo.com/?q={}&format=json&no_html=1'
#             '&t=mutantmonkey/phenny'.format(web.quote(q)))
#     except web.HTTPError:
#         raise GrumbleError("Couldn't parse the result from DuckDuckGo.")
#
#     data = web.json(r)
#     if data['AnswerType'] == 'calc':
#         answer = data['Answer'].split('=')[-1].strip()
#     else:
#         answer = None
# 
#     if answer:
#         phenny.say(answer)
#     else:
#         phenny.reply('Sorry, no result.')
c.commands = ['c']
c.example = '.c 5 + 3'


if __name__ == '__main__':
    print(__doc__.strip())
