# -*- coding: utf-8 -*-
"""
Created on Wed May 21 11:54:20 2025

@author: evert
"""

import matplotlib.pyplot as plt

# Data: bar spans from x_start to x_end
container = ['con1', 'con2', 'con3']
depart = [2, 1, 4]
arrival = [5, 4, 7]
widths = [end - start for start, end in zip(depart, arrival)]

# Create horizontal bars with left=start and width=end-start
plt.barh(container, widths, left=depart, color='skyblue')

# Add labels
plt.xlabel("Time")
plt.title("Horizontal Bar Chart with Ranges")

plt.show()