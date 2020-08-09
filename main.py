# Ruiqi Chen
# August 9, 2020
# This is the main function for the COVID-19 air travel model

import argparse
import os
import sys
from typing import Dict, Tuple, Union

import fast_model
import model
import utils

def implementation(sim_params: Dict):
    t_incubation = sim_params['t_incubation']
    t_infectious = sim_params['t_infectious']
    init_conditions = sim_params['init_conditions']
    mode = sim_params['mode']
    num_procs = sim_params['num_procs']
    seed = sim_params['seed']
    start_mmyy = sim_params['start_mmyy']
    start_day = sim_params['start_day']
    beta_airplane = sim_params['beta_airplane']
    beta_metro = sim_params['beta_metro']
    flight_load_factor = sim_params['flight_load_factor']
    log_out_path = sim_params['log_out_path']
    num_days_to_simulate = sim_params['num_days_to_simulate']
    if mode == 'fast':
        if num_procs is None: num_procs = 1
        seir = fast_model.SEIRTwoStepModel(seed, t_incubation=t_incubation, t_infectious=t_infectious, 
                                           start_mmyy=start_mmyy, start_day=start_day, 
                                           init_conditions=init_conditions, num_procs=num_procs)
    elif mode == 'slow':
        seir = model.SEIRTwoStepModel(seed, t_incubation=t_incubation, t_infectious=t_infectious, 
                                      start_mmyy=start_mmyy, start_day=start_day, 
                                      init_conditions=init_conditions)
    else:
        raise Exception('Invalid mode {} selected. Mode must either be "fast" or "slow"'.format(mode))
    for day in range(num_days_to_simulate):
        sys.stdout.write('Simulating day {}\n'.format(day + 1))
        seir.step_airplane(beta_airplane[seir.mmyy], flight_load_factor[seir.mmyy])
        seir.step_metro(beta_metro[seir.mmyy])
    if log_out_path is None:
        default_path = 'sandbox/test_{}_day_log.txt'.format(num_days_to_simulate)
        seir.write_to_log_file(default_path)
    else:
        seir.write_to_log_file(log_out_path)

def parse_sim_params(json_path: str) -> Dict:
    return dict()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sim_param_file', type=str, help='json file with all sim params')
    args = parser.parse_args()
    sim_params = utils.parse_sim_params(args.sim_param_file)
    implementation(sim_params)

if __name__ == '__main__':
    main()