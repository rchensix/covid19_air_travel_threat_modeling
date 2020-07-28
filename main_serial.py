# Ruiqi Chen
# July 27, 2020
# This is the main function for the COVID-19 air travel model
# It contains a serial implementation

from typing import Dict, Tuple

import model

def log_data(data_path: str, month: str, day: int, 
             stats: Dict[str, Tuple[float, float, float, float]], remarks: str):
    """Logs data to file
    Args:
        data_path: str path to data file to append data to
        month: formatted mm-yy, e.g. '09-19'
        day: day of the month
        stats: what is returned by calling model.SEIRTwoStepModel.statistics()
        remarks: any str that will be appended to the log
    """
    pass
    
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
    seir = model.SEIRTwoStepModel(seed, t_incubation, t_infectious)
    months_to_simulate = [
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
    num_days_per_month = {
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
    # TODO(rchensix): Get better values for beta
    beta_airplane = 0.1  # Let's assume this is high bc airplane is tight quarters
    beta_metro_by_month = {
        '12-19': 0.01,
        '01-20': 0.01,
        '02-19': 0.02,
        '03-19': 0.05,
        '04-19': 0.02,
        '05-19': 0.02,
        '06-19': 0.05,
        '07-19': 0.08,
        '08-19': 0.1,
        '09-19': 0.12,
        '10-19': 0.15,
        '11-19': 0.15,
    }
    flight_load_factor_by_month = {
        '12-19': 0.9,
        '01-20': 0.9,
        '02-19': 0.9,
        '03-19': 0.2,
        '04-19': 0.2,
        '05-19': 0.4,
        '06-19': 0.6,
        '07-19': 0.7,
        '08-19': 0.7,
        '09-19': 0.7,
        '10-19': 0.7,
        '11-19': 0.7,
    }
    data_path = 'out/serial_data.txt'
    for month in months_to_simulate:
        for day in range(1, num_days_per_month[month] + 1):
            seir.step_airplane(beta_airplane, month, flight_load_factor_by_month[month])
            log_data(data_path, month, day, seir.statistics(), 'flight')
            seir.step_metro(beta_metro_by_month[month])
            log_data(data_path, month, day, seir.statistics(), 'ground')
    visualize_data(data_path)

def main():
    serial_implementation()

if __name__ == '__main__':
    main()