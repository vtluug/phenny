"""
test_lastfm.py - tests for the lastfm module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.lastfm import now_playing, tasteometer


class TestLastfm(unittest.TestCase):
    user1 = 'test'
    user2 = 'ackthet'

    def setUp(self):
        self.phenny = MagicMock()

    def test_now_playing(self):
        input = Mock(group=lambda x: self.user1)
        now_playing(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^{0} .*$'.format(self.user1), out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_now_playing_sender(self):
        input = Mock(group=lambda x: '')
        input.nick = self.user1
        now_playing(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^{0} .*$'.format(self.user1), out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_tasteometer(self):
        def mock_group(x):
            if x == 2:
                return self.user1
            else:
                return self.user2

        input = Mock(group=mock_group)
        tasteometer(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match("^{0}'s and {1}'s musical compatibility rating is .*"\
                " and music they have in common includes: .*$".
                format(self.user1, self.user2), out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_tasteometer_sender(self):
        def mock_group(x):
            if x == 2:
                return self.user1
            else:
                return ''

        input = Mock(group=mock_group)
        input.nick = self.user2
        tasteometer(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match("^{0}'s and {1}'s musical compatibility rating is .*"\
                " and music they have in common includes: .*$".
                format(self.user1, self.user2), out, flags=re.UNICODE)
        self.assertTrue(m)
