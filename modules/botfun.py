#!/usr/bin/python3
"""
botfun.py - activities that bots do
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

otherbot = "truncatedcone"

def botfight(phenny, input):
    """.botfight - Fight the other bot in the channel."""

    messages = ["hits %s", "punches %s", "kicks %s", "hits %s with a rubber hose", "stabs %s with a clean kitchen knife"]
    response = random.choice(messages)

    phenny.do(response % otherbot)
botfight.commands = ['botfight']
botfight.priority = 'low'
botfight.example = '.botfight'

def bothug(phenny, input):
    """.bothug - Hug the other bot in the channel."""

    phenny.do("hugs %s" % otherbot)
bothug.commands = ['bothug']
bothug.priority = 'low'
bothug.example = '.bothug'

if __name__ == '__main__':
    print(__doc__.strip())
