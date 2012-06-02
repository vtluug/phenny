"""
test_nsfw.py - some things just aren't safe for work, the test cases
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.nsfw import nsfw


class TestNsfw(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_nsfw(self):
        input = Mock(group=lambda x: "test")
        nsfw(self.phenny, input)

        self.phenny.say.assert_called_once_with(
                "!!NSFW!! -> test <- !!NSFW!!")
