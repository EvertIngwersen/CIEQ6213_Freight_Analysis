# -*- coding: utf-8 -*-
"""
Created on Tue May 20 14:09:03 2025

@author: evert
"""

import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

delay_factor = 1
sys.exit()
containers = [
    {"name": "Container1", "weight": 25, "due": 12, "release": 3, "delay_penalty": 30},
    {"name": "Container2", "weight": 12, "due": 8,  "release": 0, "delay_penalty": 20},
    {"name": "Container3", "weight": 44, "due": 4,  "release": 0, "delay_penalty": 50},
    {"name": "Container4", "weight": 3,  "due": 22, "release": 2, "delay_penalty": 10},
    {"name": "Container5", "weight": 22, "due": 21, "release": 5, "delay_penalty": 0},
    {"name": "Container6", "weight": 10, "due": 21, "release": 6, "delay_penalty": 10},
    {"name": "Container7", "weight": 55, "due": 18, "release": 9, "delay_penalty": 10},
    {"name": "Container8", "weight": 76, "due": 17, "release": 10, "delay_penalty": 50},
    {"name": "Container9", "weight": 42, "due": 30, "release": 26, "delay_penalty": 90},
    {"name": "Container10","weight": 19, "due": 12, "release": 1, "delay_penalty": 30},
    {"name": "Container11","weight": 36, "due": 5,  "release": 1, "delay_penalty": 10},
    {"name": "Container12","weight": 7,  "due": 17, "release": 1, "delay_penalty": 10},
    {"name": "Container13","weight": 12, "due": 27, "release": 21, "delay_penalty": 60},
    {"name": "Container14","weight": 63, "due": 19, "release": 13, "delay_penalty": 60},
    {"name": "Container15","weight": 45, "due": 23, "release": 10, "delay_penalty": 40},
    {"name": "Container16","weight": 76, "due": 17, "release": 0, "delay_penalty": 80},
    {"name": "Container17","weight": 85, "due": 5,  "release": 3, "delay_penalty": 60},
    {"name": "Container18","weight": 23, "due": 22, "release": 11, "delay_penalty": 0},
    {"name": "Container19","weight": 12, "due": 16, "release": 10, "delay_penalty": 20},
    {"name": "Container20","weight": 3,  "due": 15, "release": 1, "delay_penalty": 60},
    {"name": "Container21","weight": 41, "due": 22, "release": 1, "delay_penalty": 10},
    {"name": "Container22","weight": 77, "due": 30, "release": 1, "delay_penalty": 80},
    {"name": "Container23","weight": 15, "due": 5,  "release": 0, "delay_penalty": 60},
    {"name": "Container24","weight": 67, "due": 8,  "release": 0, "delay_penalty": 10},
    {"name": "Container25","weight": 50, "due": 14, "release": 4, "delay_penalty": 45},
    {"name": "Container26","weight": 38, "due": 20, "release": 12, "delay_penalty": 35},
    {"name": "Container27","weight": 29, "due": 18, "release": 9, "delay_penalty": 25},
    {"name": "Container28","weight": 17, "due": 25, "release": 15, "delay_penalty": 15},
    {"name": "Container29","weight": 33, "due": 28, "release": 22, "delay_penalty": 50},
    {"name": "Container30","weight": 70, "due": 16, "release": 3, "delay_penalty": 65},
    {"name": "Container31","weight": 28, "due": 13, "release": 7, "delay_penalty": 25},
    {"name": "Container32","weight": 60, "due": 19, "release": 5, "delay_penalty": 70},
    {"name": "Container33","weight": 18, "due": 21, "release": 16, "delay_penalty": 15},
    {"name": "Container34","weight": 40, "due": 24, "release": 20, "delay_penalty": 40},
    {"name": "Container35","weight": 55, "due": 14, "release": 8, "delay_penalty": 55},
    {"name": "Container36","weight": 13, "due": 27, "release": 23, "delay_penalty": 10}
]

