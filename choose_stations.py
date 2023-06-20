import numpy as np
import pandas as pd
import glob

tosave = 1

min_active_months = [12,12] # for train and test, respectively
min_cap = 10; # minimum capacity

stations_train = np.zeros((2, 4500))
stations_test = np.zeros((2, 4500))
connections = np.zeros((4500, 4500))
bikes = np.zeros((40000))

print('\nTRAIN\n')

file_path = glob.glob(r'D:\Master Thesis\Bike py\Data\*.csv')

for i in range(48): # from 213.07-2016.06
    data = pd.read_csv(file_path[i])
    start_station_id = data.columns[3]
    end_station_id = data.columns[7]
    bike_id = data.columns[11]
    print(f'run in the {i}-th file')
    for trip in range(len(data)):
        start = data[start_station_id][trip]
        end = data[end_station_id][trip]
        if stations_train[1,start] == 0:
            stations_train[0, start] = stations_train[0, start] + 1
            stations_train[1, start] = 1
        if stations_train[1, end] == 0:
            stations_train[0, end] = stations_train[0, end] + 1
            stations_train[1 , end] = 1
        connections[start, end] = connections[start, end] + 1
        bikes[data[bike_id][trip]] = 1
    stations_train[1,:] = 0
    


print('\n\nTEST\n')

for i in range(48,60): # from 2016.07-217.06
    data = pd.read_csv(file_path[i])
    start_station_id = data.columns[3]
    end_station_id = data.columns[7]
    bike_id = data.columns[11]
    print(f'run in the {i}-th file')
    for trip in range(len(data)):
        start = data[start_station_id][trip]
        end = data[end_station_id][trip]
        if stations_test[1,start] == 0:
            stations_test[0, start] = stations_test[0, start] + 1
            stations_test[1, start] = 1
        if stations_test[1, end] == 0:
            stations_test[0, end] = stations_test[0, end] + 1
            stations_test[1 , end] = 1
        connections[start, end] = connections[start, end] + 1
        bikes[data[bike_id][trip]] = 1
    stations_test[1,:] = 0


# determine used bikes ids
bike_ids = np.where(bikes==1)

# select stations that were active at least min_active_months
station_ids_train = np.where(stations_train[0,:]>=min_active_months[0])
station_ids_test = np.where(stations_test[0,:]>=min_active_months[1])

# select only stations that were active both in the traina nd test datasets
station_ids = np.intersect1d(station_ids_train, station_ids_test)


# Read capacity value for each station in stations.
# The csv file has 4 columns: [id, available docks, total docks, available bikes]
M = pd.read_csv('capacities.csv')
 
ids = M[M.columns[0]]
capacities = M[M.columns[2]]

station_ids = ids[np.isin(ids,station_ids)]
station_capacities = capacities[np.isin(ids, station_ids)]

station_ids = station_ids[station_capacities>min_cap]
station_capacities = station_capacities[station_capacities>min_cap]

if tosave:
    stationids_capacities_df = pd.DataFrame({'Station ID': station_ids, 'Capacities': station_capacities})
    stationids_capacities_df.to_csv('stationids_capacities.csv', index = False)
    bike_ids_df = pd.DataFrame({'Bike ID': bike_ids[0]})
    bike_ids_df.to_csv('bike_ids.csv', index = False)