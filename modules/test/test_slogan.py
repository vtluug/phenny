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

        assert len(out) > 0

    def test_slogan(self):
        input = Mock(group=lambda x: 'slogan')
        slogan(self.phenny, input)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out, "Looks like an issue with sloganizer.net")
