# -*- coding: utf-8 -*-
"""
Created on Tue May  6 12:43:57 2025

@author: evert
"""

import pandas as pd
import numpy as np
from itertools import chain, combinations
import matplotlib.pyplot as plt
from itertools import permutations
import networkx as nx
from mpl_toolkits.basemap import Basemap as Basemap

# Read Data file
TotalVol = pd.read_excel('Data2.xlsx', sheet_name='TotalVol', header=0, index_col=0)  # Read the total volum
RoadDist = pd.read_excel('Data2.xlsx', sheet_name='RoadDist', header=0, index_col=0)  # Read RoadDist
RailDist = pd.read_excel('Data2.xlsx', sheet_name='RailDist', header=0, index_col=0)  # Read RailDist
RailSpec = pd.read_excel('Data2.xlsx', sheet_name='ModeSpecifications', header=0,
                         index_col=0)  # Read Rail Specifications
InputParameters = pd.read_excel('Data2.xlsx', sheet_name='InputParameters', header=0,
                                index_col=0)  # Read input parameters
Pos_data1 = pd.read_excel('Data2.xlsx', sheet_name='NodeCoordinates', header=0, index_col=0)  # Read input parameters

# ODASC is the alternative specific constant -- You may need to use it in the optimiztion model
ODASC = pd.read_excel('Data2.xlsx', sheet_name='Asc', header=0, index_col=0)  # Read ASC

##### Calculate the parameters of the model
W = TotalVol.to_numpy() / 100  # Weight of the shipments (tonne)
RaD = RailDist.to_numpy()  # Rail Distance (km)
RoD = RoadDist.to_numpy()  # Road Distance
RS = RailSpec.to_numpy()  # Rail specification
IP = InputParameters.to_numpy()  # Input parameters
OD = ODASC.to_numpy()  # OD specifications
pos_data = Pos_data1.to_numpy()

# Inputs related to the utility function
# The following three elements might be needed if you want to calculate the users behavior
# You need to enter the values that you have calculated in the first part of the assignment - the current values are fake!
Beta = IP[2][0]  # parameter of the choice model
Mu = IP[3][0]  # parameter of the choice model

# ---- Sets ----
n = len(RailDist)  # Number of countries
N = range(9, 18)  # Set of countries (from 9 to 18)

# Calculate Road and Rail time (hour)
RoadTime = RoD / RS[0, 2]  # Travel time on road
RailTimeT1 = RaD / RS[1, 2]  # Travel time on Rail Type 1

# Calculate Road and Rail tarif (Cost per tonne)
RoadTariff = RoD * RS[0, 0]  # Road Tarif (cost per road mode per OD pair)
RailTariffT1 = RaD * RS[1, 0]  # Rail type tarrif

Road_time_ODm = 0
Rail_time_ODm = 0

def powerset(iterable):  # returns all possible combinations from the elements of list
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def estimateCost_Time_ODm(i, j, m,
                          hubs):  # i,j are OD pair, m represents mode, m=0 means road, m=1 means railtype 1, Hubs is the list of hubs selected
    mode_selector = 0
    if m == 0:
        return RoadTariff[i][j], RoadTime[i][j], mode_selector, None
    elif m == 1:  # Intermodal
        minCost = float('inf')
        minTime = float('inf')
        minEmission = float('inf')
        if not hubs or len(hubs) == 1:
            return RoadTariff[i][j], RoadTime[i][j], mode_selector, None
        elif len(hubs) >= 2:
            perm = permutations(hubs, 2)
            for selected_hubs in list(perm):
                temp = RoadTariff[i][selected_hubs[0]] + RailTariffT1[selected_hubs[0]][selected_hubs[1]] + \
                       RoadTariff[selected_hubs[1]][j] + 2 * IP[1][0]
                temp_Time = RoadTime[i][selected_hubs[0]] + RailTimeT1[selected_hubs[0]][selected_hubs[1]] + \
                            RoadTime[selected_hubs[1]][j]
                tempTotal = temp + (Beta * temp_Time)
                minCost = min(minCost, tempTotal)
                if minCost == tempTotal:
                    minTempCost = temp
                    minTime = temp_Time
                    mode_selector = 1
                    best_hubs = selected_hubs
            return minTempCost, minTime, mode_selector, best_hubs
    elif m == 2:  # Direct rail mode
        minCost = float('inf')
        minTime = float('inf')
        minEmission = float('inf')
        best_hubs = (i - 9, j - 9)
        return RailTariffT1[i - 9][j - 9] + OD[i - 9][0] + OD[j - 9][1], RailTimeT1[i - 9][
            j - 9], mode_selector, best_hubs

