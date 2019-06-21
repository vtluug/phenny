# coding=utf-8
"""
test_calc.py - tests for the calc module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules.calc import c


class TestCalc(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_c(self):
        input = Mock(group=lambda x: '5*5')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('25')

    def test_c_simplify(self):
        input = Mock(group=lambda x: 'simplify 2^2+2(2)')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('8')

    def test_c_factor(self):
        input = Mock(group=lambda x: 'factor x^2 + 2x')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('x (x + 2)')

    def test_c_derive(self):
        input = Mock(group=lambda x: 'derive x^2+2x')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('2 x + 2')

    def test_c_integrate(self):
        input = Mock(group=lambda x: 'integrate x^2+2x')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('1/3 x^3 + x^2')

    def test_c_zeroes(self):
        input = Mock(group=lambda x: 'zeroes x^2+2x')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('[-2, 0]')

    def test_c_tangent(self):
        input = Mock(group=lambda x: 'tangent 2|x^3')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('12 x + -16')

    def test_c_area(self):
        input = Mock(group=lambda x: 'area 2:4|x^3')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('60')

    def test_c_cos(self):
        input = Mock(group=lambda x: 'cos pi')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('-1')

    def test_c_sin(self):
        input = Mock(group=lambda x: 'sin 0')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('0')

    def test_c_tan(self):
        input = Mock(group=lambda x: 'tan .03')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('0.030009')

    def test_c_arccos(self):
        input = Mock(group=lambda x: 'arccos 1')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('0')

    def test_c_arcsin(self):
        input = Mock(group=lambda x: 'arcsin .04')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('0.0400107')

    def test_c_arctan(self):
        input = Mock(group=lambda x: 'arctan 1')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('1/2 pi')

    def test_c_abs(self):
        input = Mock(group=lambda x: 'abs -3')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('3')

    def test_c_log(self):
        input = Mock(group=lambda x: 'log 2|8')
        c(self.phenny, input)

        self.phenny.say.assert_called_once_with('3')

    def test_c_none(self):
        input = Mock(group=lambda x: 'tangent 2lx^3')
        c(self.phenny, input)

        self.phenny.reply.assert_called_once_with('Sorry, no result.')
