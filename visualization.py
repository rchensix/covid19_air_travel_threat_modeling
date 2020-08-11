# Ruiqi Chen
# August 6, 2020
# This file contains various functions for visualizing our simulated data

import os
from typing import Dict, List, Tuple

import matplotlib.animation as animation
import matplotlib.image as mpimg
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

def bay_area_plots():
    filepath = 'sims/240_day_baseline_log.txt'
    data = utils.parse_simulation_log(filepath)
    fig = plt.figure(figsize=(16, 4))
    # Plot E, I, R for San Francisco / Oakland
    metro = 'San Francisco-Oakland-Berkeley CA MSA'
    e = np.array([event[3] for event in data[metro]])
    i = np.array([event[4] for event in data[metro]])
    r = np.array([event[5] for event in data[metro]])
    days = np.arange(e.shape[0]) / 2
    ax = fig.add_subplot(121)
    ax.semilogy(days, e, '-m')
    ax.semilogy(days, i, '-r')
    ax.semilogy(days, r, '-k')
    ax.set_xlabel('Days since January 1, 2020')
    ax.set_ylabel('Number of people')
    ax.legend(['Exposed', 'Infected', 'Removed'])
    ax.set_title(metro)
    # Plot E, I, R for San Jose
    metro = 'San Jose-Sunnyvale-Santa Clara CA MSA'
    e = np.array([event[3] for event in data[metro]])
    i = np.array([event[4] for event in data[metro]])
    r = np.array([event[5] for event in data[metro]])
    days = np.arange(e.shape[0]) / 2
    ax = fig.add_subplot(122)
    ax.semilogy(days, e, '-m')
    ax.semilogy(days, i, '-r')
    ax.semilogy(days, r, '-k')
    ax.set_xlabel('Days since January 1, 2020')
    ax.set_ylabel('Total cases')
    ax.legend(['Exposed', 'Infected', 'Removed'])
    ax.set_title(metro)
    plt.savefig('sims/bay_area_covid_baseline_sim.png')

def bay_area_scenarios():
    baseline_path = 'sims/240_day_baseline_log.txt'
    shelter_path = 'sims/240_day_shelter_log.txt'
    lockdown_path = 'sims/240_day_lockdown_log.txt'
    data_baseline = utils.parse_simulation_log(baseline_path)
    data_shelter = utils.parse_simulation_log(shelter_path)
    data_lockdown = utils.parse_simulation_log(lockdown_path)
    metro = 'San Francisco-Oakland-Berkeley CA MSA'
    total_baseline = np.array([event[3] + event[4] + event[5] for event in data_baseline[metro]])
    total_shelter = np.array([event[3] + event[4] + event[5] for event in data_shelter[metro]])
    total_lockdown = np.array([event[3] + event[4] + event[5] for event in data_lockdown[metro]])
    days = np.arange(total_baseline.shape[0]) / 2
    fig = plt.figure(figsize=(16, 4))
    ax = fig.add_subplot(121)
    ax.semilogy(days, total_lockdown, '-b')
    ax.semilogy(days, total_shelter, '-k')
    ax.semilogy(days, total_baseline, '-r')
    ax.set_xlabel('Days since January 1, 2020')
    ax.set_title(metro)
    ax.set_ylabel('Total cases')
    ax.legend(['Lockdown', 'Shelter-in-place', 'Freedom'])
    metro = 'San Jose-Sunnyvale-Santa Clara CA MSA'
    total_baseline = np.array([event[3] + event[4] + event[5] for event in data_baseline[metro]])
    total_shelter = np.array([event[3] + event[4] + event[5] for event in data_shelter[metro]])
    total_lockdown = np.array([event[3] + event[4] + event[5] for event in data_lockdown[metro]])
    days = np.arange(total_baseline.shape[0]) / 2
    ax = fig.add_subplot(122)
    ax.semilogy(days, total_lockdown, '-b')
    ax.semilogy(days, total_shelter, '-k')
    ax.semilogy(days, total_baseline, '-r')
    ax.set_xlabel('Days since January 1, 2020')
    ax.set_title(metro)
    ax.set_ylabel('Total cases')
    ax.legend(['Lockdown', 'Shelter-in-place', 'Freedom'])   
    plt.savefig('sims/bay_area_scenarios.png')

def beta_scenarios():
    beta_baseline = np.array([0.1, 0.1, 0.05, 0.02, 0.02, 0.1, 0.15, 0.15])
    beta_shelter = np.array([0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1])
    beta_lockdown = np.array([0.1, 0.1, 0.1, 0.02, 0.02, 0.02, 0.02, 0.02])
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
    fig = plt.figure(figsize=(24, 4))
    ax = fig.add_subplot(131)
    ax.bar(months, beta_lockdown)
    ax.set_ylabel('Transmission Rate')
    ax.set_title('Lockdown')
    ax = fig.add_subplot(132)
    ax.bar(months, beta_shelter)
    ax.set_ylabel('Transmission Rate')
    ax.set_title('Shelter-in-place')
    ax = fig.add_subplot(133)
    ax.bar(months, beta_baseline)
    ax.set_ylabel('Transmission Rate')
    ax.set_title('Freedom')
    plt.savefig('sims/bay_area_scenario_betas.png')

