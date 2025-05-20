# -*- coding: utf-8 -*-
"""
Created on Tue May 20 14:09:03 2025

@author: evert
"""

import sys
import numpy as np
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

delay_factor = 1

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
    {"name": "Container13","weight": 12, "due": 27,  "release": 21, "delay_penalty": 60},
    {"name": "Container14","weight": 63,  "due": 19, "release": 13, "delay_penalty": 60},
    {"name": "Container15","weight": 45, "due": 23,  "release": 10, "delay_penalty": 40},
    {"name": "Container16","weight": 76,  "due": 17, "release": 0, "delay_penalty": 80},
    {"name": "Container17","weight": 85, "due": 5,  "release": 3, "delay_penalty": 0},
    {"name": "Container18","weight": 23,  "due": 22, "release": 11, "delay_penalty": 0},
    {"name": "Container19","weight": 12, "due": 16,  "release": 10, "delay_penalty": 20},
    {"name": "Container20","weight": 3,  "due": 15, "release": 1, "delay_penalty": 60}
]

vehicles = [
    {"name": "Truck1", "cost": 100, "capacity": 38, "transit_time": 5},
    {"name": "Truck2", "cost": 150, "capacity": 35, "transit_time": 4},
    {"name": "Truck3", "cost": 124, "capacity": 40, "transit_time": 8},
    {"name": "Truck4", "cost": 90, "capacity": 35, "transit_time": 6},
    {"name": "Truck5", "cost": 90, "capacity": 35, "transit_time": 6},
    {"name": "Plane1", "cost": 550, "capacity": 75, "transit_time": 2},
    {"name": "Plane2", "cost": 750, "capacity": 100, "transit_time": 1},
    {"name": "Ship1", "cost": 30,  "capacity": 165, "transit_time": 10},
    {"name": "Ship2", "cost": 25,  "capacity": 190, "transit_time": 14},
    {"name": "Train1", "cost": 70, "capacity": 80, "transit_time": 8},
    {"name": "Train2", "cost": 65,  "capacity": 90, "transit_time": 9},
    {"name": "Train3", "cost": 85,  "capacity": 65, "transit_time": 7}
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
    gp.quicksum(d_i[i] for i in N)*delay_factor,
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



