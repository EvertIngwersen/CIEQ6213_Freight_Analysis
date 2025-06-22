# -*- coding: utf-8 -*-
"""
Created on Fri May  9 12:15:25 2025

@author: evert
"""

import random
import numpy
import math
import itertools
import matplotlib.pyplot as plt

random.seed(777)

# Create villages (i is indice of village)
V = {
    'Village1': (17, 34),
    'Village2': (94, 48),
    'Village3': (75, 2),
    'Village4': (15, 18),
    'Village5': (9, 39),
    'Village6': (33, 82),
    'Village7': (44, 96),
    'Village8': (96, 82),
    'Village9': (6, 15),
    'Village10': (36, 5),
    'Village11': (55, 51),
    'Village12': (16, 47),
    'Village13': (86, 23),
    'Village14': (77, 12),
    'Village15': (92, 8),
    'Village16': (64, 100),
    'Village17': (97, 11),
    'Village18': (80, 66)
}

# Create factories (j is indice of factory)
F = {
    'Factory1': (67, 42),
    'Factory2': (12, 41),
    'Factory3': (74, 5),
    'Factory4': (12, 58),
    'Factory5': (91, 19),
    'Factory6': (13, 21),
    'Factory7': (48, 6),
    'Factory8': (36, 55),
    'Factory9': (61, 12),
    'Factory10': (3, 5),
    'Factory11': (34, 79),
    'Factory12': (1, 55),
    'Factory13': (80, 12),
    'Factory14': (77, 89)
}

# Create commodity types (k is commodity)
P = ["Steel", "Oil", "Coal"]

# Set of transport types (indice t is transport link)
T = ["Rail", "Road"] 

# Creating Param

# Demand for commodity k for village i
d_ij = {
    'Village1': (5, 83, 1),
    'Village2': (6, 2, 0),
    'Village3': (0, 0, 46),
    'Village4': (8, 12, 7),
    'Village5': (11, 41, 4),
    'Village6': (19, 75, 2),
    'Village7': (37, 89, 6),
    'Village8': (0, 67, 5),
    'Village9': (13, 9, 3),
    'Village10': (25, 15, 0),
    'Village11': (55, 0, 12),
    'Village12': (14, 39, 8),
    'Village13': (78, 22, 9),
    'Village14': (66, 40, 10),
    'Village15': (0, 6, 2),
    'Village16': (60, 99, 4),
    'Village17': (92, 10, 1),
    'Village18': (75, 0, 7)
}

# Production of commodity k in factory j
p_jk = {
    'Factory1': (0, 0, 20),
    'Factory2': (0, 41, 0),
    'Factory3': (0, 0, 50),
    'Factory4': (0, 0, 15),
    'Factory5': (0, 0, 40),
    'Factory6': (90, 0, 0),
    'Factory7': (0, 46, 0),
    'Factory8': (0, 0, 80),
    'Factory9': (0, 70, 0),
    'Factory10': (40, 0, 0),
    'Factory11': (0, 0, 27),
    'Factory12': (0, 55, 0),
    'Factory13': (0, 12, 0),
    'Factory14': (77, 0, 0)
}


# Distance from factory j to village i: e_ji[j][i] = distance [km]
e_ji = {}

for j, (xj, yj) in F.items():
    e_ji[j] = {}
    for i, (xi, yi) in V.items():
        dist = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
        e_ji[j][i] = dist

# Cost of tranpsort type per km
c_t = {"Rail": 40,
       "Road": 5}


# Mapping from commodity index to color
commodity_colors = {
    0: 'green',   # Steel
    1: 'black',   # Oil
    2: 'orange'   # Coal
}

plt.figure(figsize=(10, 10))

# Plot villages with demand info
for name, (x, y) in V.items():
    plt.plot(x, y, 'bo')  # blue circle for villages
    demand = d_ij.get(name, (0, 0, 0))
    plt.text(x + 1, y + 1, f"{name}\n{demand}", fontsize=8)

# Plot factories with commodity color and size by amount
for name, (x, y) in F.items():
    production = p_jk[name]
    for k in range(len(production)):
        if production[k] > 0:
            color = commodity_colors[k]
            size = production[k] * 3  # Scale factor for size
            plt.scatter(x, y, s=size, c=color, marker='+', linewidths=2)
            plt.text(x + 1, y + 1, f"{name}\n{P[k]}: {production[k]}", fontsize=8)
            break  # Only one commodity per factory

# Legend for commodity types
for k, color in commodity_colors.items():
    plt.scatter([], [], c=color, marker='+', s=100, label=P[k])

plt.legend(title='Factory Commodity')
plt.title('Villages and Factories with Demand and Production')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.axis('equal')
plt.tight_layout()
plt.show()


