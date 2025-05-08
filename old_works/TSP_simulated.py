# -*- coding: utf-8 -*-
"""
Created on Thu May  8 14:22:46 2025

@author: evert
"""


import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random

# Parameters
num_cities = 10
T_start = 1000
T_min = 1
alpha = 0.995
random.seed(42)

cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]

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

# Store routes for animation
route_history = [current_route[:]]
distances = [total_distance(current_route)]

# Initialize distance for current route
current_dist = total_distance(current_route)
best_dist = current_dist

while T > T_min:
    a, b = random.sample(range(len(current_route)), 2)
    new_route = current_route[:]
    new_route[a], new_route[b] = new_route[b], new_route[a]

    # Calculate new route distance incrementally
    delta = total_distance(new_route) - current_dist

    if delta < 0 or random.random() < np.exp(-delta / T):
        current_route = new_route
        current_dist = total_distance(current_route)

        if current_dist < best_dist:
            best_route = current_route
            best_dist = current_dist

    route_history.append(current_route[:])
    distances.append(current_dist)
    T *= alpha

# Animate route evolution
fig, ax = plt.subplots(figsize=(8, 6))
line, = ax.plot([], [], 'o-', lw=2)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title("Simulated Annealing TSP Route")

# Add city markers for clarity
ax.scatter(*zip(*cities), color='red', zorder=5)

def update(frame):
    # Ensure that the route loops back to the start city to complete the cycle
    route = route_history[frame] + [route_history[frame][0]]
    xs, ys = zip(*[cities[i] for i in route])
    line.set_data(xs, ys)
    ax.set_title(f"Iteration {frame}, Distance: {distances[frame]:.2f}")
    return line,  # Return the line object as a tuple for proper animation update

ani = animation.FuncAnimation(fig, update, frames=len(route_history), interval=50, blit=True)
plt.show()

ani.save("tsp_animation.gif", writer="pillow", fps=20)

    
    
    
    
    
    
    
    
    
    
    