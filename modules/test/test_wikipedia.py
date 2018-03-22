"""
test_wikipedia.py - tests for the wikipedia module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""
import unittest
from mock import MagicMock
from modules import wikipedia
import wiki


class TestWikipedia(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()
        self.input = MagicMock()

        self.term = None
        self.section = None

    def prepare(self):
        if self.section:
            self.text = self.term + '#' + self.section
            url_text = wiki.format_term(self.term) +\
                '#' + wiki.format_section(self.section)
        else:
            self.text = self.term
            url_text = wiki.format_term(self.term)

        self.input.groups.return_value = [None, self.text]
        self.url = 'https://en.wikipedia.org/wiki/{0}'.format(url_text)

    def check_snippet(self, output):
        self.assertIn(self.url, output)

        for keyword in self.keywords:
            self.assertIn(keyword, output)

    def test_wik(self):
        self.term = "Human back"
        self.prepare()

        wikipedia.wik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        self.keywords = ['human', 'back', 'body', 'buttocks', 'neck']
        self.check_snippet(out)

    def test_wik_fragment(self):
        self.term = "New York City"
        self.section = "Climate"
        self.prepare()

        wikipedia.wik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        self.keywords = ['New York', 'climate', 'humid', 'subtropical']
        self.check_snippet(out)

    def test_wik_invalid(self):
        self.term = "New York City"
        self.section = "Physics"
        self.prepare()

        wikipedia.wik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        message = "No '{0}' section found.".format(self.section)
        self.assertEqual(out, '"{0}" - {1}'.format(message, self.url))

    def test_wik_none(self):
        self.term = "Ajgoajh"
        self.prepare()

        wikipedia.wik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        expected = "Can't find anything in Wikipedia for \"{0}\"."
        self.assertEqual(out, expected.format(self.text))
