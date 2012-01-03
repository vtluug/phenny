#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
stache.py - mustachify.me module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import web

def stache(phenny, input):
    """.stache <url> - Mustachify an image."""
    url = input.group(2)
    if not url:
        phenny.reply("Please provide an image to Mustachify™.")
        return

    phenny.reply('http://mustachify.me/?src=' + web.quote(url))
stache.rule = (['stache'],
        '(https?:\/\/[^ #]+\.(?:png|jpg|jpeg))(?:[#]\.png)?')

if __name__ == '__main__':
    print(__doc__.strip())
