"""
test_search.py - tests for the search module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.search import duck_api, google_search, google_count, \
        formatnumber, g, gc, gcs, bing_search, bing, duck_search, duck, \
        search


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_google_search(self):
        out = google_search('phenny')

        m = re.match('^https?://.*$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_g(self):
        input = Mock(group=lambda x: 'swhack')
        g(self.phenny, input)

        assert self.phenny.reply.called is True

    def test_gc(self):
        query = 'extrapolate'
        input = Mock(group=lambda x: query)
        gc(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^{0}: [0-9,\.]+$'.format(query), out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_gcs(self):
        input = Mock(group=lambda x: 'vtluug virginia phenny')
        gcs(self.phenny, input)

        assert self.phenny.say.called is True

    def test_bing_search(self):
        out = bing_search('phenny')

        m = re.match('^https?://.*$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_bing(self):
        input = Mock(group=lambda x: 'swhack')
        bing(self.phenny, input)

        assert self.phenny.reply.called is True

    def test_duck_search(self):
        out = duck_search('phenny')

        m = re.match('^https?://.*$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_duck(self):
        input = Mock(group=lambda x: 'swhack')
        duck(self.phenny, input)

        assert self.phenny.reply.called is True

    def test_duck_api(self):
        input = Mock(group=lambda x: 'swhack')
        duck(self.phenny, input)

    def test_search(self):
        input = Mock(group=lambda x: 'vtluug')
        duck(self.phenny, input)

        assert self.phenny.reply.called is True
