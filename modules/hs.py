#!/usr/bin/python2
"""
hs.py - hokie stalker module
author: mutantmonkey <mutantmonkey@gmail.com>
"""

import ldap
from urllib import quote as urlquote

LDAP_URI = "ldap://directory.vt.edu"

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

	# initially try search by PID
	s = search('uupid=%s' % q)

	# try partial search on CN if no results for PID
	if not s:
		s = search('cn=*%s*' % '*'.join(q.split(' ')))

	# try email address if no results found for PID or CN
	if not s:
		s = search('mail=%s*' % q)

	if s:
		if len(s) >1:
			phenny.reply("Multiple results found; try http://search.vt.edu/search/people.html?q=%s" % urlquote(q))
		else:
			for dh, entry in s:
				phenny.reply("%s - http://search.vt.edu/search/person.html?person=%d" % (entry['cn'][0], int(entry['uid'][0])))
	else:
		phenny.reply("No results found")
hs.rule = (['hs'], r'(.*)')

if __name__ == '__main__':
	print __doc__.strip()

