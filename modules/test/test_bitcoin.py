"""
test_bitcoin.py - tests for the bitcoin
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.bitcoin import bitcoin


class TestCalc(unittest.TestCase):
    def makegroup(*args):
        args2 = [] + list(args)
        def group(x):
            if x > 0 and x <= len(args2):
                return args2[x - 1]
            else:
                return None
        return group

    def setUp(self):
        self.phenny = MagicMock()

    def test_negative(self):
        input = Mock(group=self.makegroup('1', 'USD'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'[\d\.]+ BTC')

    def test_usd(self):
        input = Mock(group=self.makegroup('1', 'USD'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'[\d\.]+ BTC')

    def test_usd_decimal(self):
        input = Mock(group=self.makegroup('1.25', 'USD'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'[\d\.]+ BTC')

    def test_eur(self):
        input = Mock(group=self.makegroup('1', 'EUR'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'[\d\.]+ BTC')

    def test_xzz(self):
        input = Mock(group=self.makegroup('1', 'XZZ'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertNotRegex(out, r'[\d\.]+ BTC')

    def test_btc(self):
        input = Mock(group=self.makegroup('1', 'BTC'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'\d+\.\d{2} USD')

    def test_btcusd(self):
        input = Mock(group=self.makegroup('1', 'BTC', 'USD'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'\d+\.\d{2} USD')

    def test_eurbtc(self):
        input = Mock(group=self.makegroup('1', 'BTC', 'EUR'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'\d+\.\d{2} EUR')

    def test_xzzbtc(self):
        input = Mock(group=self.makegroup('1', 'BTC', 'XZZ'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertNotRegex(out, r'[\d\.]+ BTC')

    def test_invalid(self):
        input = Mock(group=self.makegroup('.-1', 'USD'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertNotRegex(out, r'[\d\.]+ BTC')

    def test_lettercase(self):
        input = Mock(group=self.makegroup('1', 'btc', 'EuR'))
        bitcoin(self.phenny, input)

        out = self.phenny.say.call_args[0][0]
        self.assertRegex(out, r'\d+\.\d{2} EUR')
