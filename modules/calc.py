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
r_google_calc_exp = re.compile(r'calculator-40.gif.*? = (.*?)<sup>(.*?)</sup></h2>')

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
        num = num.replace('×', '*')
        phenny.say(num)
    else:
        phenny.reply("Sorry, no result.")
c.commands = ['c']
c.example = '.c 5 + 3'


if __name__ == '__main__':
    print(__doc__.strip())
