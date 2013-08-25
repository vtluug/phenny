"""
test_imdb.py - tests for the imdb module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.imdb import imdb_search, imdb


class TestImdb(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_imdb_search(self):
        data = imdb_search('Hackers')

        assert 'Plot' in data
        assert 'Title' in data
        assert 'Year' in data
        assert 'imdbID' in data

    def test_imdb(self):
        input = Mock(group=lambda x: 'Antitrust')
        imdb(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        pattern = re.compile(
            r'^.* \(.*\): .* http://imdb.com/title/[a-z\d]+$',
            flags=re.UNICODE)
        self.assertRegex(out, pattern)

    def test_imdb_none(self):
        input = Mock(group=lambda x: None)
        imdb(self.phenny, input)

        self.phenny.say.assert_called_once_with(
            ".imdb what?")
