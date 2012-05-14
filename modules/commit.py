#!/usr/bin/python3
"""
commit.py - what the commit
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.error import HTTPError
import web

def commit(phenny, input):
    """.commit - Get a What the Commit commit message."""

    try:
        msg = web.get("http://whatthecommit.com/index.txt")
    except (HTTPError, IOError, ValueError):
        phenny.reply("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return
    phenny.reply(msg)
commit.commands = ['commit']

if __name__ == '__main__':
    print(__doc__.strip())
