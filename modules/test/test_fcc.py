"""
test_fcc.py - tests for the fcc callsign lookup module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.fcc import fcc


class TestFcc(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_result(self):
        callsign = 'KK4EWT'
        ham = 'JAMES B WILLIAMS'
        key = 3326562

        input = Mock(group=lambda x: 'KK4EWT')
        fcc(self.phenny, input)

        self.phenny.say.assert_called_once_with('{0} - {1} - '\
            'http://wireless2.fcc.gov/UlsApp/UlsSearch/license.jsp?licKey={2}'
            .format(callsign, ham, key))

    def test_none(self):
        callsign = 'XFOOBAR'

        input = Mock(group=lambda x: callsign)
        fcc(self.phenny, input)

        self.phenny.reply.assert_called_once_with('No results found for '\
                '{0}'.format(callsign))
