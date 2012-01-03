#!/usr/bin/python3
"""
stache.py - mustachify.me module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import web

def stache(phenny, input):
    """.stache <url> - Mustachify an image."""
    url = input.group(2)
    phenny.reply('http://mustachify.me/?src=' + web.quote(url))
stache.rule = (['stache'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
