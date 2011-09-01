#!/usr/bin/python2
"""
mlib.py - my life is bro retrieval
author: Ramblurr <unnamedrambler@gmail.com>
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import random

from urllib import quote as urlquote
from urllib2 import urlopen, HTTPError
import lxml.html

def mlib(phenny, input):
   """.mlib"""
   try:
      req = urlopen("http://mylifeisbro.com/random")
   except HTTPError:
      phenny.say("MLIB is out getting a case of Natty. It's chill.")
      return

   doc = lxml.html.parse(req)

   quote = doc.getroot().find_class('storycontent')[0][0].text_content()

   phenny.say(quote)
mlib.commands = ['mlib']

if __name__ == '__main__':
   print __doc__.strip()

