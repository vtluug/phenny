"""
test_short.py - tests for the vtluug url shortener module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.short import short


class TestShort(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_short(self):
        input = Mock(group=lambda x: 'http://vtluug.org/')
        short(self.phenny, input)

        self.phenny.reply.assert_called_once_with('http://vtlu.ug/bLQYAy')
