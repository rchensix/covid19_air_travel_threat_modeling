#%matplotlib notebook
# ^^^ This allows for the animations to be run in Jupyter

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


#print(marksize)


img = plt.imread('data/united_states_map_with_metro_areas.jpg')
fig, ax = plt.subplots()
#plt.figure(num=None, figsize=(5, 5), dpi=200, facecolor='w', edgecolor='k')
ax.imshow(img)


ims = []
imslist = []
for k in range(len(city_names)):
    imslist = []
    for i in range(day_len):
        imslist.append(plt.plot(locations[city_names[k]][0],locations[city_names[k]][1],marker="o", markersize = marksize[k][i], color = 'blue'))
    ims.append(imslist)

'''
This is just commented out using text because I didn't want to put an # on every line
#####################################################################################
ims0 = []
for i in range(day_len):
    ims0.append(ax.plot(locations[city_names[0]][0],locations[city_names[0]][1],marker="o", markersize = marksize[0][i], color = 'blue'))
    ims0.append(plt.plot(locations[city_names[1]][0],locations[city_names[1]][1],marker="o", markersize = marksize[1][i], color = 'blue'))

ims1 = []
for i in range(day_len):
    ims1.append(plt.plot(locations[city_names[1]][0],locations[city_names[1]][1],marker="o", markersize = marksize[1][i], color = 'blue'))

    ims2 = []
for i in range(day_len):
    ims2.append(plt.plot(locations[city_names[2]][0],locations[city_names[2]][1],marker="o", markersize = marksize[2][i], color = 'blue'))

ims3 = []
for i in range(day_len):
    ims3.append(plt.plot(locations[city_names[3]][0],locations[city_names[3]][1],marker="o", markersize = marksize[3][i], color = 'blue'))

ims4 = []
for i in range(day_len):
    ims4.append(plt.plot(locations[city_names[4]][0],locations[city_names[4]][1],marker="o", markersize = marksize[4][i], color = 'blue'))

ims5 = []
for i in range(day_len):
    ims5.append(plt.plot(locations[city_names[5]][0],locations[city_names[5]][1],marker="o", markersize = marksize[5][i], color = 'blue'))

ims6 = []
for i in range(day_len):
    ims6.append(plt.plot(locations[city_names[6]][0],locations[city_names[6]][1],marker="o", markersize = marksize[6][i], color = 'blue'))

ims7 = []
for i in range(day_len):
    ims7.append(plt.plot(locations[city_names[7]][0],locations[city_names[7]][1],marker="o", markersize = marksize[7][i], color = 'blue'))

ims8 = []
for i in range(day_len):
    ims8.append(plt.plot(locations[city_names[8]][0],locations[city_names[8]][1],marker="o", markersize = marksize[8][i], color = 'blue'))

ims9 = []
for i in range(day_len):
    ims9.append(plt.plot(locations[city_names[9]][0],locations[city_names[9]][1],marker="o", markersize = marksize[9][i], color = 'blue'))

ims10 = []
for i in range(day_len):
    ims10.append(plt.plot(locations[city_names[10]][0],locations[city_names[10]][1],marker="o", markersize = marksize[10][i], color = 'blue'))

ims11 = []
for i in range(day_len):
    ims11.append(plt.plot(locations[city_names[11]][0],locations[city_names[11]][1],marker="o", markersize = marksize[11][i], color = 'blue'))

ims12 = []
for i in range(day_len):
    ims12.append(plt.plot(locations[city_names[12]][0],locations[city_names[12]][1],marker="o", markersize = marksize[12][i], color = 'blue'))

ims13 = []
for i in range(day_len):
    ims13.append(plt.plot(locations[city_names[13]][0],locations[city_names[13]][1],marker="o", markersize = marksize[13][i], color = 'blue'))

ims14 = []
for i in range(day_len):
    ims14.append(plt.plot(locations[city_names[14]][0],locations[city_names[14]][1],marker="o", markersize = marksize[14][i], color = 'blue'))

ims15 = []
for i in range(day_len):
    ims15.append(plt.plot(locations[city_names[15]][0],locations[city_names[15]][1],marker="o", markersize = marksize[15][i], color = 'blue'))

ims16 = []
for i in range(day_len):
    ims16.append(plt.plot(locations[city_names[16]][0],locations[city_names[16]][1],marker="o", markersize = marksize[16][i], color = 'blue'))

ims17 = []
for i in range(day_len):
    ims17.append(plt.plot(locations[city_names[17]][0],locations[city_names[17]][1],marker="o", markersize = marksize[17][i], color = 'blue'))

ims18 = []
for i in range(day_len):
    ims18.append(plt.plot(locations[city_names[18]][0],locations[city_names[18]][1],marker="o", markersize = marksize[18][i], color = 'blue'))

ims19 = []
for i in range(day_len):
    ims19.append(plt.plot(locations[city_names[19]][0],locations[city_names[19]][1],marker="o", markersize = marksize[19][i], color = 'blue'))

ims20 = []
for i in range(day_len):
    ims20.append(plt.plot(locations[city_names[20]][0],locations[city_names[20]][1],marker="o", markersize = marksize[20][i], color = 'blue'))

ims21 = []
for i in range(day_len):
    ims21.append(plt.plot(locations[city_names[21]][0],locations[city_names[21]][1],marker="o", markersize = marksize[21][i], color = 'blue'))

ims22 = []
for i in range(day_len):
    ims22.append(plt.plot(locations[city_names[22]][0],locations[city_names[22]][1],marker="o", markersize = marksize[22][i], color = 'blue'))

ims23 = []
for i in range(day_len):
    ims23.append(plt.plot(locations[city_names[23]][0],locations[city_names[23]][1],marker="o", markersize = marksize[23][i], color = 'blue'))

ims24 = []
for i in range(day_len):
    ims24.append(plt.plot(locations[city_names[24]][0],locations[city_names[24]][1],marker="o", markersize = marksize[24][i], color = 'blue'))

ims25 = []
for i in range(day_len):
    ims25.append(plt.plot(locations[city_names[25]][0],locations[city_names[25]][1],marker="o", markersize = marksize[25][i], color = 'blue'))

ims26 = []
for i in range(day_len):
    ims26.append(plt.plot(locations[city_names[26]][0],locations[city_names[26]][1],marker="o", markersize = marksize[26][i], color = 'blue'))

ims27 = []
for i in range(day_len):
    ims27.append(plt.plot(locations[city_names[27]][0],locations[city_names[27]][1],marker="o", markersize = marksize[27][i], color = 'blue'))

ims28 = []
for i in range(day_len):
    ims28.append(plt.plot(locations[city_names[28]][0],locations[city_names[28]][1],marker="o", markersize = marksize[28][i], color = 'blue'))

ims29 = []
for i in range(day_len):
    ims29.append(plt.plot(locations[city_names[29]][0],locations[city_names[29]][1],marker="o", markersize = marksize[29][i], color = 'blue'))

ims30 = []
for i in range(day_len):
    ims30.append(plt.plot(locations[city_names[30]][0],locations[city_names[30]][1],marker="o", markersize = marksize[30][i], color = 'blue'))

ims31 = []
for i in range(day_len):
    ims31.append(plt.plot(locations[city_names[31]][0],locations[city_names[31]][1],marker="o", markersize = marksize[31][i], color = 'blue'))

ims32 = []
for i in range(day_len):
    ims32.append(plt.plot(locations[city_names[32]][0],locations[city_names[32]][1],marker="o", markersize = marksize[32][i], color = 'blue'))

ims33 = []
for i in range(day_len):
    ims33.append(plt.plot(locations[city_names[33]][0],locations[city_names[33]][1],marker="o", markersize = marksize[33][i], color = 'blue'))

ims34 = []
for i in range(day_len):
    ims34.append(plt.plot(locations[city_names[34]][0],locations[city_names[34]][1],marker="o", markersize = marksize[34][i], color = 'blue'))

ims35 = []
for i in range(day_len):
    ims35.append(plt.plot(locations[city_names[35]][0],locations[city_names[35]][1],marker="o", markersize = marksize[35][i], color = 'blue'))

ims36 = []
for i in range(day_len):
    ims36.append(plt.plot(locations[city_names[36]][0],locations[city_names[36]][1],marker="o", markersize = marksize[36][i], color = 'blue'))

ims37 = []
for i in range(day_len):
    ims37.append(plt.plot(locations[city_names[37]][0],locations[city_names[37]][1],marker="o", markersize = marksize[37][i], color = 'blue'))

ims38 = []
for i in range(day_len):
    ims38.append(plt.plot(locations[city_names[38]][0],locations[city_names[38]][1],marker="o", markersize = marksize[38][i], color = 'blue'))

ims39 = []
for i in range(day_len):
    ims39.append(plt.plot(locations[city_names[39]][0],locations[city_names[39]][1],marker="o", markersize = marksize[39][i], color = 'blue'))

ims40 = []
for i in range(day_len):
    ims40.append(plt.plot(locations[city_names[40]][0],locations[city_names[40]][1],marker="o", markersize = marksize[40][i], color = 'blue'))

ims41 = []
for i in range(day_len):
    ims41.append(plt.plot(locations[city_names[41]][0],locations[city_names[41]][1],marker="o", markersize = marksize[41][i], color = 'blue'))

ims42 = []
for i in range(day_len):
    ims42.append(plt.plot(locations[city_names[42]][0],locations[city_names[42]][1],marker="o", markersize = marksize[42][i], color = 'blue'))

ims43 = []
for i in range(day_len):
    ims43.append(plt.plot(locations[city_names[43]][0],locations[city_names[43]][1],marker="o", markersize = marksize[43][i], color = 'blue'))

ims44 = []
for i in range(day_len):
    ims44.append(plt.plot(locations[city_names[44]][0],locations[city_names[44]][1],marker="o", markersize = marksize[44][i], color = 'blue'))

ims45 = []
for i in range(day_len):
    ims45.append(plt.plot(locations[city_names[45]][0],locations[city_names[45]][1],marker="o", markersize = marksize[45][i], color = 'blue'))

ims46 = []
for i in range(day_len):
    ims46.append(plt.plot(locations[city_names[46]][0],locations[city_names[46]][1],marker="o", markersize = marksize[46][i], color = 'blue'))

ims47 = []
for i in range(day_len):
    ims47.append(plt.plot(locations[city_names[47]][0],locations[city_names[47]][1],marker="o", markersize = marksize[47][i], color = 'blue'))

ims48 = []
for i in range(day_len):
    ims48.append(plt.plot(locations[city_names[48]][0],locations[city_names[48]][1],marker="o", markersize = marksize[48][i], color = 'blue'))

ims49 = []
for i in range(day_len):
    ims49.append(plt.plot(locations[city_names[49]][0],locations[city_names[49]][1],marker="o", markersize = marksize[49][i], color = 'blue'))

ims50 = []
for i in range(day_len):
    ims50.append(plt.plot(locations[city_names[50]][0],locations[city_names[50]][1],marker="o", markersize = marksize[50][i], color = 'blue'))

ims51 = []
for i in range(day_len):
    ims51.append(plt.plot(locations[city_names[51]][0],locations[city_names[51]][1],marker="o", markersize = marksize[51][i], color = 'blue'))

ims52 = []
for i in range(day_len):
    ims52.append(plt.plot(locations[city_names[52]][0],locations[city_names[52]][1],marker="o", markersize = marksize[52][i], color = 'blue'))
'''
#This all but works with the loops I created above but it creates what I think to be a still image but not entirely sure,
# if you can figure out if its a animation or image and then save it that would save the day
im_ani0 = animation.ArtistAnimation(fig, ims, interval=20, repeat_delay=300, blit=True)

