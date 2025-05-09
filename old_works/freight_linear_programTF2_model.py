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

# Create villages
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
    'Village11': (94, 71),
    'Village12': (16, 47),
    'Village13': (86, 23),
    'Village14': (77, 43),
    'Village15': (93, 8),
    'Village16': (64, 100),
    'Village17': (97, 11),
    'Village18': (80, 66)
}

# Create factories
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


# Plotting the nodes
plt.figure(figsize=(8, 8))
for name, (x, y) in V.items():
    plt.plot(x, y, 'bo')  # 'bo' means blue circle
    plt.text(x + 1, y + 1, name, fontsize=9)  # Label each point slightly offset
for name, (x, y) in F.items():
    plt.plot(x, y, 'r+')  # 'bo' means blue circle
    plt.text(x + 1, y + 1, name, fontsize=9)  # Label each point slightly offset

plt.title('Villages and Factories')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.axis('equal')
plt.show()









