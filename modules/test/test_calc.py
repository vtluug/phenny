"""
test_calc.py - tests for the calc module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.calc import c, wa


class TestCalc(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_c(self):
        input = Mock(group=lambda x: '5*5')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('25')

    def test_c_scientific(self):
        input = Mock(group=lambda x: '2^64')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('1.84467441 * 10^(19)')

    def test_c_none(self):
        input = Mock(group=lambda x: 'aif')
        c(self.phenny, input)

        self.phenny.reply.assert_called_once_with('Sorry, no result.')

    def test_wa(self):
        input = Mock(group=lambda x: 'airspeed of an unladen swallow')
        wa(self.phenny, input)

        self.phenny.say.assert_called_once_with('25 mph  (miles per hour)')

    def test_wa_none(self):
        input = Mock(group=lambda x: "jajoajaj ojewphjqo I!tj")
        wa(self.phenny, input)

        self.phenny.reply.assert_called_once_with('Sorry, no result.')
