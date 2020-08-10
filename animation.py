
import os
import json
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import numpy as np
import PIL

import utils


############################################
# Compliation of info from 240 day data log into nested dictionary with all info for cities,months,days,sus,exp,inf,rec
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
                city_counter = 1
            if tot_counter >= file_len:
                break

#print(map_data)
##################################################################
# Connecting city locations on United States map, serveying how many potential covid cases and plotting points to an animation
# as necessary
city_names = list(map_data.keys())
city_pts = [[1510,334],[190,685],[1116,410],[864,791],[914,901],[1429,456],[1439,474],[1476,390],[1258,696],[378,744],[1260,257],[85,490],[203,677],[1239,369],[186,141],[925,307],[205,729],[1357,909],[617,522],[1049,539],[1450,425],[1362,621],[139,879],[808,920],[156,205],[123,475],[1340,404],[300,614],[843,894],[1220,496],[916,539],[1261,451],[1172,487],[1282,385],[85,513],[1174,619],[1487,515],[1562,281],[1560,287],[199,371],[1364,813],[841,690],[1422,576],[1073,679],[1444,511],[1095,884],[1192,537],[414,455],[1530,296],[1349,311],[1179,731],[1161,354],[1364,306]]
locations = dict()

for i in range(len(city_pts)):
    locations[city_names[i]] = city_pts[i]


day_len = len(map_data[city_names[0]]['day'])

j = 1
ms = 1
#marksize = [[0] * day_len] * len(city_names)
marksize = []
for k in range(len(city_names)):
    j = 1
    ms = 1
    mslist = []
    for i in range(day_len):
        mark = map_data[city_names[k]]['expose'][i] + map_data[city_names[k]]['infect'][i] + map_data[city_names[k]]['recover'][i]
        if mark > 5*j:
            ms += 2
            j += 1
        mslist.append(ms)
    marksize.append(mslist)
    #marksize[0][i] = ms

#print(marksize)


#img = mpimg.imread('data/united_states_map_with_metro_areas.jpg')
#plt.figure(num=None, figsize=(5, 5), dpi=200, facecolor='w', edgecolor='k')
#imgplot = plt.imshow(img)

map = PIL.Image.open('data/united_states_map_with_metro_areas.jpg')
width, height = map.size
fig2 = plt.figure(figsize = (7,6))


ims = []
imslist = []
for k in range(len(city_names)):
    imslist = []
    for i in range(day_len):
        imslist.append(plt.plot(locations[city_names[k]][0],locations[city_names[k]][1],marker="o", markersize = marksize[k][i], color = 'blue'))
    ims.append(imslist)

ims_test = []
for i in range(day_len):
    ims_test.append(plt.plot(locations[city_names[0]][0],locations[city_names[0]][1],marker="o", markersize = marksize[0][i], color = 'blue'))

#for i in range(day_len):
#    ims2.append(plt.plot(locations[city_names[0]][0],locations[city_names[0]][1],marker="o", markersize = marksize[0][i], color = 'blue'))


#im_ani = animation.ArtistAnimation(fig2, ims[0], interval=20, repeat_delay=300, blit=True)
#im_ani = animation.ArtistAnimation(fig2, ims, interval=20, repeat_delay=300, blit=True)
#im_ani2 = animation.ArtistAnimation(fig2, ims2, interval=20, repeat_delay=300, blit=True)


#plt.show()


#im_ani.save('test.gif', writer=animation.PillowWriter(fps=24))
#################################################################################################
#Failed Animation attempts

#map = PIL.Image.open('data/united_states_map_with_metro_areas.jpg')
#width, height = map.size

#plt.figure(num=None, figsize=(5, 5), dpi=200, facecolor='w', edgecolor='k')
#fig, ax = plt.subplots()
#ax.axis([0,width,height,0])
#l, = plt.plot([],[])


#def animate(i):
#    plt.plot(city_pts[0][0],city_pts[0][1],marker="o", markersize = marksize[:i])

#ani = animation.FuncAnimation(fig, animate, frames=len(marksize))

#for i in range(len(locations)):
#    plt.plot(locations[city_names[i]][0],locations[city_names[i]][1],marker="o", markersize = 1, color = 'blue')


#from IPython.display import HTML
#HTML(ani.to_jshtml())
