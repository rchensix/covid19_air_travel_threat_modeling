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
        }
        
    def _load_data(self):
        """Load data from pre-defined directories"""
        # Load metro information
        with open('data/metropolitan_areas.json', 'r') as f:
            self.metropolitan_areas = json.load(f)
        # Load airplane information
        with open('data/aircrafts.json', 'r') as f:
            self.aircrafts = dict()
            aircrafts = json.load(f)
            # json stores keys as strings so lets convert them back to int
            for key, val in aircrafts.items():
                self.aircrafts[int(key)] = val
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

    def step_airplane(self, beta: float, flight_load_factor: float):
        """Loops through all flights and calculates number of people that get sick according to
        discrete SEIR model with transmission rate beta. Updates all metro areas with new S,
        E, I, R populations.
        Args:
            beta: transmission rate aboard airplane (number between 0-1)
            flight_load_factor: scaling factor to multiply number of passengers by on each flight
        """
        flights = self.flights[self.mmyy]
        population_change = dict()
        for flight in flights:
            origin = flight[0]
            dest = flight[1]
            ac_type = flight[2]
            if origin not in self.airports.keys(): continue
            if dest not in self.airports.keys(): continue
            if ac_type not in self.aircrafts.keys(): continue
            # For every flight, calculate S, E, I, R population aboard airplane based on flight origin
            num_pax = int(self.aircrafts[ac_type] * flight_load_factor)
            orig_metro = self.airports[origin]
            _, _, s0, e0, i0, r0 = self.population[orig_metro][-1]
            pvals = np.array([s0, e0, i0, r0]) / (s0 + e0 + i0 + r0)
            s0, e0, i0, r0 = np.random.multinomial(num_pax, pvals, size=1)[0]
            # "Remove" people from population origin (record negative population change)
            if orig_metro in population_change.keys():
                population_change[orig_metro][0] -= s0
                population_change[orig_metro][1] -= e0
                population_change[orig_metro][2] -= i0
                population_change[orig_metro][3] -= r0
            else:
                population_change[orig_metro] = [-s0, -e0, -i0, -r0]
            # Step S, E, I, R variables based on flight beta
            s1, e1, i1, r1 = self._step_seir(s0, e0, i0, r0, beta, self.t_incubation, self.t_infectious)
            # Update destination S, E, I, R populations locally
            dest_metro = self.airports[dest]
            if dest_metro in population_change.keys():
                population_change[dest_metro][0] += s1
                population_change[dest_metro][1] += e1
                population_change[dest_metro][2] += i1
                population_change[dest_metro][3] += r1
            else:
                population_change[dest_metro] = [s1, e1, i1, r1]
        # Update global population data
        for metro, delta in population_change.items():
            mmyy, dd, s0, e0, i0, r0 = self.population[metro][-1]
            ds, de, di, dr = delta
            new_data = (mmyy, dd, s0 + ds, e0 + de, i0 + di, r0 + dr)
            self.population[metro].append(new_data)
        
    def step_metro(self, beta: float):
        """Loops through all metropolitan areas and updates S, E, I, R populations
        Args:
            beta: transmission rate within metro area (number between 0-1)
        """
        self._step_date()
        for metro in self.population.keys():
            mmyy, dd, s0, e0, i0, r0 = self.population[metro][-1]
            s1, e1, i1, r1 = self._step_seir(s0, e0, i0, r0, beta, self.t_incubation, self.t_infectious)
            new_data = (self.mmyy, self.day, s1, e1, i1, r1)
            self.population[metro].append(new_data)

    def _step_date(self):
        day = self.day + 1
        mmyy = self.mmyy
        if day > self.num_days_per_month[self.mmyy]:
            day = 1
            mmyy = self._next_month(mmyy)
        self.mmyy = mmyy
        self.day = day

    def _next_month(self, mmyy: str):
        d = {
            '11-19': '12-19',
            '12-19': '01-20',
            '01-20': '02-19',
            '02-19': '03-19',
            '03-19': '04-19',
            '04-19': '05-19',
            '05-19': '06-19',
            '06-19': '07-19',
            '07-19': '08-19',
            '08-19': '08-19',  # There's no mmyy after this!
        }
        return d[mmyy]

    def _step_seir(self, s: float, e: float, i: float, r: float, beta: float, t_incubation: float,
                   t_infectious: float) -> Tuple[int, int, int, int]:
        """Increments S, E, I, R variables using Eqs. 1-7 in the following source:
        DOI: 10.1111/j.1541-0420.2006.00609.x
        Args:
            s: susceptible population
            e: exposed population
            i: infectious population
            r: removed population
        """
        # Calculate probabilities (Eq. 6 in source)
        n = s + e + i + r
        p = 1 - np.exp(-beta/n*i)
        pc = 1 - np.exp(-1/t_incubation)
        pr = 1 - np.exp(-1/t_infectious)
        # Calculate b, c, d (Eq. 5 in source)
        b = np.random.binomial(n, p)
        c = np.random.binomial(e, pc)
        d = np.random.binomial(i, pr)
        # Step s, e, i, r variables (Eqs. 1-4)
        # I've added maxes to make sure these all stay positive
        # Not sure if this makes any difference or not
        s1 = np.max(s - b, 0)
        e1 = np.max(e + b - c, 0)
        i1 = np.max(i + c - d, 0)
        r1 = np.max(n - s1 - e1 - i1, 0)
        return (s1, e1, i1, r1)
        
    def statistics(self) -> Dict[str, Tuple[float, float, float, float]]:
        """Return current simulation statistics
        Returns:
          Dict[str, Tuple[float, float, float, float]] where key is metro area name and tuple
          contains S, E, I, R population values in that order.
        """
        pass