"""
test_archwiki.py - tests for the arch wiki module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""
import unittest
from mock import MagicMock
from modules import archwiki
import wiki


class TestArchwiki(unittest.TestCase):
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

        self.input.group = lambda x: [None, self.text][x]
        self.url = 'https://wiki.archlinux.org/index.php/{0}'.format(url_text)

    def check_snippet(self, output):
        self.assertIn(self.url, output)

        for keyword in self.keywords:
            self.assertIn(keyword, output)

    def test_awik(self):
        self.term = "OpenDMARC"
        self.prepare()

        archwiki.awik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        self.keywords = ['policy', 'mail', 'transfer', 'providers']
        self.check_snippet(out)

    def test_awik_fragment(self):
        self.term = "KVM"
        self.section = "Kernel support"
        self.prepare()

        archwiki.awik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        self.keywords = ['kernel', 'modules', 'KVM', 'VIRTIO']
        self.check_snippet(out)

    def test_awik_invalid(self):
        self.term = "KVM"
        self.section = "Enabling KSM"
        self.prepare()

        archwiki.awik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        message = "No '{0}' section found.".format(self.section)
        self.assertEqual(out, '"{0}" - {1}'.format(message, self.url))

    def test_awik_none(self):
        self.term = "Ajgoajh"
        self.prepare()

        archwiki.awik(self.phenny, self.input)
        out = self.phenny.say.call_args[0][0]

        expected = "Can't find anything in the ArchWiki for \"{0}\"."
        self.assertEqual(out, expected.format(self.text))