def findDemandIndex(i):
    if i < 9:
        return i + 9
    else:
        return i

def flow_Quantity_ODm_estimator(hubs):
    # ---- Create empty systemic utility matrices we will fill later on ----

    gen_cost_ODm = np.zeros((n, n, len(M)))  # SystUtil per Transport Mode on each OD

    # calculate the systematic utility for all modes, for all OD-pairs
    for i in N:
        for j in N:
            for m in M:
                # We take the systematic utility for intrazonal transport as 0, no
                # matter the ASCs, this is done to get the modal split to 50/50 %
                # for intrazonal transport
                if i == j:
                    gen_cost_ODm[i, j, m] = 0

                # For non-intrazonal transport, the systematic utility per OD-pair
                # for both road and rail
                # tempp_hub2= (0,4)
                if i != j:
                    if m == 0:
                        cost_estimate, time_estimate, m_selected, best_hubs = estimateCost_Time_ODm(i, j, 0, Hubs)
                        gen_cost_ODm[i, j, m] = (Beta * time_estimate) + cost_estimate

                    elif m == 1 and (i - 9) in Hubs and (j - 9) in Hubs:
                        cost_estimate, time_estimate, m_selected, best_hubs = estimateCost_Time_ODm(i, j, 1, Hubs)
                        gen_cost_ODm[i, j, m] = (Beta * time_estimate) + cost_estimate

                    elif m == 2 and (i - 9) in Hubs and (j - 9) in Hubs:
                        cost_estimate, time_estimate, m_selected, best_hubs = estimateCost_Time_ODm(i, j, 2, Hubs)
                        gen_cost_ODm[i, j, m] = (Beta * time_estimate) + cost_estimate

                    else:
                        gen_cost_ODm[i, j, m] = 10000  # penalty for closed hubs

    # calculate the estimated share(s) of each mode
    Estimated_Share_ODm = np.zeros((n, n, len(M)))
    denominator_ESm = np.zeros((n, n))
    for i in N:
        for j in N:
            for m in M:
                denominator_ESm[i, j] = denominator_ESm[i, j] + np.exp(-Mu * gen_cost_ODm[i, j, m])
    for i in N:
        for j in N:
            for m in M:
                Estimated_Share_ODm[i, j, m] = np.exp(-Mu * gen_cost_ODm[i, j, m]) / denominator_ESm[i, j]

    flow_Quantity_ODm = np.zeros((n, n, len(M)))  # Flow quantity on each OD per Transport Mode

    for i in N:
        for j in N:
            for m in M:
                flow_Quantity_ODm[i, j, m] = flow_Quantity_ODm[i, j, m] + Estimated_Share_ODm[i, j, m] * W[
                    findDemandIndex(i), findDemandIndex(j)]
    return flow_Quantity_ODm, denominator_ESm





