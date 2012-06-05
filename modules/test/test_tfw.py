"""
test_tfw.py - tests for the fucking weather module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
import tools
from mock import MagicMock, Mock
from modules.tfw import tfw


class TestTfw(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_badloc(self):
        input = Mock(group=lambda x: 'tu3jgoajgoahghqog')
        tfw(self.phenny, input)
    
        self.phenny.say.assert_called_once_with("UNKNOWN FUCKING LOCATION. Try another?")

    def test_celsius(self):
        input = Mock(group=lambda x: '24060')
        tfw(self.phenny, input, celsius=True)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^\d+°C‽ .* \- .*$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_fahrenheit(self):
        input = Mock(group=lambda x: '24060')
        tfw(self.phenny, input, fahrenheit=True)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^\d+°F‽ .* \- .*$', out, flags=re.UNICODE)
        self.assertTrue(m)

    def test_mev(self):
        input = Mock(group=lambda x: '24060')
        tfw(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        m = re.match('^[\d\.]+ meV‽ .* \- .*$', out, flags=re.UNICODE)
        self.assertTrue(m)