vehicles = [
    {"name": "Truck1", "cost": 90, "capacity": 38, "transit_time": 5},
    {"name": "Truck2", "cost": 135, "capacity": 35, "transit_time": 4},
    {"name": "Truck3", "cost": 110, "capacity": 40, "transit_time": 8},
    {"name": "Truck4", "cost": 90, "capacity": 35, "transit_time": 6},
    {"name": "Truck5", "cost": 90, "capacity": 35, "transit_time": 6},
    {"name": "Truck6", "cost": 140, "capacity": 65, "transit_time": 8},
    {"name": "Plane1", "cost": 550, "capacity": 75, "transit_time": 2},
    {"name": "Plane2", "cost": 750, "capacity": 100, "transit_time": 1},
    {"name": "Ship1", "cost": 30,  "capacity": 165, "transit_time": 10},
    {"name": "Ship2", "cost": 25,  "capacity": 190, "transit_time": 14},
    {"name": "Train1", "cost": 70, "capacity": 80, "transit_time": 8},
    {"name": "Train2", "cost": 65,  "capacity": 90, "transit_time": 9},
    {"name": "Train3", "cost": 85,  "capacity": 65, "transit_time": 7},
    {"name": "Truck7", "cost": 95,  "capacity": 45, "transit_time": 5},
    {"name": "Truck8", "cost": 130, "capacity": 50, "transit_time": 7},
    {"name": "Plane3", "cost": 800, "capacity": 120, "transit_time": 1},
    {"name": "Ship3",  "cost": 28,  "capacity": 200, "transit_time": 12},
    {"name": "Train4", "cost": 60,  "capacity": 100, "transit_time": 10},
    {"name": "Truck9",  "cost": 100, "capacity": 55, "transit_time": 6},
    {"name": "Truck10", "cost": 115, "capacity": 48, "transit_time": 5},
    {"name": "Plane4",  "cost": 900, "capacity": 130, "transit_time": 1},
    {"name": "Ship4",   "cost": 27,  "capacity": 210, "transit_time": 13},
    {"name": "Train5",  "cost": 75,  "capacity": 95,  "transit_time": 9}
]


df_i = pd.DataFrame(containers)
df_vehicles = pd.DataFrame(vehicles)

# Sets
N = df_i["name"].tolist()
M = df_vehicles["name"].tolist()

# Parameters

# Delay penalty for item i
p_i = df_i.set_index("name")["delay_penalty"].to_dict()

# Cost of bin j
C_j = df_vehicles.set_index("name")["cost"].to_dict()

# Capacity of bin j
Q_j = df_vehicles.set_index("name")["capacity"].to_dict()

# Transport time of bin j (days)
T_j = df_vehicles.set_index("name")["transit_time"].to_dict()

# Weight of container i
w_i = df_i.set_index("name")["weight"].to_dict()

# Due time of container i
D_i = df_i.set_index("name")["due"].to_dict()

# Release time of container i
A_i = df_i.set_index("name")["release"].to_dict()

# A very large number for bigM >> 0 
bigM = 1000000

# Making Model

model = gp.Model("Bin Packing with Time Constraint")

x_ij = model.addVars(N, M, vtype=GRB.BINARY, name="x_ij")
u_j = model.addVars(M, vtype=GRB.BINARY, name="u_j")
t_j = model.addVars(M, vtype=GRB.CONTINUOUS, name="t_j")
d_i = model.addVars(N, vtype=GRB.CONTINUOUS, name="d_i")

model.setObjective(
    gp.quicksum(u_j[j]*C_j[j] for j in M) +
    gp.quicksum(d_i[i]*p_i[i] for i in N),
    sense=GRB.MINIMIZE)

# Adding constraints
for i in N:
    model.addConstr(gp.quicksum(x_ij[i, j] for j in M) == 1, name=f"assign_{i}")
    
for j in M:
    model.addConstr(
        gp.quicksum(w_i[i] * x_ij[i, j] for i in N) <= Q_j[j] * u_j[j],
        name=f"capacity_{j}"
    )

for i in N:
    for j in M:
        model.addConstr(
            t_j[j] >= A_i[i] * x_ij[i, j],
            name=f"release_time_{i}_{j}"
        )

