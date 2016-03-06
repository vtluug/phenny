"""
test_lastfm.py - tests for the lastfm module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.lastfm import now_playing


class TestLastfm(unittest.TestCase):
    user1 = 'test'
    user2 = 'telnoratti'

    def setUp(self):
        self.phenny = MagicMock()

    def test_now_playing(self):
        input = Mock(group=lambda x: self.user1)
        now_playing(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^{0} listened to ".+" by .+ on .+ .*$'.format(self.user1), out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_now_playing_sender(self):
        input = Mock(group=lambda x: '')
        input.nick = self.user1
        now_playing(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^{0} listened to ".+" by .+ on .+ .*$'.format(self.user1), out, flags=re.UNICODE)
        self.assertTrue(m)
