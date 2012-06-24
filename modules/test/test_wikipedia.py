"""
test_wikipedia.py - tests for the wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules import wikipedia


class TestWikipedia(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_wik(self):
        input = Mock(groups=lambda: ['', "Human back"])
        wikipedia.wik(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^.* - https:\/\/en\.wikipedia\.org\/wiki\/Human_back$',
                out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_wik_invalid(self):
        term = "New York City#Climate"
        input = Mock(groups=lambda: ['', term])
        wikipedia.wik(self.phenny, input)

        self.phenny.say.assert_called_once_with( "Can't find anything in "\
                "Wikipedia for \"{0}\".".format(term))

    def test_wik_none(self):
        term = "Ajgoajh"
        input = Mock(groups=lambda: ['', term])
        wikipedia.wik(self.phenny, input)

        self.phenny.say.assert_called_once_with( "Can't find anything in "\
                "Wikipedia for \"{0}\".".format(term))
