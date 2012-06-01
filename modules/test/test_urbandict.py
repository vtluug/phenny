"""
test_urbandict.py - tests for the urban dictionary module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.urbandict import urbandict


class TestUrbandict(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_result(self):
        word = 'slemp'
        input = Mock(group=lambda x: word)
        urbandict(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^.* - '\
                'http://www\.urbandictionary\.com/define\.php\?term=.*$', out,
                flags=re.UNICODE)
        self.assertTrue(m)

    def test_none(self):
        word = '__no_word_here__'
        input = Mock(group=lambda x: word)
        urbandict(self.phenny, input)

        self.phenny.say.assert_called_once_with('No results found for '\
                '{0}'.format(word))
