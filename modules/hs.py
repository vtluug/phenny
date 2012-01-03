#!/usr/bin/python3
"""
hs.py - hokie stalker module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import web
import lxml.etree

SEARCH_URL = "https://webapps.middleware.vt.edu/peoplesearch/PeopleSearch?query={0}&dsml-version=2"
RESULTS_URL = "http://search.vt.edu/search/people.html?q={0}"
PERSON_URL = "http://search.vt.edu/search/person.html?person={0:d}"
NS = NS = '{urn:oasis:names:tc:DSML:2:0:core}'

"""Search the people search database using the argument as a query."""
def search(query):
    query = web.quote(query)
    try:
        req = web.get(SEARCH_URL.format(query))
    except (HTTPError, IOError):
        phenny.say("THE INTERNET IS FUCKING BROKEN. Please try again later.")
        return

    xml = lxml.etree.fromstring(req.encode('utf-8'))
    results = xml.findall('{0}searchResponse/{0}searchResultEntry'.format(NS))
    if len(results) <= 0:
        return False

    ret = []
    for entry in results:
        entry_data = {}
        for attr in entry:
            entry_data[attr.attrib['name']] = attr[0].text
        ret.append(entry_data)

    return ret

def hs(phenny, input):
    """.hs <pid/name/email> - Search for someone on Virginia Tech People Search."""

    q = input.group(2)
    if q is None:
        return
    q = q.strip()
    results = RESULTS_URL.format(web.quote(q))

    s = search(q)
    if s:
        if len(s) >1:
            phenny.reply("Multiple results found; try {0}".format(results))
        else:
            for entry in s:
                person = PERSON_URL.format(int(entry['uid']))
                phenny.reply("{0} - {1}".format(entry['cn'], person))
    else:
        phenny.reply("No results found")
hs.rule = (['hs'], r'(.*)')

if __name__ == '__main__':
    print(__doc__.strip())
