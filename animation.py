import os
import json
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import numpy as np
#import imp

import utils

month = []
day = []
susceptible = []
expose = []
infect = []
recover = []
city_data = dict()

map_data = dict()

test_log = 'data/test_240_day_log.txt'
assert os.path.isfile(test_log), '{} is not valid file'.format(test_log)
file_len = len(open(test_log).readlines())
with open(test_log) as f:
    city_counter = 0
    tot_counter = 0
    for line in f:
        city_counter += 1

        if 'MSA' in line:
            line = line[0:len(line)-1]
            map_data[line] = city_data

        elif 'susceptible' in line: continue

        else:
            split_line = line.split(sep=',')
            month.append(split_line[0])
            day.append(int(split_line[1]))
            susceptible.append(int(split_line[2]))
            expose.append(int(split_line[3]))
            infect.append(int(split_line[4]))
            recover.append(int(split_line[5]))

            if city_counter > 482:
                city_data['month'] = month
                city_data['day'] = day
                city_data['susceptible'] = susceptible
                city_data['expose'] = expose
                city_data['infect'] = infect
                city_data['recover'] = recover

                month = []
                day = []
                susceptible = []
                expose = []
                infect = []
                recover = []
                city_data = dict()

                tot_counter += city_counter
                city_counter = 0
            if tot_counter >= file_len:
                break

#print(map_data)
##################################################################
#print(map_data.keys()) #lists out all the map_data dictionary keys
#list(map_data)[1] #lists out individual map_data dictionary keys

#dict = {New York: [1700-x,1100-y], Los Angeles: [x,y]...}

#city_names = list(map_data.keys())

img = mpimg.imread('data/united_states_map_with_metro_areas.jpg')
plt.figure(num=None, figsize=(15, 13), dpi=200, facecolor='w', edgecolor='k')
plt.plot(190,685,marker="o")
imgplot = plt.imshow(img)

#city_pts = [[190,680],[..,..]...]

#locations = dict()
#for i in len(city_pts):
#    locations[city_names[i]] = city_pts[i]
