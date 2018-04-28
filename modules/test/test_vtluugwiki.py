"""
test_vtluugwiki.py - tests for the VTLUUG wiki module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""
import unittest
from mock import MagicMock
from modules import vtluugwiki
import wiki


class TestVtluugwiki(unittest.TestCase):
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
        self.url = 'https://vtluug.org/wiki/{0}'.format(url_text)

    def check_snippet(self, output):
        self.assertIn(self.url, output)

        for keyword in self.keywords:
            self.assertIn(keyword, output)

    def test_vtluug(self):
        self.term = "VT-Wireless"
        self.prepare()

        vtluugwiki.vtluug(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        self.keywords = ['campus', 'wireless', 'networks']
        self.check_snippet(out)

    def test_vtluug_fragment(self):
        self.term = "EAP-TLS"
        self.section = "netctl"
        self.prepare()

        vtluugwiki.vtluug(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        self.keywords = ['Arch', 'Linux', 'netctl']
        self.check_snippet(out)

    def test_vtluug_invalid(self):
        self.term = "EAP-TLS"
        self.section = "netcfg"
        self.prepare()

        vtluugwiki.vtluug(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        message = "No '{0}' section found.".format(self.section)
        self.assertEqual(out, '"{0}" - {1}'.format(message, self.url))

    def test_vtluug_none(self):
        self.term = "Ajgoajh"
        self.prepare()

        vtluugwiki.vtluug(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        expected = "Can't find anything in the VTLUUG Wiki for \"{0}\"."
        self.assertEqual(out, expected.format(self.text))

