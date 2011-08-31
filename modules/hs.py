#!/usr/bin/python2
"""
hs.py - hokie stalker module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import ldap
from urllib import quote as urlquote

LDAP_URI = "ldap://directory.vt.edu"
RESULTS_URL = "http://search.vt.edu/search/people.html?q={0}"
PERSON_URL = "http://search.vt.edu/search/person.html?person={0:d}"

l = ldap.initialize(LDAP_URI)

"""Search LDAP using the argument as a query. Argument must be a valid LDAP query."""
def search(query):
    result = l.search_s('ou=People,dc=vt,dc=edu', ldap.SCOPE_SUBTREE, query)
    if len(result) <= 0:
        return False

    return result

def hs(phenny, input):
    """.hs <pid/name/email> - Search for someone on Virginia Tech People Search."""

    q = input.group(2)
    if q is None:
        return
    q = q.strip()
    results = RESULTS_URL.format(urlquote(q))

    try:
        s = search('(|(uupid={0})(mail={0})(cn={1}))'.format(q[0], ' '.join(q)))
        if not s:
            s = search('(|(uupid=*{0}*)(mail=*{0}*)(cn=*{1}*))'.format(q[0], '*'.join(q)))
    except ldap.FILTER_ERROR:
        phenny.reply('Filter error; try to avoid injection attacks in the future please.')
        return
    except ldap.SIZELIMIT_EXCEEDED:
        phenny.reply('Too many results to display here; check out {0}'.format(results))
        return
    except ldap.TIMELIMIT_EXCEEDED:
        phenny.reply('Time limit exceeded; check out {0}'.format(results))
        return

    if s:
        if len(s) >1:
            phenny.reply("Multiple results found; try {0}".format(results))
        else:
            for dh, entry in s:
                person = PERSON_URL.format(int(entry['uid'][0]))
                phenny.reply("{0} - {1}".format(entry['cn'][0], person))
    else:
        phenny.reply("No results found")
hs.rule = (['hs'], r'(.*)')

if __name__ == '__main__':
    print __doc__.strip()

