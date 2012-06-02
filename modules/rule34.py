#!/usr/bin/python3
"""
rule34.py - rule 34 module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.parse import quote as urlquote
from urllib.error import HTTPError
from tools import GrumbleError
import web
import lxml.html

def rule34(phenny, input):
    """.rule34 <query> - Rule 34: If it exists there is porn of it."""

    q = input.group(2)
    if not q:
        phenny.say(rule34.__doc__.strip())
        return

    try:
        req = web.get("http://rule34.xxx/index.php?page=post&s=list&tags={0}".format(urlquote(q)))
    except (HTTPError, IOError):
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    doc = lxml.html.fromstring(req)
    doc.make_links_absolute('http://rule34.xxx/')
    thumbs = doc.find_class('thumb')
    if len(thumbs) <= 0:
        phenny.reply("You just broke Rule 34! Better start uploading...")
        return

    try:
        link = thumbs[0].find('a').attrib['href']
    except AttributeError:
        raise GrumbleError("THE INTERNET IS FUCKING BROKEN. Please try again later.")

    response = '!!NSFW!! -> {0} <- !!NSFW!!'.format(link)
    phenny.reply(response)
rule34.rule = (['rule34'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
