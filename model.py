# Ruiqi Chen
# July 27, 2020
# Implements discrete SEIR model as described in Eq. 1-7 in this reference:
# https://doi.org/10.1111/j.1541-0420.2006.00609.x

from typing import Dict, Tuple

import numpy as np

import utils

class SEIRTwoStepModel:
    def __init__(self, seed: int, t_incubation: float=2, t_infectious: float=14):
        """Initialize two step SEIR model with parameters
        Args:
            seed: random seed
            t_incubation: mean incubation period in days
            t_infectious: mean infectious period in days
        """
        self.seed = seed
        np.random.seed(self.seed)
        self.t_incubation = t_incubation
        self.t_infectious = t_infectious
        self._load_data()
        self.population = self._init_population()
        
    def _load_data(self):
        """Load data from pre-defined directories"""
        # Load city information

        # Load airplane information
        # Load airport information
        # Load flight information (throw out any flights that depart/arrive in a city not in the
        #     list of cities, or using a plane not in the list of airplanes)

    def _init_population(self):
        """Initialize S, E, I, R populations for all metro areas"""
        pass
    
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