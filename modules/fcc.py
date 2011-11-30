#!/usr/bin/python3
"""
fcc.py - fcc callsign lookup
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.error import HTTPError
import web
import lxml.html

def fcc(phenny, input):
	""".fcc <callsign> - Look up a callsign issued by the FCC."""

	callsign = input.group(2)

	try:
		req = web.post("http://www.arrl.org/advanced-call-sign-search",
		        {'data[Search][terms]': callsign})
	except (HTTPError, IOError):
		phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
		return

	doc = lxml.html.fromstring(req)
	result = doc.xpath('//h3')
	if len(result) != 2:
	    phenny.reply('No results found for {0}'.format(callsign))
	    return

	response = result[0].text_content().strip()
	phenny.say(response)
fcc.rule = (['fcc'], r'(.*)')

if __name__ == '__main__':
	print(__doc__.strip())

