#!/usr/bin/python3
"""
fcc.py - fcc callsign lookup
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.error import HTTPError
import web
import json

def fcc(phenny, input):
	""".fcc <callsign> - Look up a callsign issued by the FCC."""

	callsign = input.group(2)

	try:
		req = web.get("http://callook.info/{0}/json".format(web.quote(callsign)))
	except (HTTPError, IOError):
		phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
		return

	data = json.loads(req)
	if len(data) <= 0 or data['status'] == 'INVALID':
	    phenny.reply('No results found for {0}'.format(callsign))
	    return

	response = "{0} - {1} - {2}".format(data['current']['callsign'],
	        data['name'], data['otherInfo']['ulsUrl'])
	phenny.say(response)
fcc.rule = (['fcc'], r'(.*)')

if __name__ == '__main__':
	print(__doc__.strip())

