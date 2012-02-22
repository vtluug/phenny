#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
tfw.py - the fucking weather module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

from urllib.parse import quote as urlquote
from urllib.error import HTTPError
import web
import lxml.html

def tfw(phenny, input, fahrenheit=False, celsius=False):
    """.tfw <city/zip> - Show the fucking weather at the specified location."""

    zipcode = input.group(2)
    if not zipcode:
        # default to Blacksburg, VA
        zipcode = "24060"

    if fahrenheit:
        celsius_param = ""
    else:
        celsius_param = "&CELSIUS=yes"

    try:
        req = web.get("http://thefuckingweather.com/?zipcode=%s%s" % (urlquote(zipcode), celsius_param))
    except (HTTPError, IOError):
        phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return

    doc = lxml.html.fromstring(req)

    try:
        location = doc.find_class('small')[0].text_content()
        weather = doc.get_element_by_id('content')
    except (IndexError, KeyError):
        phenny.say("UNKNOWN FUCKING LOCATION. Try another?")
        return

    main = weather.find_class('large')

    # temperature is everything up to first <br />
    tempt = ""
    for c in main[0].text:
        if c.isdigit() or c == '-':
            tempt += c
    temp = int(tempt)
            
    # add units and convert if necessary
    if fahrenheit:
        temp = "{0:d}°F‽".format(temp)
    elif celsius:
        temp = "{0:d}°C‽".format(temp)
    else:
        tempev = (temp + 273.15) * 8.617343e-5 * 1000
        temp = "%f meV‽" % tempev
    
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

def tfwf(phenny, input):
    """.tfwf <city/zip> - The fucking weather, in fucking degrees Fahrenheit."""
    return tfw(phenny, input, fahrenheit=True)
tfwf.rule = (['tfwf'], r'(.*)')

def tfwc(phenny, input):
    """.tfwc <city/zip> - The fucking weather, in fucking degrees celsius."""
    return tfw(phenny, input, celsius=True)
tfwc.rule = (['tfwc'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
