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
        # Make sure all capacities are greater than 0
        for _, v in aircraft_capacity.items():
            self.assertGreater(v, 0)
    
    def test_parse_airports(self):
        airports = utils.parse_airports()
        # Check some particular airports
        self.assertEqual(airports['SJC'], 'San Jose-Sunnyvale-Santa Clara CA MSA')
        self.assertEqual(airports['SFO'], 'San Francisco-Oakland-Berkeley CA MSA')
        self.assertEqual(airports['OAK'], airports['SFO'])
        # Check total number of airports
        self.assertEqual(len(airports.keys()), 84)
        # All aircraft codes should be three letters
        for k in airports.keys():
            self.assertEqual(len(k), 3)

    def test_parse_flights(self):
        flights = utils.parse_flight_data()
        # Test on test dataset
        self.assertEqual(len(flights['test']), 23)
        flight_las_sjc = flights['test'][1]
        self.assertEqual(flight_las_sjc[0], 'LAS')
        self.assertEqual(flight_las_sjc[1], 'SJC')
        self.assertEqual(flight_las_sjc[2], 612)
        # Check that all airport codes are three letters
        # Check all dates are formatted as 'mm-yy' (i.e. length 5)
        # Check all aircraft type IDs are greater than 0
        for k, v in flights.items():
            if k != 'test': self.assertEqual(len(k), 5)
            for flight in v:
                self.assertEqual(len(flight[0]), 3)
                self.assertEqual(len(flight[1]), 3)
                self.assertGreater(flight[2], 0)

    def test_json(self):
        flight_data = utils.parse_flight_data()
        airports = utils.parse_airports()
        metropolitan_areas = utils.parse_metropolitan_areas()
        aircraft_capacity = utils.parse_aircraft_capacity()
        utils.write_json(flight_data, 'data/flights.json')
        utils.write_json(airports, 'data/airports.json')
        utils.write_json(metropolitan_areas, 'data/metropolitan_areas.json')
        utils.write_json(aircraft_capacity, 'data/aircrafts.json')

if __name__ == '__main__':
    unittest.main()