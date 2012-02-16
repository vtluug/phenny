#!/usr/bin/python3
"""
nsfw.py - some things just aren't safe for work, a phenny module
author: Casey Link <unnamedrambler@gmail.com
"""

def nsfw(phenny, input):
    link = input.group(2)
    if not link:
        phenny.say(".nsfw <link> - for when a link isn't safe for work")
        return
    phenny.say("!!NSFW!! -> %s <- !!NSFW!!" % (link))
nsfw.rule = (['nsfw'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
