#!/usr/bin/python2
"""
tfw.py - the fucking weather module
author: mutantmonkey <mutantmonkey@gmail.com>
"""

import random

from urllib2 import urlopen
import lxml.html

def tfw(phenny, input):
	zipcode = input.group(2)
	zipcode = int(zipcode)

	req = urlopen("http://thefuckingweather.com/?zipcode=%d" % zipcode)
	doc = lxml.html.parse(req)

	location = doc.getroot().find_class('small')[0].text_content()

	weather = doc.getroot().get_element_by_id('content')
	main = weather.find_class('large')

	# temperature is everything up to first <br />
	temp =  main[0].text
	
	# parse comment (broken by <br />, so we have do it this way)
	comments = main[0].xpath('text()')
	comment = "%s %s" % (comments[1], comments[2])

	# remark is in its own div, so we have it easy
	remark = weather.get_element_by_id('remark').text_content()

	response = "%s %s - %s - %s" % (temp, comment, remark, location)
	phenny.say(response)
tfw.rule = (['tfw'], r'(.*)')

if __name__ == '__main__':
	print __doc__.strip()

