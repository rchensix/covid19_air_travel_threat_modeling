# Ruiqi Chen
# July 27, 2020
# This file contains utility functions for parsing CSV and TXT files

import json
import os
from typing import Any, Dict, List, Tuple

def file_parser(file_path: str, key_col: int, key_type: Any, val_col: int, val_type: Any,
                delimiter: str=',', rows_to_skip: int=0) -> Dict[Any, Any]:
    """Parses a text file and returns a data dictionary of the form d[key] = val
    Args:
        file_path: str path to file
        key_col: index of column containing keys
        key_type: all keys will be casted to this type
        val_col: index of column containing values
        val_type: all values will be casted to this type
        delimiter: separater between columns (defaults to comma)
        rows_to_skip: skip this number of rows at the beginning (defaults to 0)
    Returns:
        Dict[key_type, val_type]: dictionary of parsed data
    """
    assert os.path.isfile(file_path), '{} not found'.format(file_path)
    data = dict()
    with open(file_path) as f:
        i = 0
        for line in f:
            if i < rows_to_skip:
                i += 1
                continue
            split_line = line.rstrip().split(sep=delimiter)
            data[key_type(split_line[key_col])] = val_type(split_line[val_col])
    return data

def parse_metropolitan_areas() -> Dict[str, int]:
    """Parse metropolitan data for name and population"""
    data_path = 'data/metropolitan_areas.csv'
    return file_parser(data_path, 1, str, 2, int, delimiter=',', rows_to_skip=2)

def parse_aircraft_capacity() -> Dict[int, int]:
    """Parse aircraft data for FAA aircraft identifier code and capacity"""
    data_path = 'data/aircraft_type.csv'
    return file_parser(data_path, 0, int, 2, int, delimiter=',', rows_to_skip=1)

def parse_airports() -> Dict[str, str]:
    """Parse airport list for metro name and set of airports in each metro area"""
    data_path = 'data/airports.txt'
    raw_data = file_parser(data_path, 0, str, 1, str, delimiter='|', rows_to_skip=2)
    # Convert to d[airport_code] = metro_name
    airports = dict()
    for metro, airport_list in raw_data.items():
        airport_codes = airport_list.rstrip().split(',')  # Remove newline and split by commas
        for code in airport_codes: airports[code] = metro
    return airports

def parse_flight_data() -> Dict[str, List[Tuple[str, str, int]]]:
    """Parse flight data and returns dictionary of flights by month/year
    Returns:
        Dict[str, List[str, str, int]]: d['mm-yy'] = [(origin_code, dest_code, aircraft_code), ...]
    """
    data_paths = {
        'test': 'data/test_flight_data.csv',
        '11-19': 'data/Nov2019_flight_data.csv',
        '12-19': 'data/Dec2019_flight_data.csv',
        '01-20': 'data/Jan2020_flight_data.csv',
        '02-19': 'data/Feb2019_flight_data.csv',
        '03-19': 'data/Mar2019_flight_data.csv',
        '04-19': 'data/Apr2019_flight_data.csv',
        '05-19': 'data/May2019_flight_data.csv',
        '06-19': 'data/Jun2019_flight_data.csv',
        '07-19': 'data/Jul2019_flight_data.csv',
        '08-19': 'data/Aug2019_flight_data.csv',
    }
    flight_data = dict()
    for month_year, data_path in data_paths.items():
        flight_data[month_year] = list()
        with open(data_path) as f:
            lines_to_skip = 1
            i = 0
            for line in f:
                if i < lines_to_skip:
                    i += 1
                    continue
                split_line = line.rstrip().split(',')
                try:
                    int(split_line[11])
                except:
                    raise Exception('Bad line: {}'.format(line))
                flight_data[month_year].append((split_line[4], split_line[8], int(split_line[11])))
    return flight_data

def write_json(data: Dict, out_path: str):
    """Writes dict as serialized json
    Args:
        data: Dict containing data to serialize
        out_path: path to json file
    """
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)

def parse_simulation_log(filepath: str) -> Dict[str, List[Tuple[str, int, float, float, float, float]]]:
    assert os.path.isfile(filepath), '{} not a valid file'.format(filepath)
    with open(filepath) as f:
        line_count = 0
        current_metro = None
        sim_data = dict()
        for line in f:
            # Skip first line
            if line_count == 0: 
                line_count += 1
                continue
            # Start parsing for this city
            if 'MSA' in line:
                current_metro = line.rstrip()
                sim_data[current_metro] = list()
                continue
            if current_metro is not None:
                split_line = line.split(',')
                datapoint = (split_line[0], int(split_line[1]), float(split_line[2]),
                             float(split_line[3]), float(split_line[4]), float(split_line[5]))
                sim_data[current_metro].append(datapoint)
    return sim_data

def main():
    pass

if __name__ == '__main__':
    main()