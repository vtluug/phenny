#!/usr/bin/python2
"""
fml.py - fuck my life retrieval
author: Ramblurr <unnamedrambler@gmail.com>
"""

import random

from urllib import quote as urlquote
from urllib2 import urlopen, HTTPError
import lxml.html

def fml(phenny, input):
   """.fml"""
   try:
      req = urlopen("http://www.fmylife.com/random")
   except HTTPError:
      phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
      return

   doc = lxml.html.parse(req)

   quote = doc.getroot().find_class('article')[0][0].text_content()

   phenny.say(quote)
fml.commands = ['fml']

if __name__ == '__main__':
   print __doc__.strip()

