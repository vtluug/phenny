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
import lxml.cssselect

def tfw(phenny, input, fahrenheit=False, celsius=False):
    """.tfw <city/zip> - Show the fucking weather at the specified location."""

    where = input.group(2)
    if not where:
        # default to Blacksburg, VA
        where = "24060"

    if fahrenheit:
        celsius_param = ""
    else:
        celsius_param = "&CELSIUS=yes"

    try:
        req = web.get("http://thefuckingweather.com/?where={0}{1}".format(urlquote(where), celsius_param))
    except (HTTPError, IOError):
        phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return

    doc = lxml.html.fromstring(req)

    try:
        #location = doc.find_class('small')[0].text_content()
        location = doc.get_element_by_id('locationDisplaySpan').text_content()
    except (IndexError, KeyError):
        phenny.say("UNKNOWN FUCKING LOCATION. Try another?")
        return

    temp_sel = lxml.cssselect.CSSSelector('span.temperature')
    temp = temp_sel(doc)[0].text_content()
    temp = int(temp)
            
    # add units and convert if necessary
    if fahrenheit:
        temp = "{0:d}°F‽".format(temp)
    elif celsius:
        temp = "{0:d}°C‽".format(temp)
    else:
        tempev = (temp + 273.15) * 8.617343e-5 * 1000
        temp = "%f meV‽" % tempev
    
    remark_sel = lxml.cssselect.CSSSelector('p.remark')
    remark = remark_sel(doc)[0].text_content()

    flavor_sel = lxml.cssselect.CSSSelector('p.flavor')
    flavor = flavor_sel(doc)[0].text_content()

    response = "%s %s - %s - %s" % (temp, remark, flavor, location)
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
