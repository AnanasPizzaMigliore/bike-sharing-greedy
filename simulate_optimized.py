import numpy as np
import pandas as pd
import glob
import calendar
from optimal_states import optimal_states
from add_trip import add_trip
from optimize import optimize
import pdb

bike_ids = pd.read_csv('bike_ids.csv')
bike_ids = bike_ids[bike_ids.columns[0]].values
stationids_capacities = pd.read_csv('stationids_capacities.csv')
station_ids = stationids_capacities[stationids_capacities.columns[0]].values
capacities = stationids_capacities[stationids_capacities.columns[1]].values
simple_markov = np.load('simple_markov_frequencies.npz')
arrivals = simple_markov['arrivals']
departures = simple_markov['departures']
station_count = np.zeros(len(station_ids))

bike_file = glob.glob(r'D:\Master Thesis\Bike py\Data\*.csv')
survival_file = glob.glob(r'D:\Master Thesis\Bike py\Markov_matrix\*.npz')

# simulated month for test data


    # time intervals
Tr = 60*60
Tp = 15*60
    
    # optimization parameters
beta = 1800
gamma = 0.02
p_th = 0.1
    
    # load data (rows: trips, cols: [start_time/trip_duration/start_id/end_id/bike_id/weekday]
    # load data of year 17 month 6
data = pd.read_csv(bike_file[47])
survival = np.load(survival_file[0],allow_pickle=True)
    
survival_mat = survival['survival'].reshape(1,-1)
survival_mat = survival_mat[0][0]
    
start_time = pd.to_datetime(data[data.columns[1]])
second = (start_time - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
data[data.columns[1]] = second
data.sort_values(by = data.columns[1], inplace = True)
data.reset_index(drop = True, inplace = True)
second = data[data.columns[1]]
    
second = second + 7200
    
start_station = data[data.columns[3]]
end_station = data[data.columns[7]]
trip_duration = data[data.columns[0]]

    #data.sort_values(by = data.columns[1]) 
    
year = start_time.dt.year
month = start_time.dt.month
weekday = start_time.dt.weekday
    
days = calendar.monthrange(year[0], month[0])[1] # number of days in current month
sec_per_day = 3600*24
    
weekday = weekday[0] # day of the week of first day of month
month = month[0]
year = year[0]
if (np.mod(second[0], 86400) <= 7200):
    weekday = np.mod(weekday + 1, 7)
        
time_offset = second[0] - np.floor(np.mod(second[0], sec_per_day))
trip = 0
    
    # measurement vectors
total_empty = np.zeros((7, len(station_ids)))
total_full = np.zeros((7, len(station_ids)))
failures = np.zeros((len(station_ids), 2))
sent_trucks = 0
total_distance = np.zeros((7))
    
    # utility vectors
emptied = np.zeros(len(station_ids))
filled = np.zeros(len(station_ids))
traveling = []
    
    # initial states
state = np.zeros((len(station_ids)))
h = 0 #starting hour
start_date = np.array([h, weekday, 1, month, year]).astype(int)
#print(f'the start date: {start_date}')
state = np.ceil(capacities/2)
#print(f'state {state}, survival {survival}')
    
for day in range(days):
    for hour in range(24):
        #print(f'day {day}, hour {hour}\n')
            # find survival times and ideal state
            # survival = zeros(1, length(station_ids));
            # max_survival = zeros(1, length(station_ids));
            # optimal_state = zeros(1, length(station_ids));
        date = np.array([hour, weekday, day, month, year])
            
        [optimal_state, survival, max_survival] = optimal_states(p_th,state,capacities,departures,arrivals,Tr,Tp,date,
                                                                 survival_mat,day==days);
        #old_state = state
        #distance = 0
        #trucks = 0
            
            # optimize and rebalance
        [state, trucks, distance, count] = optimize(state, survival, max_survival, optimal_state, beta, gamma)
        station_count = station_count + count
        total_distance[weekday] = total_distance[weekday] + distance
        sent_trucks = sent_trucks + trucks
            
            #old_state
            #survival
            #max_survival
            #trucks
            
            # calculate empty/full time
        if(trucks > 0):
            for i in range(len(station_ids)):
                if (state[i] > 0 and emptied[i] > 0):
                    total_empty[weekday, i] = total_empty[weekday, i] + time_offset - emptied[i]
                    emptied[i] = 0
                    
                if (state[i] < capacities[i] and filled[i] > 0):
                    total_full[weekday, i] = total_full[weekday, i] + time_offset - filled[i]
                    filled[i] = 0
                        
        time_offset = time_offset + 3600
            
            # demand
        while ((trip < len(second) and second[trip] < time_offset) or ( len(traveling) != 0 and traveling[0][0] < time_offset)):
            if (np.mod(trip, 1000)==0):
                print(f'trip {trip}')
            #print(f'traveling {traveling}')
            if ( len(traveling) != 0 and ( trip >= len(second) or traveling[0][0] < second[trip])):
                    # arrival
                arrival_time = traveling[0][0]
                station = traveling[0][1]
                #print(f'arrival_time {arrival_time}, station {station}')
                if (state[station] == capacities[station]):
                        # failure: the station is full
                    failures[station, 1] = failures[station, 1] + 1
                else:
                        # arrival
                    state[station] = state[station] + 1
                    
                    if (state[station] == capacities[station]):
                        filled[station] = arrival_time
 
                        # if the station was empty, calculate empty time
                    if (emptied[station] > 0):
                        if (emptied[station] > arrival_time):
                            print(f'empty station time {emptied}')
                            print('error may occur here tag 1')
                            pdb.set_trace()
                    #print(f'traveling {traveling}')
                        total_empty[weekday, station] = total_empty[weekday, station] + arrival_time - emptied[station]
                        emptied[station] = 0
 
                del traveling[0]
            else:
                    # departure
                station = np.where(station_ids == start_station[trip])
                station = station[0]
                #print(f'station {station}')
                if(state[station] == 0):
                    failures[station, 0] = failures[station, 0] + 1
                else:
                        # departure
                    state[station] = state[station] - 1
                    if (state[station] == 0):
                        emptied[station] = second[trip]

                        
                        # schedule arrival
                    arrival_time = second[trip] + trip_duration[trip]
                    if (arrival_time < second[trip]):
                        print('error may occur here tag 2')
                        pdb.set_trace()
 
                    arrival_station = np.where(station_ids == end_station[trip])
                    arrival_station = arrival_station[0]
                    #print(f'arrival time {arrival_time}, arrival station {arrival_station} value {arrival_station} 
                    #length {len(arrival_station)}\n')
                    if (len(arrival_station) != 0):
                        traveling = add_trip(traveling, arrival_time, arrival_station)

                        
                        # if the station was full, calculate full time
                    if (filled[station] > 0):
                        total_full[weekday, station] = total_full[weekday, station] + second[trip] - filled[station]
                        filled[station] = 0
 
                trip = trip + 1

        #np.save(strcat('results_', num2str(year), '_', num2str(month), '_unopt.mat'));
    weekday = np.mod(weekday + 1, 7)

    
total_time = days * sec_per_day
print(f'year: {year}, month: {month}')
    
    #np.save(strcat('results_', num2str(year), '_', num2str(month), '_unopt.mat'));
np.savez('Results/results_' + str(year) + '_' + str(month) + '_' + str(beta) + '_' + str(gamma), 
         total_full = total_full, total_empty = total_empty, failures = failures, sent_trucks = sent_trucks, 
         total_distance = total_distance, station_count = station_count)
    
