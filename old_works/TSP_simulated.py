# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:22:46 2025

@author: evert
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# Parameters
num_cities = 10
T_start = 1000
T_min = 1
alpha = 0.995
random.seed(42)

cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]

# Step 2: Initial route
current_route = list(range(num_cities))
random.shuffle(current_route)
best_route = current_route[:]
T = T_start

def total_distance(route):
    dist = 0
    for i in range(len(route)):
        city_a = cities[route[i]]
        city_b = cities[route[(i + 1) % len(route)]]
        dist += np.linalg.norm(np.array(city_a) - np.array(city_b))
    return dist

distances = [total_distance(current_route)]

while T > T_min:
    # Generate a new candidate route by swapping two cities
    a, b = random.sample(range(len(current_route)), 2)
    new_route = current_route[:]
    new_route[a], new_route[b] = new_route[b], new_route[a]

    delta = total_distance(new_route) - total_distance(current_route)

    if delta < 0 or random.random() < np.exp(-delta / T):
        current_route = new_route
        if total_distance(current_route) < total_distance(best_route):
            best_route = current_route

    distances.append(total_distance(current_route))
    T *= alpha
    
# Step 4: Plot best route
route_cities = [cities[i] for i in best_route] + [cities[best_route[0]]]
xs, ys = zip(*route_cities)
plt.figure(figsize=(8, 6))
plt.plot(xs, ys, 'o-')
plt.title("Best Route Found")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()

# Step 5: Plot convergence
plt.figure(figsize=(8, 4))
plt.plot(distances)
plt.title("Convergence of Route Distance")
plt.xlabel("Iteration")
plt.ylabel("Distance")
plt.grid(True)
plt.show()    
    
    
    
    
    
    
    
    
    
    
    
    