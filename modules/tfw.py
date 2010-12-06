#!/usr/bin/python2
"""
tfw.py - the fucking weather module
author: mutantmonkey <mutantmonkey@gmail.com>
"""

import random

from urllib import quote as urlquote
from urllib2 import urlopen, HTTPError
import lxml.html

def tfw(phenny, input):
	zipcode = input.group(2)

	try:
		req = urlopen("http://thefuckingweather.com/?zipcode=%s" % urlquote(zipcode))
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

if __name__ == '__main__':
	print __doc__.strip()

