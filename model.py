# Ruiqi Chen
# July 27, 2020
# Implements discrete SEIR model as described in Eq. 1-7 in this reference:
# https://doi.org/10.1111/j.1541-0420.2006.00609.x

import json
from typing import Dict, Tuple, Union

import numpy as np

import utils

class SEIRTwoStepModel:
    def __init__(self, seed: int, t_incubation: float=2, t_infectious: float=14,
                 start_mmyy: str='11-19', start_day: int=1, 
                 init_conditions: Union[None, Dict[str, Tuple[float, float, float, float]]]=None):
        """Initialize two step SEIR model with parameters
        Args:
            seed: random seed
            t_incubation: mean incubation period in days
            t_infectious: mean infectious period in days
            start_mmyy: simulation start month and year in mm-yy format (e.g. '11-19')
            start_day: simulation start day of the month
            init_conditions: initial conditions in the form d[metro_name] = (s, e, i, r) 
        """
        self.seed = seed
        np.random.seed(self.seed)
        self.t_incubation = t_incubation
        self.t_infectious = t_infectious
        self.start_mmyy = start_mmyy
        self.mmyy = start_mmyy
        self.start_day = start_day
        self.day = start_day
        self.init_conditions = init_conditions
        self._load_data()
        self._init_population()
        self._load_constants()

    def _load_constants(self):
        self.order_of_months = [
            '11-19',
            '12-19', 
            '01-20', 
            '02-19',
            '03-19',
            '04-19',
            '05-19',
            '06-19',
            '07-19',
            '08-19',
        ]
        self.num_days_per_month = {
            '11-19': 30,
            '12-19': 31,
            '01-20': 31,
            # Use 2019 data for remaining months in 2020
            '02-19': 29,  # 2020 is a leap year while 2019 was not
            '03-19': 31,
            '04-19': 30,
            '05-19': 31,
            '06-19': 30,
            '07-19': 31,
            '08-19': 31,
            '09-19': 30,
            '10-19': 31,
            '11-19': 30,
        }
        
    def _load_data(self):
        """Load data from pre-defined directories"""
        # Load metro information
        with open('data/metropolitan_areas.json', 'r') as f:
            self.metropolitan_areas = json.load(f)
        # Load airplane information
        with open('data/aircrafts.json', 'r') as f:
            self.aircrafts = json.load(f)
        # Load airport information
        with open('data/airports.json', 'r') as f:
            self.airports = json.load(f)
        # Load flight information
        with open('data/flights.json', 'r') as f:
            self.flights = json.load(f)

    def _init_population(self):
        """Initialize S, E, I, R populations for all metro areas
        Population data is stored as a dict in the following format:
            population[metro_name] = List[(mm-yy, day, s, e, i, r), ...]
        """
        self.population = dict()
        for metro, population in self.metropolitan_areas.items():
            if self.init_conditions != None and metro in self.init_conditions.keys():
                s, e, i, r = self.init_conditions[metro]
                self.population[metro] = [(self.mmyy, self.day, s, e, i, r)]
            else:
                self.population[metro] = [(self.mmyy, self.day, population, 0, 0, 0)]

    def step_airplane(self, beta: float, data: str, flight_load_factor: float):
        """Loops through all flights and calculates number of people that get sick according to
        discrete SEIR model with transmission rate beta. Updates all metro areas with new S,
        E, I, R populations.
        Args:
            beta: transmission rate aboard airplane (number between 0-1)
            data: which airplane month data to use, in the format mm-yy (e.g. '09-19')
            flight_load_factor: scaling factor to multiply number of passengers by on each flight
        """
        pass
        
    def step_metro(self, beta: float):
        """Loops through all metropolitan areas and updates S, E, I, R populations
        Args:
            beta: transmission rate within metro area (number between 0-1)
        """
        pass
        
    def statistics(self) -> Dict[str, Tuple[float, float, float, float]]:
        """Return current simulation statistics
        Returns:
          Dict[str, Tuple[float, float, float, float]] where key is metro area name and tuple
          contains S, E, I, R population values in that order.
        """
        pass