def estimateFinalFlows_ODm(
        hubs):  # i,j are OD pair, m represents mode, m=0 means road, m=1 means railtype 1, Hubs is the list of hubs selected
    flow_Quantity_ODm = np.zeros((n, n))  # Flow quantity on each OD per Transport Mode

    for i in N:
        for j in N:
            if i != j:
                minCost = float('inf')
                tempMode = -1
                bestMode = -1
                bestHubs = [-1, -1]
                for m in M:
                    tempCost = float('inf')
                    if m == 0:
                        tempCost = (RoadTariff[i][j] + Beta * RoadTime[i][j]) * W[
                            findDemandIndex(i), findDemandIndex(j)]
                        tempMode = m
                    elif m == 1:  # Intermodal
                        if not hubs or len(hubs) == 1:
                            tempCost = (RoadTariff[i][j] + Beta * RoadTime[i][j]) * W[
                                findDemandIndex(i), findDemandIndex(j)]
                            tempMode = m
                        elif len(hubs) >= 2:
                            perm = permutations(hubs, 2)
                            for selected_hubs in list(perm):
                                temp = ((RoadTariff[i][selected_hubs[0]] + Beta * RoadTime[i][selected_hubs[0]]) +
                                        (RailTariffT1[selected_hubs[0]][selected_hubs[1]] + Beta *
                                         RailTimeT1[selected_hubs[0]][selected_hubs[1]])
                                        + (RoadTariff[selected_hubs[1]][j] + Beta * RoadTime[selected_hubs[1]][j]) + 2 *
                                        IP[1][0]) * W[findDemandIndex(i), findDemandIndex(j)]
                                if tempCost > temp:
                                    tempCost = temp
                                    tempMode = m
                                    bestHubs = selected_hubs
                    elif m == 2:  # Direct rail mode
                        tempCost = ((RoadTariff[i][i - 9] + Beta * RoadTime[i][i - 9])
                                    + (RailTariffT1[i - 9][j - 9] + Beta * RailTimeT1[i - 9][j - 9])
                                    + (RoadTariff[j - 9][j] + Beta * RoadTime[j - 9][j]) + +OD[i - 9][0] + OD[j - 9][
                                        1]) * W[findDemandIndex(i), findDemandIndex(j)]
                        tempMode = m
                    # print("mode %d cost %f", m, tempCost)
                    if minCost > tempCost:
                        minCost = tempCost
                        bestMode = tempMode

                if bestMode == 0:
                    flow_Quantity_ODm[i, j] = W[findDemandIndex(i), findDemandIndex(j)]
                    #print(1)
                elif bestMode == 1:
                    flow_Quantity_ODm[i, bestHubs[0]] = W[findDemandIndex(i), findDemandIndex(j)]
                    flow_Quantity_ODm[bestHubs[0], bestHubs[1]] = W[findDemandIndex(i), findDemandIndex(j)]
                    flow_Quantity_ODm[bestHubs[1], j] = W[findDemandIndex(i), findDemandIndex(j)]
                    #print(2)
                elif bestMode == 2:
                    flow_Quantity_ODm[i - 9, j - 9] = W[findDemandIndex(i), findDemandIndex(j)]
                    #print(3)

    return flow_Quantity_ODm

''' Experiment loop starts here'''


number_of_Possible_Hubs = 9  # Total number of possible hub locations
# For road (m=0), intermodal (m=1), and direct rail (m=2)
M = range(
    3)  # number of modes, 0: Road transport, 1 : Intermodal trasnport with hub in atleast one different country, 2: Rail mode

combiList = list()  # to store all possible combinations

HubList = list(range(number_of_Possible_Hubs))
for i, combo in enumerate(powerset(HubList), 1):
    combiList.append(combo)
    pass

total_Open_Hubs_Combinations = len(combiList)  # total number of combinations
Gen_cost_System = [0] * total_Open_Hubs_Combinations  # to store gen cost for each hub combination
combi_Hubs_map = [0] * total_Open_Hubs_Combinations  # to map the combination number to number of open hubs

bestIndex = [0] * (
            number_of_Possible_Hubs + 1)  # to store the index of best hub combination for n open hubs, n ={0,1, 2, ..., 9}
bestCost = [0] * (
            number_of_Possible_Hubs + 1)  # to store the total cost of best hub combination for n open hubs, n ={0,1, 2, ..., 9}

for x, Hubs in enumerate(powerset(HubList), 0):  # x is combination no, Hubs : is the list of selected hubs
    # Temp_Hub = (0,1,2)
    # if(Hubs ==Temp_Hub):
    flow_Quantity_ODm, denominator_ESm = flow_Quantity_ODm_estimator(Hubs)

    Gen_cost_OD = np.zeros((n, n))
    for i in N:
        for j in N:
            Gen_cost_OD[i][j] = -1 * np.log(np.sum(denominator_ESm[i][j])) / Mu

    for i in N:
        for j in N:
            if i != j:
                Gen_cost_System[x] = Gen_cost_System[x] + Gen_cost_OD[i][j] * W[
                    findDemandIndex(i), findDemandIndex(j)]  # NEED to change W

    Gen_cost_System[x] = Gen_cost_System[x] + [len(Hubs) * IP[0][0]]
    combi_Hubs_map[x] = len(Hubs)

    #storing the best cost and index values
    if (bestCost[combi_Hubs_map[x]] == 0):
        bestCost[combi_Hubs_map[x]] = Gen_cost_System[x]
        bestIndex[combi_Hubs_map[x]] = x

    elif (bestCost[combi_Hubs_map[x]] >= Gen_cost_System[x]):
        bestCost[combi_Hubs_map[x]] = Gen_cost_System[x]
        bestIndex[combi_Hubs_map[x]] = x

