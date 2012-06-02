"""
test_catfacts.py - tests for the cat facts module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock
from modules.catfacts import catfacts


class TestCatfacts(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_catfacts(self):
        catfacts(self.phenny, None)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^.* \(#[0-9]+\)$', out,
                flags=re.UNICODE)
        self.assertTrue(m)
