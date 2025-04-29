
#Excel toy test file

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

province_list = ['Groningen',
                 'Friesland',
                 'Drenthe',
                 'Overijsel',
                 'Gelderland',
                 'Utrecht',
                 'Noord-Holland',
                 'Zuid-Holland',
                 'Zeeland',
                 'Noord-Brabant',
                 'Limburg']

OD = np.array([
    [15, 60, 94, 105, 55, 136, 131, 253, 342, 253, 366],
    [56, 15, 92, 98, 56, 155, 124, 230, 325, 256, 428],
    [101, 95, 15, 48, 103, 106, 151, 144, 253, 242, 283],
    [106, 100, 50, 15, 96, 96, 164, 144, 187, 189, 227],
    [60, 63, 100, 108, 15, 149, 220, 197, 247, 139, 216],
    [164, 135, 103, 109, 145, 15, 96, 97, 104, 100, 141],
    [141, 135, 143, 162, 192, 109, 15, 106, 160, 128, 193],
    [238, 230, 140, 143, 196, 105, 106, 15, 104, 105, 196],
    [381, 372, 256, 206, 267, 103, 155, 103, 15, 99, 153],
    [258, 271, 254, 184, 139, 101, 118, 104, 99, 15, 106],
    [430, 436, 293, 240, 189, 159, 216, 190, 147, 95, 15],
])

β = -0.01
cost_values = np.array(OD)

c_ij = pd.DataFrame(OD, index=province_list, columns=province_list)

A_i = np.array([124, 26, 19, 97, 157, 38, 182, 290, 75, 98, 114])
B_j = np.array([41, 19, 15, 69, 95, 33, 127, 177, 43, 78, 59])

flow_matrix = np.zeros((len(province_list),len(province_list)))

for i in range(len(province_list)):
    for j in range(len(province_list)):
        flow_matrix[i,j] = A_i[i]*B_j[j]*math.exp(OD[i,j]*β)
        
c_ij_list = np.arange(0,500,20)
r_ij_list = np.zeros(len(c_ij_list))
for i in range(len(c_ij_list)):
    r_ij_list[i] = math.exp(β*c_ij_list[i])

plt.figure(1)
plt.plot(c_ij_list,r_ij_list)
plt.grid()
plt.title("Deterrence Function")
plt.xlabel("Transport Costs")
plt.ylabel("Deterrence Function Value")
plt.show()
    
    










