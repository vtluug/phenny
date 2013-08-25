"""
test_slogan.py - tests for the slogan module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.slogan import sloganize, slogan


class TestSlogan(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_sloganize(self):
        out = sloganize('slogan')
        self.assertRegex(out, ".*slogan.*")

    def test_slogan(self):
        input = Mock(group=lambda x: 'slogan')
        slogan(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, ".*slogan.*")

    def test_slogan_none(self):
        input = Mock(group=lambda x: None)
        slogan(self.phenny, input)
        self.phenny.say.assert_called_once_with(
            "You need to specify a word; try .slogan Granola")
