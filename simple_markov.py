import numpy as np
import pandas as pd
import glob

stationids_capacities = pd.read_csv('stationids_capacities.csv')
station_ids = stationids_capacities[stationids_capacities.columns[0]]
num_stats = len(station_ids)
trips = 24*7*12
sec_per_hour = 3600
hour_per_day = 24
sec_per_day = sec_per_hour*hour_per_day

arrivals = np.zeros((trips, num_stats))
departures = np.zeros((trips, num_stats))
seen = np.zeros((trips))

file_path = glob.glob(r'D:\Master Thesis\Bike py\Data\*.csv')

for i in range(48):
    print(f'run the {i}-th file\n')
    data = pd.read_csv(file_path[i])
    old_date_dep = 0
    old_date_arr = 0
    start_time = pd.to_datetime(data[data.columns[1]])
    duration_sec = data[data.columns[0]]
    second = (start_time - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
    weekday = start_time.dt.weekday
    month = start_time.dt.month
    dep_station = data[data.columns[3]]
    arr_station = data[data.columns[7]]
    for trip in range(len(data)):
        hour_dep = np.mod(np.floor(np.mod(second[trip], sec_per_day) / sec_per_hour).astype(int) + 2, 24) + 1
        hour_arr = np.mod(np.floor(np.mod(second[trip] + duration_sec[trip], sec_per_day) / sec_per_hour).astype(int) + 2, 24) + 1
        day_dep = weekday[trip]
        if (hour_dep < 3):
            day_dep = (day_dep + 1) % 7
            
        day_arr = day_dep
        if (hour_arr < hour_dep):
            day_arr = (day_dep + 1) % 7

        index_dep = (month[trip] - 1) * 168 + day_dep * hour_per_day + hour_dep - 1
        index_arr = (month[trip] - 1) * 168 + day_arr * hour_per_day + hour_arr - 1
        if (old_date_dep < np.floor(second[trip] / sec_per_day) + hour_dep / hour_per_day):
            seen[index_dep] = seen[index_dep] + 1
            old_date_dep = np.floor(second[trip] / sec_per_day) + hour_dep / hour_per_day

        departed = np.where(station_ids == dep_station[trip])
        arrived = np.where(station_ids == arr_station[trip])
        arrivals[index_arr, arrived] = arrivals[index_arr, arrived] + 1
        departures[index_dep, departed] = departures[index_dep, departed] + 1

for i in range(trips):
    if (seen[i] > 0):
        departures[i, :] = departures[i, :] / seen[i]
        arrivals[i, :] = arrivals[i, :] / seen[i]

np.savez('simple_markov_frequencies', arrivals = arrivals, departures = departures)

