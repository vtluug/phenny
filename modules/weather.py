#!/usr/bin/env python
"""
weather.py - Phenny Weather Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re
import metar
import web
from tools import deprecated, GrumbleError

r_from = re.compile(r'(?i)([+-]\d+):00 from')

def location(name):
    name = web.quote(name)
    uri = 'http://ws.geonames.org/searchJSON?q=%s&maxRows=1' % name
    for i in range(10):
        bytes = web.get(uri)
        if bytes is not None: break

    results = web.json(bytes)
    try: name = results['geonames'][0]['name']
    except IndexError: 
        return '?', '?', '0', '0'
    countryName = results['geonames'][0]['countryName']
    lat = results['geonames'][0]['lat']
    lng = results['geonames'][0]['lng']
    return name, countryName, lat, lng

def local(icao, hour, minute):
    uri = ('http://www.flightstats.com/' + 
             'go/Airport/airportDetails.do?airportCode=%s')
    try: bytes = web.get(uri % icao)
    except AttributeError:
        raise GrumbleError('A WEBSITE HAS GONE DOWN WTF STUPID WEB')
    m = r_from.search(bytes)
    if m:
        offset = m.group(1)
        lhour = int(hour) + int(offset)
        lhour = lhour % 24
        return (str(lhour) + ':' + str(minute) + ', ' + str(hour) + 
                  str(minute) + 'Z')
        # return (str(lhour) + ':' + str(minute) + ' (' + str(hour) + 
        #            ':' + str(minute) + 'Z)')
    return str(hour) + ':' + str(minute) + 'Z'

def code(phenny, search):
    from icao import data
    
    if search.upper() in [loc[0] for loc in data]:
        return search.upper()
    else:
        name, country, latitude, longitude = location(search)
        if name == '?': return False
        sumOfSquares = (99999999999999999999999999999, 'ICAO')
        for icao_code, lat, lon in data:
            latDiff = abs(latitude - lat)
            lonDiff = abs(longitude - lon)
            diff = (latDiff * latDiff) + (lonDiff * lonDiff)
            if diff < sumOfSquares[0]:
                sumOfSquares = (diff, icao_code)
        return sumOfSquares[1]

def f_weather(phenny, input):
    """.weather <ICAO> - Show the weather at airport with the code <ICAO>."""
    icao_code = input.group(2)
    if not icao_code:
        return phenny.say("Try .weather London, for example?")

    icao_code = code(phenny, icao_code)

    if not icao_code:
        phenny.say("No ICAO code found, sorry")
        return

    uri = 'http://weather.noaa.gov/pub/data/observations/metar/stations/%s.TXT'
    try:
        bytes = web.get(uri % icao_code)
    except AttributeError:
        raise GrumbleError('OH CRAP NOAA HAS GONE DOWN THE WEB IS BROKEN')
    except web.HTTPError:
        phenny.say("No NOAA data available for that location.")
        return

    if 'Not Found' in bytes:
        phenny.say(icao_code + ": no such ICAO code, or no NOAA data")
        return

    phenny.say(str(metar.parse(bytes)))
f_weather.rule = (['weather'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
