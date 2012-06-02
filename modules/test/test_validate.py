"""
test_validate.py - tests for the validation module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.validate import val


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_valid(self):
        url = 'http://vtluug.org/'
        input = Mock(group=lambda x: url)
        val(self.phenny, input)

        self.phenny.reply.assert_called_once_with('{0} is Valid'.format(url))

    def test_invalid(self):
        url = 'http://microsoft.com/'
        input = Mock(group=lambda x: url)
        val(self.phenny, input)

        out = self.phenny.reply.call_args[0][0]
        m = re.match('^{0} is Invalid \(\d+ errors\)'.format(url),
                out, flags=re.UNICODE)
        self.assertTrue(m)
