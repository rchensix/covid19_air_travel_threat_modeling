# Ruiqi Chen
# July 27, 2020
# This is the main function for the COVID-19 air travel model
# It contains a serial implementation

import sys
from typing import Dict, Tuple

import model
    
def visualize_data(data_path: str):
    """Visualizes data stored at data_path and saves plots to same directory
    Args:
        data_path: str path to data file (plots will be saved to same directory)
    """
    pass

def serial_implementation():
    seed = 0
    t_incubation = 2
    t_infectious = 14
    init_conditions = {
        'San Francisco-Oakland-Berkeley CA MSA': (4731802, 0, 10, 0),
        'San Jose-Sunnyvale-Santa Clara CA MSA': (1990658, 0, 10, 0),
    }
    seir = model.SEIRTwoStepModel(seed, t_incubation=t_incubation, t_infectious=t_infectious, 
                                  start_mmyy='01-20', start_day=1, init_conditions=init_conditions)
    beta_airplane = 0.2  # Let's assume this is high bc airplane is tight quarters
    beta_metro_by_month = {
        '12-19': 0.1,
        '01-20': 0.1,
        '02-19': 0.1,
        '03-19': 0.05,
        '04-19': 0.02,
        '05-19': 0.02,
        '06-19': 0.1,
        '07-19': 0.15,
        '08-19': 0.15,
    }
    flight_load_factor_by_month = {
        '12-19': 1,
        '01-20': 0.9,
        '02-19': 0.9,
        '03-19': 0.2,
        '04-19': 0.2,
        '05-19': 0.4,
        '06-19': 0.6,
        '07-19': 0.7,
        '08-19': 0.7,
    }
    data_path = 'out/serial_data.txt'
    num_days_to_simulate = 240  # Ends in August at some point
    for day in range(num_days_to_simulate):
        sys.stdout.write('Simulating day {}'.format(day + 1))
        seir.step_airplane(beta_airplane, flight_load_factor_by_month[seir.mmyy])
        seir.step_metro(beta_metro_by_month[seir.mmyy])
    seir.write_to_log_file('data/test_240_day_log.txt')
    visualize_data(data_path)

def main():
    serial_implementation()

if __name__ == '__main__':
    main()