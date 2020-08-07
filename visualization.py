# Ruiqi Chen
# August 6, 2020
# This file contains various functions for visualizing our simulated data

import os
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import multiprocessing
import numpy as np

import utils

def _calculate_running_average(sim_data_list: List, metro: str) -> np.ndarray:
    n = len(sim_data_list)
    population = np.zeros((n, 4))
    for j in range(n):
        mmyy, d, s, e, i, r = sim_data_list[j][metro][-1]
        population[j] = np.array([s, e, i, r])
    return np.cumsum(population, axis=0) / np.arange(1, n + 1).reshape((-1, 1))

def running_average_plot(sim_files: List[str], metros_to_plot: List[str], out_path: str,
                         subplot_size: Tuple[float, float]=(6, 4)):
    """Plots running average of S, E, I, R populations at last timepoint from the given sim files. 
    Generates one for each metro in metros_to_plot.
    Args:
        sim_files: list of simulation output files
        metros_to_plot: list of metropolitan areas to generate plots for
        out_path: path to save figure
    """
    assert len(sim_files) > 0, 'no sim files specified'
    assert len(metros_to_plot) > 0, 'no metro area(s) specified'
    for filename in sim_files:
        assert os.path.isfile(filename), '{} not a valid sim file'.format(filename)
    # Fetch all data
    with multiprocessing.Pool(4) as p:
        data = p.map(utils.parse_simulation_log, sim_files)
    num_subplots = len(metros_to_plot)
    fig = plt.figure(figsize=(subplot_size[0], subplot_size[1]*num_subplots))
    for i, metro in enumerate(metros_to_plot):
        ax = fig.add_subplot(num_subplots, 1, i + 1)
        running_avg = _calculate_running_average(data, metro)
        for j in range(4):
            ax.plot(running_avg[:, j])
        ax.set_title('Running average population: {}'.format(metro))
        ax.set_xlabel('Num simulations')
        ax.set_ylabel('Population')
        ax.legend(['Susceptible', 'Exposed', 'Infected', 'Removed'])
    plt.savefig(out_path)

def generate_running_average_plot():
    files = ['sandbox/days240_seed{}.txt'.format(i) for i in range(100)]
    metros_to_plot = [
        'New York-Newark-Jersey City NY-NJ-PA MSA',
        'San Francisco-Oakland-Berkeley CA MSA',
        'San Jose-Sunnyvale-Santa Clara CA MSA',
        'Detroit-Warren-Dearborn MI MSA',
    ]
    running_average_plot(files, metros_to_plot, 'sandbox/240day_runningavg.png')

def main():
    generate_running_average_plot()

if __name__ == '__main__':
    main()