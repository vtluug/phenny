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
from modules.search import newton_api

operations = {'simplify', 'factor', 'derive', 'integrate', 'zeroes', 'tangent',
        'area', 'cos', 'sin', 'tan', 'arccos', 'arcsin', 'arctan', 'abs', 'log'}

def c(phenny, input):
    """Newton calculator."""
    if not input.group(2):
        return phenny.reply("Nothing to calculate.")
    q = input.group(2)
    q = q.split(' ', 1)

    if len(q) > 1 and q[0] in operations:
        operation = q[0]
        expression = q[1]
    elif len(q) > 0:
        operation = 'simplify'
        expression = q[0]

    result = newton_api(operation, expression)

    if result:
        phenny.say(result)
    else:
        phenny.reply("Sorry, no result.")
c.commands = ['c']
c.example = '.c 5 + 3'
c.example = '.c integrate 1/3 x^3 + x^2 + C'


if __name__ == '__main__':
    print(__doc__.strip())
