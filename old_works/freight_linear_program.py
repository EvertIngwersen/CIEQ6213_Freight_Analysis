# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:49:32 2025

@author: evert
"""

import random
import numpy
import math
import itertools
import matplotlib.pyplot as plt

random.seed(777)

# Create nodes
V = {
    'Node1': (17, 34),
    'Node2': (94, 48),
    'Node3': (75, 2),
    'Node4': (15, 18),
    'Node5': (9, 39),
    'Node6': (33, 82),
    'Node7': (44, 96),
    'Node8': (96, 82),
    'Node9': (6, 15),
    'Node10': (36, 5),
    'Node11': (94, 71),
    'Node12': (16, 47),
    'Node13': (86, 23),
    'Node14': (77, 43),
    'Node15': (93, 8),
    'Node16': (64, 100),
    'Node17': (97, 11),
    'Node18': (80, 66),
    'Node19': (45, 36),
    'Node20': (19, 17)
}

# Assume V already exists from earlier code
nodes = list(V.keys())


# Service Type T

T = ["High Speed", "Normal Rail"]

# Create W: demand between random pairs of nodes
W = {}

random.seed(777) # Keep consistent randomness

# Select 30 random (i,j) pairs without replacement and i ≠ j
pairs = set()
while len(pairs) < 30:
    i, j = random.sample(nodes, 2)
    if (i, j) not in pairs:
        pairs.add((i, j))

# Assign random demand values (e.g., 10 to 100) to each pair
for (i, j) in pairs:
    W[(i, j)] = random.randint(10, 100)

# Create C_n: node cost dictionary
C_i = {}

for node in V:
    C_i[node] = random.randint(50, 500)
    
    
# Create distance dictionary D 
D = {}    
    
for i in V:
    for j in V:
        if i != j:
            x1, y1 = V[i]
            x2, y2 = V[j]
            distance = math.hypot(x2 - x1, y2 - y1)  # Euclidean distance
            D[(i, j)] = distance    

Q_i = {}

for node in V:
    Q_i[node] = random.randint(50, 200)
    
# Plotting the nodes
plt.figure(figsize=(8, 8))
for name, (x, y) in V.items():
    plt.plot(x, y, 'bo')  # 'bo' means blue circle
    plt.text(x + 1, y + 1, name, fontsize=9)  # Label each point slightly offset

plt.title('Randomly Generated Nodes')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.axis('equal')
plt.show()
        





