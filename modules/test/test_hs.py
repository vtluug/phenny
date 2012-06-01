"""
test_hs.py - tests for the hokie stalker module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.hs import search, hs


class TestHs(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_search(self):
        data = search('john')

        assert len(data) >= 1
        assert 'uid' in data[0]
        assert 'cn' in data[0]

    def test_single(self):
        input = Mock(group=lambda x: 'marchany')
        hs(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match(
            '^.* - http://search\.vt\.edu/search/person\.html\?person=\d+$',
            out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_multi(self):
        input = Mock(group=lambda x: 'john')
        hs(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match(
            '^Multiple results found; try http://search\.vt\.edu/search/people\.html\?q=.*$',
            out, flags=re.UNICODE)
        self.assertTrue(m)
