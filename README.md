phenny
======

This is an experimental port of phenny, a Python IRC bot, to Python3. It is
currently fairly stable, but it has not been as well-tested as the original.

Support for IPv6 and SSL has been added. It appears that SSL support requires
Python 3.2.

Compatibility with existing phenny modules has been mostly retained, but they
will need to be updated to run on Python3 if they do not already.

Installation
------------
1. Run `./phenny` - this creates a default config file
2. Edit `~/.phenny/default.py`
3. Run `./phenny` - this now runs phenny with your settings

Enjoy!

Testing
-------
You will need `python-nose` and `python-mock`. To run the test, simply run
`nosetests` or `nosetests3`, depending on your distribution.

Authors
-------
* Sean B. Palmer, http://inamidst.com/sbp/
* mutantmonkey, http://mutantmonkey.in
