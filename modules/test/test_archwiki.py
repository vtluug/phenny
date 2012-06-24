"""
test_archwiki.py - tests for the arch wiki module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules import archwiki


class TestArchwiki(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_awik(self):
        input = Mock(groups=lambda: ['', "KVM"])
        archwiki.awik(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^.* - https:\/\/wiki\.archlinux\.org\/index\.php\/KVM$',
                out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_awik_invalid(self):
        term = "KVM#Enabling_KSM"
        input = Mock(groups=lambda: ['', term])
        archwiki.awik(self.phenny, input)

        self.phenny.say.assert_called_once_with( "Can't find anything in "\
                "the ArchWiki for \"{0}\".".format(term))

    def test_awik_none(self):
        term = "Ajgoajh"
        input = Mock(groups=lambda: ['', term])
        archwiki.awik(self.phenny, input)

        self.phenny.say.assert_called_once_with( "Can't find anything in "\
                "the ArchWiki for \"{0}\".".format(term))
