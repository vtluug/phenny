#!/usr/bin/python2
"""
tfw.py - the fucking weather module
author: mutantmonkey <mutantmonkey@gmail.com>
"""

import random

from urllib import quote as urlquote
from urllib2 import urlopen, HTTPError
import lxml.html

def tfw(phenny, input, celsius=False):
	""".tfw <city/zip> - Show the fucking weather at the specified location."""

	zipcode = input.group(2)
	if not zipcode:
		# default to Blacksburg, VA
		zipcode = "24060"

	if celsius:
		celsius_param = "&CELSIUS=yes"
	else:
		celsius_param = ""

	try:
		req = urlopen("http://thefuckingweather.com/?zipcode=%s%s" % (urlquote(zipcode), celsius_param))
	except HTTPError:
		phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
		return

	doc = lxml.html.parse(req)

	location = doc.getroot().find_class('small')[0].text_content()

	try:
		weather = doc.getroot().get_element_by_id('content')
	except KeyError:
		phenny.say("Unknown location")
		return

	main = weather.find_class('large')

	# temperature is everything up to first <br />
	temp =  main[0].text
	
	# parse comment (broken by <br />, so we have do it this way)
	comments = main[0].xpath('text()')
	if len(comments) > 2:
		comment = "%s %s" % (comments[1], comments[2])
	else :
		comment = comments[1]

	# remark is in its own div, so we have it easy
	remark = weather.get_element_by_id('remark').text_content()

	response = "%s %s - %s - %s" % (temp, comment, remark, location)
	phenny.say(response)
tfw.rule = (['tfw'], r'(.*)')

def tfwc(phenny, input):
	""".tfwc <city/zip> - The fucking weather, in fucking celsius."""
	return tfw(phenny, input, True)
tfwc.rule = (['tfwc'], r'(.*)')

if __name__ == '__main__':
	print __doc__.strip()

