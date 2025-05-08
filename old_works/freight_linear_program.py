# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:49:32 2025

@author: evert
"""

import random
import numpy
import matplotlib.pyplot as plt

random.seed(777)

# Create random nodes
V = {f'Node{i}': (random.randint(0, 100), random.randint(0, 100)) for i in range(1, 21)}

# Let's say 5 nodes are hubs
hub_keys = random.sample(list(V.keys()), 5)
V_h = {k: V[k] for k in hub_keys}
V_d = {k: V[k] for k in V if k not in hub_keys}

# Create edge dictionary: each demand node connected to one random hub
E = {}
for d_node in V_d:
    chosen_hub = random.choice(list(V_h.keys()))
    E[(d_node, chosen_hub)] = (V_d[d_node], V_h[chosen_hub]) 

# Create scatter plot
plt.figure(figsize=(10, 10))

# Plot hub nodes (red squares)
x_h = [coord[0] for coord in V_h.values()]
y_h = [coord[1] for coord in V_h.values()]
plt.scatter(x_h, y_h, color='red', marker='s', label='Hub Nodes')

# Plot demand nodes (blue circles)
x_d = [coord[0] for coord in V_d.values()]
y_d = [coord[1] for coord in V_d.values()]
plt.scatter(x_d, y_d, color='blue', marker='o', label='Demand Nodes')

# Plot edges
for (d_node, h_node), (d_coord, h_coord) in E.items():
    plt.plot([d_coord[0], h_coord[0]], [d_coord[1], h_coord[1]], color='gray', linestyle='--', linewidth=1)

# Add labels to each node
for k, (x, y) in V.items():
    plt.text(x + 1, y + 1, k, fontsize=9)

# Add legend, grid, and labels
plt.legend()
plt.grid(True)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Scatter Plot of Hub and Demand Nodes with Edges')
plt.show()


# Create random demand values between selected pairs of demand nodes
W = {}
demand_range = (1, 10)  # Example demand range, adjust as needed

# Generate all pairs of demand nodes (combinations)
demand_nodes = list(V_d.keys())

# Randomly select a subset of pairs (e.g., 50% of possible pairs)
pairs_to_create_demand = random.sample(
    [(demand_nodes[i], demand_nodes[j]) for i in range(len(demand_nodes)) for j in range(i + 1, len(demand_nodes))],
    k=int(len(demand_nodes) * (len(demand_nodes) - 1) / 2 * 0.5)  # Adjust 0.5 for how many pairs to generate demand
)

# Assign random demand to the selected pairs
for pair in pairs_to_create_demand:
    demand_value = random.randint(demand_range[0], demand_range[1])
    W[pair] = demand_value
        











