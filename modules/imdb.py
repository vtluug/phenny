#!/usr/bin/env python
"""
imdb.py - Phenny Web Search Module
Copyright 2012, Randy Nance, randynance.info 
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import json
import web


def imdb_search(query): 
   query = query.replace('!', '')
   query = query.encode('utf-8')
   query = web.quote(query)
   uri = 'http://www.imdbapi.com/?i=&t=%s' % query
   bytes = web.get(uri)
   m = json.loads(bytes)
   return m

def imdb(phenny, input): 
   query = input.group(2)
   if not query: return phenny.reply('.imdb what?')

   m = imdb_search(query)
   try:
       phenny.reply('{0} ({1}): {2}  http://imdb.com/title/{3}'.format(m['Title'], m['Year'], m['Plot'], m['imdbID']))
   except:
        phenny.reply("No results found for '%s'." % query)
imdb.commands = ['imdb']
