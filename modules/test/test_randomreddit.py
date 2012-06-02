"""
test_randomredit.py - tests for the randomreddit module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.randomreddit import randomreddit


class TestRandomreddit(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_randomreddit(self):
        input = Mock(group=lambda x: 'vtluug')
        randomreddit(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^http://.+? \(.*\)$',
                out, flags=re.UNICODE)
        self.assertTrue(m)
