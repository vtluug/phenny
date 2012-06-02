"""
test_mylife.py - tests for the mylife module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock
from modules import mylife


class TestMylife(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_fml(self):
        mylife.fml(self.phenny, None)
        assert self.phenny.say.called is True

    def test_mlia(self):
        mylife.mlia(self.phenny, None)
        assert self.phenny.say.called is True

    def test_mlib(self):
        mylife.mlib(self.phenny, None)
        assert self.phenny.say.called is True

    def test_mlih(self):
        mylife.mlih(self.phenny, None)
        assert self.phenny.say.called is True

    def test_mlihp(self):
        mylife.mlihp(self.phenny, None)
        assert self.phenny.say.called is True

    def test_mlit(self):
        mylife.mlit(self.phenny, None)
        assert self.phenny.say.called is True