print(" ********************************************************** ")
for i in range(number_of_Possible_Hubs + 1):
    print(i, "hubs:", 'Cost = ',bestCost[i][0], 'Best combination:', combiList[bestIndex[i]], )

# -----------------------------------------------------------------------------
# Plotting graphs starts here

# select 1 for pareto graph and 2 for network graph
graphSelector = 2
selected_hubs = (1, 4, 5, 7)
flow_Quantity_ODmm = estimateFinalFlows_ODm(selected_hubs)
xaxis = range(1, number_of_Possible_Hubs + 1)
bestCost_filtered = bestCost[1:]

# Pareto graph as investment increases
x = range(number_of_Possible_Hubs + 1)

if (graphSelector == 1):
    plt.plot(xaxis, bestCost_filtered)
    plt.xlabel('Investment cost (no of hubs opened)')
    plt.ylabel('Generalized system cost')
    plt.title('Investment VS Generalized cost')

else:
    #Network graph of flows of the selected hub scenario
    T = range(0, 18)
    t = 18
    route_data = pd.DataFrame(columns=['Source', 'Destination', 'Total flow'])
    for i in T:
        for j in T:
            if i != j:
                new_row = {'Source': i, 'Destination': j, 'Total flow': flow_Quantity_ODmm[i][j]}
                # condition to check and add the flows if the row already exists
                if ((route_data['Source'] == new_row['Source']) & (
                        route_data['Destination'] == new_row['Destination'])).any():
                    route_data['Total flow'] = route_data['Total flow'] + flow_Quantity_ODmm[i][j]
                else:
                    # adding a new row to the dataframe
                    route_data.loc[len(route_data), route_data.columns] = new_row
    # removing unnecessary rows with 0 flows
    route_data_updated = route_data[route_data['Total flow'] != 0]
    
    #Instantiation of the network
    graph = nx.Graph()
    
    #adding nodes
    graph.add_nodes_from(route_data_updated['Source'])
    #adding edges
    graph = nx.from_pandas_edgelist(route_data_updated, source='Source', target='Destination', edge_attr='Total flow')

    plt.figure(figsize=(10, 9))
    #basemap to focus on Europe using coordinates
    m = Basemap(projection='merc', llcrnrlon=-5, llcrnrlat=40, urcrnrlon=25, urcrnrlat=60, lat_ts=0, resolution='l',
                suppress_ticks=False)
    
    #Copying geo coordinates of hub and demand locations from the input data 
    mx, my = m(Pos_data1['Lon'].values, Pos_data1['Lat'].values)
    pos = {} 
    for count, elem in enumerate(Pos_data1['id']):
        pos[elem] = (mx[count], my[count])
        
    
    #Seperating hubs and OD nodes
    hub_nodes=[]
    demand_nodes =[]
    labels ={}
    for gn in graph.nodes():
        if gn < 9:
            hub_nodes.append(gn)
            labels[gn]= int(gn)
        else:
            demand_nodes.append(gn)
            labels[gn] = int(gn)
            
    #plotting the nodes on network
    nx.draw_networkx_nodes(G=graph, pos= pos, nodelist=hub_nodes, node_color='r', node_shape='^', node_size= 170, label= "hub")
    nx.draw_networkx_nodes(G=graph, pos=pos, nodelist=demand_nodes, node_color='b', node_shape='o', node_size=120, label= "origin")

    #Extracting rail and road mode specifications seperately
    rail_lines=[]
    rail_flow=[]
    road_lines=[]
    road_flow=[]
    for edge in graph.edges():
        if edge[0] <9 and edge[1] <9:
            rail_lines.append(edge)
            rail_flow.append(0.0003 *graph.adj[edge[0]][edge[1]]['Total flow'])
        else:
            road_lines.append(edge)
            road_flow.append(0.0003* graph.adj[edge[0]][edge[1]]['Total flow'])

    #Plotting the edges on network
    nx.draw_networkx_edges(graph, pos, width=1.0, alpha=0.5,arrows=True,arrowstyle="->", arrowsize=10)
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=rail_lines,
        width=rail_flow ,
        alpha=0.5,
        edge_color="tab:red",
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=road_lines,
        width=road_flow,
        alpha=0.4,
        edge_color="tab:blue",
    )
    nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_color="black")
    
    #plotting the map of Europe
    m.drawcountries(linewidth=3)
    m.drawstates(linewidth=0.2)
    m.drawcoastlines(linewidth=3)
    nx.draw_networkx(graph, with_labels=True)

    plt.tight_layout()
    plt.show()












