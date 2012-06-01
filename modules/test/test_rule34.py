"""
test_rule34.py - tests for the rule 34 module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.rule34 import rule34


class TestRule34(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_result(self):
        input = Mock(group=lambda x: 'python')
        rule34(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^!!NSFW!! -> http://rule34\.xxx/.* <- !!NSFW!!$', out,
                flags=re.UNICODE)
        self.assertTrue(m)
    def test_none(self):
        input = Mock(group=lambda x: '__no_results_for_this__')
        rule34(self.phenny, input)

        self.phenny.reply.assert_called_once_with(
                "You just broke Rule 34! Better start uploading...")