# Make this a list otherwise the order might get messed up
def _metro_coords():
    return {
        "New York-Newark-Jersey City NY-NJ-PA MSA": (1516, 336),
        "Los Angeles-Long Beach-Anaheim CA MSA": (189, 680),
        "Chicago-Naperville-Elgin IL-IN-WI MSA": (1116, 411),
        "Dallas-Fort Worth-Arlington TX MSA": (866, 794),
        "Houston-The Woodlands-Sugar Land TX MSA": (917, 908),
        "Washington-Arlington-Alexandria DC-VA-MD-WV MSA": (1430, 441),
        "Miami-Fort Lauderdale-Pompano Beach FL MSA": (1443, 971),
        "Philadelphia-Camden-Wilmington PA-NJ-DE-MD MSA": (1481, 390),
        "Atlanta-Sandy Springs-Alpharetta GA MSA": (1261, 696),
        "Phoenix-Mesa-Chandler AZ MSA": (378, 742),
        "Boston-Cambridge-Newton MA-NH MSA": (1562, 254),
        "San Francisco-Oakland-Berkeley CA MSA": (93, 492),
        "Riverside-San Bernardino-Ontario CA MSA": (227, 678),
        "Detroit-Warren-Dearborn MI MSA": (1240, 372),
        "Seattle-Tacoma-Bellevue WA MSA": (189, 138),
        "Minneapolis-St. Paul-Bloomington MN-WI MSA": (936, 312),
        "San Diego-Chula Vista-Carlsbad CA MSA": (208, 730),
        "Tampa-St. Petersburg-Clearwater FL MSA": (1353, 917),
        "Denver-Aurora-Lakewood CO MSA": (616, 520),
        "St. Louis MO-IL MSA": (1052, 538),
        "Baltimore-Columbia-Towson MD MSA": (1447, 420),
        "Charlotte-Concord-Gastonia NC-SC MSA": (1409, 702),
        "Orlando-Kissimmee-Sanford FL MSA": (1388, 879),
        "San Antonio-New Braunfels TX MSA": (809, 923),
        "Portland-Vancouver-Hillsboro OR-WA MSA": (154, 202),
        "Sacramento-Roseville-Folsom CA MSA": (122, 473),
        "Pittsburgh PA MSA": (1342, 411),
        "Las Vegas-Henderson-Paradise NV MSA": (304, 619),
        "Austin-Round Rock-Georgetown TX MSA": (842, 890),
        "Cincinnati OH-KY-IN MSA": (1224, 495),
        "Kansas City MO-KS MSA": (918, 540),
        "Columbus OH MSA": (1263, 452),
        "Indianapolis-Carmel-Anderson IN MSA": (1170, 481),
        "Cleveland-Elyria OH MSA": (1282, 387),
        "San Jose-Sunnyvale-Santa Clara CA MSA": (90, 511),
        "Nashville-Davidson-Murfreesboro-Franklin TN MSA": (1175, 621),
        "Virginia Beach-Norfolk-Newport News VA-NC MSA": (1486, 512),
        "Providence-Warwick RI-MA MSA": (1559, 281),
        "Milwaukee-Waukesha WI MSA": (1100, 372),
        "Jacksonville FL MSA": (1368, 810),
        "Oklahoma City OK MSA": (840, 686),
        "Raleigh-Cary NC MSA": (1423, 573),
        "Memphis TN-MS-AR MSA": (1078, 680),
        "Richmond VA MSA": (1444, 506),
        "New Orleans-Metairie LA MSA": (1097, 880),
        "Louisville/Jefferson County KY-IN MSA": (1192, 540),
        "Salt Lake City UT MSA": (415, 458),
        "Hartford-East Hartford-Middletown CT MSA": (1530, 291),
        "Buffalo-Cheektowaga NY MSA": (1349, 309),
        "Birmingham-Hoover AL MSA": (1181, 728),
        "Grand Rapids-Kentwood MI MSA": (1164, 350),
        "Rochester NY MSA": (1393, 285),
        "Tucson AZ MSA": (402, 786),
    }

def _animation_func(frame, scatter, ax):
    scatter.set_sizes(frame[1])
    ax.set_title('Day {}'.format(frame[0]))

def us_covid_animation():
    # Load background image
    background_img_path = 'data/united_states_map_with_metro_areas.jpg'
    background_img = mpimg.imread(background_img_path)
    metro_coords = _metro_coords()
    # DO NOT CHANGE FIGURE SIZE!
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    ax.imshow(background_img)
    x = np.array([metro_coords[metro][0] for metro in metro_coords.keys()])
    y = np.array([metro_coords[metro][1] for metro in metro_coords.keys()])
    s = np.ones_like(x)
    smax = 4000
    scatter = ax.scatter(x, y, s=s, c='#800080', alpha=0.5)
    sim_path = 'sims/240_day_baseline_log.txt'
    data = utils.parse_simulation_log(sim_path)
    pmax = 1695640  # E + I + R of NYC on day 240
    frames = list()
    num_half_days = len(data['Tucson AZ MSA'])
    for half_day in range(num_half_days):
        if half_day % 2 == 0: continue  # only plot half the data
        point_sizes = list()
        for metro in data.keys():
            snapshot = data[metro][half_day]
            pt_size = int(np.log(snapshot[3] + snapshot[4] + snapshot[5] + 1) / np.log(pmax)) * smax + 1
            point_sizes.append(pt_size)
        frames.append((half_day // 2, np.array(point_sizes)))
    ani = animation.FuncAnimation(fig, _animation_func, frames=frames, fargs=(scatter, ax),
                                  interval=100, blit=False)
    # plt.show()
    ani.save('sims/240_day_baseline_cases.gif', fps=30)

def main():
    # generate_running_average_plot()
    # bay_area_plots()
    # bay_area_scenarios()
    # beta_scenarios()
    us_covid_animation()

if __name__ == '__main__':
    main()