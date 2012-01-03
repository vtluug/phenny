#!/usr/bin/python3
"""
linx.py - linx.li uploader
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.error import HTTPError
import web
import json

def linx(phenny, input):
    """.linx <url> - Upload a URL to linx.li."""

    url = input.group(2)
    if not url:
        phenny.reply("No URL provided. CAN I HAS?")
        return

    try:
        req = web.post("http://linx.li/vtluug", {'url': url})
    except (HTTPError, IOError):
        phenny.reply("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return

    data = json.loads(req)
    if len(data) <= 0 or not data['success']:
        phenny.reply('Sorry, upload failed.')
        return

    phenny.reply(data['url'])
linx.rule = (['linx'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
