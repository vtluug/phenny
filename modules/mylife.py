#!/usr/bin/python2
"""
mylife.py - various commentary on life
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

def mlia(phenny, input):
   """.mlia"""
   try:
       req = urlopen("http://mylifeisaverage.com/")
   except HTTPError:
      phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
      return

   doc = lxml.html.parse(req)
   quote = doc.getroot().find_class('story')[0][0].text_content()
   quote = quote.strip()
   phenny.say(quote)
mlia.commands = ['mlia']

def mlih(phenny, input):
   """.mlih"""
   try:
      req = urlopen("http://mylifeisho.com/random")
   except HTTPError:
      phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
      return

   doc = lxml.html.parse(req)
   quote = doc.getroot().find_class('storycontent')[0][0].text_content()
   phenny.say(quote)
mlih.commands = ['mlih']

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
mlih.commands = ['mlih']

if __name__ == '__main__':
   print __doc__.strip()

