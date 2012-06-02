"""
test_nodetodo.py - tests for the node-todo xss module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.nodetodo import xss, urlshortener


class TestNodeTodo(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_xss(self):
        input = Mock(group=lambda x: 'http://vtluug.org/')
        xss(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^http://node-todobin\.herokuapp\.com/list/[a-z0-9]+$',
                out, flags=re.UNICODE)
        self.assertTrue(m)
