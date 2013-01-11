"""
Tests for phenny's metar.py
"""

import unittest
import metar
import glob


class MetarTest(unittest.TestCase):
    def test_files(self):
        for station in glob.glob('test/metar/*.TXT'):
            with open(station) as f:
                w = metar.parse(f.read())
                assert w.station is not None
                assert w.time is not None
                assert w.cover is not None

                assert w.temperature > -100
                assert w.temperature < 100

                assert w.pressure is not None
