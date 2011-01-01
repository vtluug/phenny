#!/usr/bin/python2
"""
ddg.py - duck duck go module
author: mutantmonkey <mutantmonkey@gmail.com>
portions based on search.py by sean b palmer
"""

import random

from urllib import quote as urlquote
from urllib2 import urlopen, HTTPError
import lxml.html

import web

def search(query):
	uri = 'https://api.duckduckgo.com/'
	args = '?q=%s&o=json' % web.urllib.quote(query.encode('utf-8'))
	bytes = web.get(uri + args)
	return web.json(bytes)

def result(query):
	results = search(query)
	try:
		return results['Results'][0]['FirstURL']
	except IndexError:
		return None

def ddg(phenny, input, celsius=False):
	""".tfw <query> - Search Duck Duck Go for the specified query."""

	query = input.group(2)
	if not query:
		return phenny.reply(".ddg what?")

	uri = result(query)
	if uri:
		phenny.reply("%s - Results from https://duckduckgo.com/" % uri)
	else:
		phenny.reply("No results found for '%s'." % query)
ddg.rule = (['ddg'], r'(.*)')

if __name__ == '__main__':
	print __doc__.strip()

