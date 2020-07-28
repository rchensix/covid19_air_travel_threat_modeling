# Ruiqi Chen
# July 27, 2020

import unittest

import utils

class TestUtils(unittest.TestCase):
    def test_parse_metropolitan_areas(self):
        metro_data = utils.parse_metropolitan_areas()
        # Check a particular metro area
        self.assertEqual(metro_data['San Francisco-Oakland-Berkeley CA MSA'], 4731803)
        # Check total number of entries
        self.assertEqual(len(metro_data.keys()), 53)
        # Check that all population entries are greater than 1000000
        for _, v in metro_data.items():
            self.assertGreaterEqual(v, 1000000)

    def test_parse_aircraft_capacity(self):
        aircraft_capacity = utils.parse_aircraft_capacity()
        # Check a particular aircraft
        self.assertEqual(aircraft_capacity[838], 178)
        # Check number of aircrafts in database
        self.assertEqual(len(aircraft_capacity.keys()), 68)
    
    def test_parse_airports(self):
        airports = utils.parse_airports()
        # Check some particular airports
        self.assertEqual(airports['SJC'], 'San Jose-Sunnyvale-Santa Clara, CA MSA')
        self.assertEqual(airports['SFO'], 'San Francisco-Oakland-Berkeley, CA MSA')
        self.assertEqual(airports['OAK'], airports['SFO'])
        # Check total number of airports
        self.assertEqual(len(airports.keys()), 85)

    def test_parse_flights(self):
        flights = utils.parse_flight_data()
        # Test on test dataset
        self.assertEqual(len(flights['test']), 23)
        flight_las_sjc = flights['test'][1]
        self.assertEqual(flight_las_sjc[0], 'LAS')
        self.assertEqual(flight_las_sjc[1], 'SJC')
        self.assertEqual(flight_las_sjc[2], 612)

if __name__ == '__main__':
    unittest.main()