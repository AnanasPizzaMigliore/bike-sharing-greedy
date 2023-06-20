import pandas as pd
import numpy as np
import glob

stationids_capacities = pd.read_csv('stationids_capacities.csv')
station_ids = stationids_capacities[stationids_capacities.columns[0]]
positions = np.zeros((2, len(station_ids)))

file_path = glob.glob(r'D:\Master Thesis\Bike py\Data\*.csv')

for i in range(48):
    data = pd.read_csv(file_path[i])
    start_stations = data[data.columns[3]]
    end_stations = data[data.columns[7]]
    start_lat = data[data.columns[5]]
    start_lon = data[data.columns[6]]
    end_lat = data[data.columns[9]]
    end_lon = data[data.columns[10]]
    print(f'run the {i}-th file\n')
    for j in range(len(start_stations)):
        id1 = np.where(station_ids == start_stations[j])
        id2 = np.where(station_ids == end_stations[j])
        positions[0, id1] = start_lat[j]
        positions[1, id1] = start_lon[j]
        positions[0, id2] = end_lat[j]
        positions[1, id2] = end_lon[j]

np.savez('station_positions',positions = positions,station_ids = station_ids)