for i in N:
    for j in M:
        model.addConstr(
            t_j[j] + T_j[j] <= D_i[i] + d_i[i] + bigM * (1 - x_ij[i, j]),
            name=f"arrival_time_{i}_{j}"
        )

# Solve Model

model.optimize()

# Check if a feasible solution was found
if model.status == GRB.OPTIMAL:
    print("\nObjective Value:", model.ObjVal)
    
    print("\n--- Container Assignments ---")
    for i in N:
        for j in M:
            if x_ij[i, j].X > 0.5:
                print(f"{i} → {j}")
    
    print("\n--- Bins Used ---")
    for j in M:
        if u_j[j].X > 0.5:
            print(f"{j} used, departs at time {t_j[j].X:.1f}")
    
    print("\n--- Delays ---")
    for i in N:
        if d_i[i].X > 1e-5:
            print(f"{i} has delay: {d_i[i].X:.1f}")
else:
    print("No feasible solution found.")
    model.computeIIS()
    model.write("model.ilp")
    sys.exit("No solution - program closes")


# Collect departure times for each vehicle (columns)
depart_times = [t_j[j].X for j in M]

# Collect delay times for each container (rows)
delay_times = [d_i[i].X for i in N]

# Compute loading percentages for each vehicle
loading_percent = []

# Build the binary assignment matrix
VisualMatrix = np.zeros((len(N), len(M)))

for i in N:
    for j in M:
        i_idx = N.index(i)
        j_idx = M.index(j)
        val = x_ij[i, j].X
        VisualMatrix[i_idx, j_idx] = 1 if val > 0.5 else 0
        
for j in M:
    total_weight = sum(w_i[i] for i in N if x_ij[i, j].X > 0.5)
    loading = total_weight / Q_j[j] if Q_j[j] > 0 else 0
    loading_percent.append(round(loading * 100, 1))  # in %, rounded

# Create DataFrame with container names as row indices and vehicle names as columns
df_visual = pd.DataFrame(VisualMatrix, index=N, columns=M)

# Add delay times as a new column
df_visual['Delay Time'] = delay_times

# Add departure times as a new row (append at the bottom)
depart_row = pd.Series(depart_times + [np.nan], index=df_visual.columns, name='Depart Time')  # np.nan to align with 'Delay Time' column
df_visual = pd.concat([df_visual, depart_row.to_frame().T])
# Create the row with loading percentages (add NaN for the 'Delay Time' column)
loading_row = pd.Series(loading_percent + [np.nan], index=df_visual.columns, name='Loading %')

# Append to df_visual
df_visual = pd.concat([df_visual, loading_row.to_frame().T])

# Heatmap of assignments (excluding the last two rows that contain departure and loading info)
assignment_matrix = df_visual.iloc[:-2, :-1].astype(int)
plt.figure(figsize=(12, 8))
sns.heatmap(assignment_matrix, cmap="Blues", cbar=False, linewidths=0.5, linecolor='gray')
plt.title("Container Assignments to Vehicles")
plt.xlabel("Vehicles")
plt.ylabel("Containers")
plt.show()

# Bar chart for loading percentages
plt.figure(figsize=(10, 5))
vehicles = df_visual.columns[:-1]
plt.bar(vehicles, loading_percent)
plt.title("Loading Percentages per Vehicle")
plt.ylabel("Loading (%)")
plt.xticks(rotation=45)
plt.show()

# Bar chart for delays per container
containers = df_visual.index[:-2]
plt.figure(figsize=(12, 5))
plt.bar(containers, delay_times)
plt.title("Delay Times per Container")
plt.ylabel("Delay (time units)")
plt.xticks(rotation=90)
plt.show()

# Departure times per vehicle (only vehicles used)
used_vehicles = [j for j in df_visual.columns[:-1] if any(df_visual[j].iloc[:-2] == 1)]
used_depart_times = [depart_times[df_visual.columns.get_loc(j)] for j in used_vehicles]

plt.figure(figsize=(10, 5))
plt.bar(used_vehicles, used_depart_times, color='green')
plt.title("Vehicle Departure Times (Used Vehicles Only)")
plt.ylabel("Departure Time")
plt.xticks(rotation=45)
plt.show()

