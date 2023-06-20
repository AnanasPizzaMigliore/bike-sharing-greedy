import numpy as np
import pandas as pd
import markov_survival as MS

stationids_capacities = pd.read_csv('stationids_capacities.csv')
bike_ids = pd.read_csv('bike_ids.csv')
simple_markov_frequencies = np.load('simple_markov_frequencies.npz')

station_ids = stationids_capacities[stationids_capacities.columns[0]]
capacities = stationids_capacities[stationids_capacities.columns[1]]
max_stations = len(station_ids)
departures = simple_markov_frequencies['departures']
arrivals = simple_markov_frequencies['arrivals']

# time intervals
Tr = 60*60
Tp = 15*60
sec_per_day = 3600*24
p_th = 0.1

# survival matrix
survival = {}
for i in range(max_stations):
    survival[i] = np.zeros((7, 24, capacities[i] + 1))
    
day = 10
""""
# simulated month
year = 13

for month in range(7,13):
    for weekday in range(7):
        for hour in range(24):
            for station in range(max_stations):
                M = capacities[station]
                markov = MS.Markov_Survival(p_th, M, departures[:,station], arrivals[:,station], Tr, Tp,  hour, weekday, day, month, year)
                T = markov.T()
                #print(f'output T {T} \n')
                T_mat = survival[station]
                #print(f'output T_mat {T_mat}')
                T_mat[weekday , hour] = T
                survival[station] = T_mat
                #print(f'output survival {T_mat}')
                print(f'year: {year}, month: {month}, weekday: {weekday}, hour: {hour} station: {station}')     
    np.savez('Markov_matrix/survival_' + str(year) + '_' + str(month) + '_' + str(p_th), survival = survival)


for year in range(14,18):
    for month in range(1,13):
        for weekday in range(7):
            for hour in range(24):
                for station in range(max_stations):
                    M = capacities[station]
                    markov = MS.Markov_Survival(p_th, M, departures[:,station], arrivals[:,station], Tr, Tp,  hour, weekday, day, month, year)
                    T = markov.T()
                    T_mat = survival[station]
                    T_mat[weekday , hour] = T
                    survival[station] = T_mat
                    print(f'year: {year}, month: {month}, weekday: {weekday}, hour: {hour} station: {station}')
        np.savez('Markov_matrix/survival_' + str(year) + '_' + str(month) + '_' + str(p_th), survival = survival)
"""""

year = 17
month = 6

for weekday in range(7):
    for hour in range(24):
        for station in range(max_stations):
            M = capacities[station]
            markov = MS.Markov_Survival(p_th, M, departures[:,station], arrivals[:,station], Tr, Tp,  hour, weekday, day, month, year)
            T = markov.T()
            T_mat = survival[station]
            T_mat[weekday , hour] = T
            survival[station] = T_mat
            print(f'year: {year}, month: {month}, weekday: {weekday}, hour: {hour} station: {station}')
            np.savez('Markov_matrix/survival_' + str(year) + '_' + str(month) + '_' + str(p_th), survival = survival)