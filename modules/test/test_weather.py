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

    def test_locations(self):
        def check_places(*args):
            def validate(actual_name, actual_lat, actual_lon):
                names = [n.strip() for n in actual_name.split(',')]
                for arg in args:
                    self.assertIn(arg, names)
            return validate

        locations = [
            ('24060', check_places("Blacksburg", "Virginia")),
            ('92121', check_places("San Diego", "California")),
            ('94110', check_places("San Francisco", "California")),
            ('94041', check_places("Mountain View", "California")),
            ('27959', check_places("Nags Head", "North Carolina")),
            ('48067', check_places("Royal Oak", "Michigan")),
            ('23606', check_places("Newport News", "Virginia")),
            ('23113', check_places("Midlothian", "Virginia")),
            ('27517', check_places("Chapel Hill", "North Carolina")),
            ('46530', check_places("Granger", "Indiana")),
            ('15213', check_places("Pittsburgh", "Pennsylvania")),
            ('90210', check_places("Beverly Hills", "California")),
            ('12144', check_places("Clinton Park", "New York")),
            ('33109', check_places("Homestead", "Florida")),
            ('80201', check_places("Denver", "Colorado")),

            ("Berlin", check_places("Berlin", "Deutschland")),
            ("Paris", check_places("Paris", "France métropolitaine")),
            ("Vilnius", check_places("Vilnius", "Lietuva")),
        ]

        for loc, validator in locations:
            names, lat, lon = location(loc)
            validator(names, lat, lon)

    def test_code_20164(self):
        icao = code(self.phenny, '20164')
        self.assertEqual(icao, 'KIAD')

    def test_airport(self):
        input = Mock(group=lambda x: 'KIAD')
        f_weather(self.phenny, input)
        
        assert self.phenny.say.called is True

    def test_place(self):
        input = Mock(group=lambda x: 'Blacksburg')
        f_weather(self.phenny, input)
        
        assert self.phenny.say.called is True

    def test_notfound(self):
        input = Mock(group=lambda x: 'Hell')
        f_weather(self.phenny, input)
        
        self.phenny.say.called_once_with('#phenny',
                "No NOAA data available for that location.")