'''
#im_ani1 = animation.ArtistAnimation(fig, ims1, interval=20, repeat_delay=300, blit=True)
#im_ani2 = animation.ArtistAnimation(fig, ims2, interval=20, repeat_delay=300, blit=True)
#im_ani3 = animation.ArtistAnimation(fig, ims3, interval=20, repeat_delay=300, blit=True)
#im_ani4 = animation.ArtistAnimation(fig, ims4, interval=20, repeat_delay=300, blit=True)
#im_ani5 = animation.ArtistAnimation(fig, ims5, interval=20, repeat_delay=300, blit=True)
#im_ani6 = animation.ArtistAnimation(fig, ims6, interval=20, repeat_delay=300, blit=True)
#im_ani7 = animation.ArtistAnimation(fig, ims7, interval=20, repeat_delay=300, blit=True)
#im_ani8 = animation.ArtistAnimation(fig, ims8, interval=20, repeat_delay=300, blit=True)
im_ani9 = animation.ArtistAnimation(fig, ims9, interval=20, repeat_delay=300, blit=True)
im_ani10 = animation.ArtistAnimation(fig, ims10, interval=20, repeat_delay=300, blit=True)

im_ani11 = animation.ArtistAnimation(fig, ims11, interval=20, repeat_delay=300, blit=True)
im_ani12 = animation.ArtistAnimation(fig, ims12, interval=20, repeat_delay=300, blit=True)
im_ani13 = animation.ArtistAnimation(fig, ims13, interval=20, repeat_delay=300, blit=True)
im_ani14 = animation.ArtistAnimation(fig, ims14, interval=20, repeat_delay=300, blit=True)
im_ani15 = animation.ArtistAnimation(fig, ims15, interval=20, repeat_delay=300, blit=True)
im_ani16 = animation.ArtistAnimation(fig, ims16, interval=20, repeat_delay=300, blit=True)
im_ani17 = animation.ArtistAnimation(fig, ims17, interval=20, repeat_delay=300, blit=True)
im_ani18 = animation.ArtistAnimation(fig, ims18, interval=20, repeat_delay=300, blit=True)
im_ani19 = animation.ArtistAnimation(fig, ims19, interval=20, repeat_delay=300, blit=True)
im_ani20 = animation.ArtistAnimation(fig, ims20, interval=20, repeat_delay=300, blit=True)

im_ani21 = animation.ArtistAnimation(fig, ims21, interval=20, repeat_delay=300, blit=True)
im_ani22 = animation.ArtistAnimation(fig, ims22, interval=20, repeat_delay=300, blit=True)
im_ani23 = animation.ArtistAnimation(fig, ims23, interval=20, repeat_delay=300, blit=True)
im_ani24 = animation.ArtistAnimation(fig, ims24, interval=20, repeat_delay=300, blit=True)
im_ani25 = animation.ArtistAnimation(fig, ims25, interval=20, repeat_delay=300, blit=True)
im_ani26 = animation.ArtistAnimation(fig, ims26, interval=20, repeat_delay=300, blit=True)
im_ani27 = animation.ArtistAnimation(fig, ims27, interval=20, repeat_delay=300, blit=True)
im_ani28 = animation.ArtistAnimation(fig, ims28, interval=20, repeat_delay=300, blit=True)
im_ani29 = animation.ArtistAnimation(fig, ims29, interval=20, repeat_delay=300, blit=True)
im_ani30 = animation.ArtistAnimation(fig, ims30, interval=20, repeat_delay=300, blit=True)

im_ani31 = animation.ArtistAnimation(fig, ims31, interval=20, repeat_delay=300, blit=True)
im_ani32 = animation.ArtistAnimation(fig, ims32, interval=20, repeat_delay=300, blit=True)
im_ani33 = animation.ArtistAnimation(fig, ims33, interval=20, repeat_delay=300, blit=True)
im_ani34 = animation.ArtistAnimation(fig, ims34, interval=20, repeat_delay=300, blit=True)
im_ani35 = animation.ArtistAnimation(fig, ims35, interval=20, repeat_delay=300, blit=True)
im_ani36 = animation.ArtistAnimation(fig, ims36, interval=20, repeat_delay=300, blit=True)
im_ani37 = animation.ArtistAnimation(fig, ims37, interval=20, repeat_delay=300, blit=True)
im_ani38 = animation.ArtistAnimation(fig, ims38, interval=20, repeat_delay=300, blit=True)
im_ani39 = animation.ArtistAnimation(fig, ims39, interval=20, repeat_delay=300, blit=True)
im_ani40 = animation.ArtistAnimation(fig, ims40, interval=20, repeat_delay=300, blit=True)

im_ani41 = animation.ArtistAnimation(fig, ims41, interval=20, repeat_delay=300, blit=True)
im_ani42 = animation.ArtistAnimation(fig, ims42, interval=20, repeat_delay=300, blit=True)
im_ani43 = animation.ArtistAnimation(fig, ims43, interval=20, repeat_delay=300, blit=True)
im_ani44 = animation.ArtistAnimation(fig, ims44, interval=20, repeat_delay=300, blit=True)
im_ani45 = animation.ArtistAnimation(fig, ims45, interval=20, repeat_delay=300, blit=True)
im_ani46 = animation.ArtistAnimation(fig, ims46, interval=20, repeat_delay=300, blit=True)
im_ani47 = animation.ArtistAnimation(fig, ims47, interval=20, repeat_delay=300, blit=True)
im_ani48 = animation.ArtistAnimation(fig, ims48, interval=20, repeat_delay=300, blit=True)
im_ani49 = animation.ArtistAnimation(fig, ims49, interval=20, repeat_delay=300, blit=True)
im_ani50 = animation.ArtistAnimation(fig, ims50, interval=20, repeat_delay=300, blit=True)

im_ani51 = animation.ArtistAnimation(fig, ims51, interval=20, repeat_delay=300, blit=True)
im_ani52 = animation.ArtistAnimation(fig, ims52, interval=20, repeat_delay=300, blit=True)
'''


#plt.show()


#im_ani0.save('test2.gif', writer=animation.PillowWriter(fps=24))
#im_ani1.save('test2.gif', writer=animation.PillowWriter(fps=24))
#################################################################################################
