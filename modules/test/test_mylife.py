"""
test_mylife.py - tests for the mylife module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock, Mock
from modules import mylife


class TestMylife(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_fml(self):
        mylife.fml(self.phenny, None)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out,
            "I tried to use .fml, but it was broken. FML")

    def test_mlia(self):
        mylife.mlia(self.phenny, None)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out,
            "I tried to use .mlia, but it wasn't loading. MLIA")

    def test_mlib(self):
        mylife.mlib(self.phenny, None)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out,
            "MLIB is out getting a case of Natty. It's chill.")

    def test_mlih(self):
        mylife.mlih(self.phenny, None)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out,
            "MLIH is giving some dome to some lax bros.")

    def test_mlihp(self):
        mylife.mlihp(self.phenny, None)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out,
            "This service is not available to Muggles.")

    def test_mlit(self):
        mylife.mlit(self.phenny, None)
        out = self.phenny.say.call_args[0][0]

        self.assertNotEqual(out,
           "Error: Your life is too Twilight. Go outside.")
