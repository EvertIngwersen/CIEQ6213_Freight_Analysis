# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:49:32 2025

@author: evert
"""

import random
import numpy
import matplotlib.pyplot as plt

random.seed(77)

# Create random nodes
V = {f'Node{i}': (random.randint(0, 100), random.randint(0, 100)) for i in range(1, 21)}

# Let's say 5 nodes are hubs
hub_keys = random.sample(list(V.keys()), 5)
V_h = {k: V[k] for k in hub_keys}
V_d = {k: V[k] for k in V if k not in hub_keys}

# Create scatter plot
plt.figure(figsize=(8, 6))

# Plot hub nodes (e.g., red squares)
x_h = [coord[0] for coord in V_h.values()]
y_h = [coord[1] for coord in V_h.values()]
plt.scatter(x_h, y_h, color='red', marker='s', label='Hub Nodes')

# Plot demand nodes (e.g., blue circles)
x_d = [coord[0] for coord in V_d.values()]
y_d = [coord[1] for coord in V_d.values()]
plt.scatter(x_d, y_d, color='blue', marker='o', label='Demand Nodes')

# Add labels to each point
for k, (x, y) in V.items():
    plt.text(x + 1, y + 1, k, fontsize=9)

# Add legend, grid, and labels
plt.legend()
plt.grid(True)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot of Hub and Demand Nodes')
plt.show()











