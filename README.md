phenny
======

This is a port of phenny, a Python IRC bot, to Python3. It is currently fairly
stable, but it has not been as well-tested as the original. It was developed
for #vtluug on OFTC.

New features include many new modules, IPv6 and TLS support (which requires
Python 3.2), and unit tests.

Compatibility with existing phenny modules has been mostly retained, but they
will need to be updated to run on Python3 if they do not already. All of the
core modules have been ported.

Installation
------------
1. Run `./phenny` - this creates a default config file
2. Edit `~/.phenny/default.py`
3. Run `./phenny` - this now runs phenny with your settings

Enjoy!

Testing
-------
You will need the Python3 versions of `python-nose` and `python-mock`. To run
the tests, simply run `nosetests3`.

Authors
-------
* Sean B. Palmer, http://inamidst.com/sbp/
* mutantmonkey, http://mutantmonkey.in
