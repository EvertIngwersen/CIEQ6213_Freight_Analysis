# -*- coding: utf-8 -*-
"""
Created on Mon May 26 12:04:47 2025

@author: evert
"""

from bs4 import BeautifulSoup
import pandas as pd

# Load the HTML content
with open("C:/Users/evert/Documents/TU-Delft/TIL Master/CIEQ6213 Freight Transport Networks and Systems/CIEQ6213_Freight_Analysis/Driving Distances between European Cities.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract all distance tables
tables = soup.find_all("table", class_="tablesorter")

# Parse city names from the headers of the first table
header_cells = tables[0].find("thead").find_all("th")[1:]  # skip "Distance (km)"
cities = [cell.text.strip() for cell in header_cells]

# Initialize distance DataFrame
df_distance = pd.DataFrame(index=cities, columns=cities)

# Fill the DataFrame with values from each table
for table in tables:
    rows = table.find("tbody").find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_city = cells[0].text.strip()
        distances = [cell.text.strip().replace('-', '0') for cell in cells[1:]]
        for col_city, distance in zip(cities, distances):
            if row_city in cities and col_city in cities:
                df_distance.loc[row_city, col_city] = int(distance)

# Convert all values to integers
df_distance = df_distance.astype(int)

df_distance.head()  # Display a sample of the dataframe















