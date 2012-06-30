"""
test_weather.py - tests for the weather module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock, patch
from modules.weather import location, local, code, f_weather


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_location(self):
        name, countryName, lat, lng = location('24060')

        self.assertEqual(name, "Blacksburg")
        self.assertEqual(countryName, "United States")
        self.assertEqual(lat, 37.2295733)
        self.assertEqual(lng, -80.4139393)

    def test_code(self):
        icao = code(self.phenny, '20164')
        
        self.assertEqual(icao, 'KIAD')

    def test_airport(self):
        input = Mock(
                match=Mock(group=lambda x: 'KIAD'),
                sender='#phenny', nick='phenny_test')
        f_weather(self.phenny, input)
        
        assert self.phenny.msg.called is True

    def test_place(self):
        input = Mock(
                match=Mock(group=lambda x: 'Blacksburg'),
                sender='#phenny', nick='phenny_test')
        f_weather(self.phenny, input)
        
        assert self.phenny.msg.called is True

    def test_notfound(self):
        input = Mock(
                match=Mock(group=lambda x: 'Hell'),
                sender='#phenny', nick='phenny_test')
        f_weather(self.phenny, input)
        
        self.phenny.msg.called_once_with('#phenny',
                "No NOAA data available for that location.")
        
