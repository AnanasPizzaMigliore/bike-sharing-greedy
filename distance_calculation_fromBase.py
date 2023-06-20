import pandas as pd
import numpy as np
from find_distance import find_distance

stationids_capacities = pd.read_csv('stationids_capacities.csv')
station_ids = stationids_capacities[stationids_capacities.columns[0]]
M = len(station_ids)
ids = station_ids
distances = np.zeros(M)
station_positions = np.load('station_positions.npz')
positions = station_positions['positions']

base = np.array([40.646581, -74.016238])

for i in range(M):
    id1 = np.where(station_ids == ids[i])
    distances[i] = find_distance(positions[:, id1], base)


np.savez('station_distances_from_base',distances = distances,station_ids = station_ids)
