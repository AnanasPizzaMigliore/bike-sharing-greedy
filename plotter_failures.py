import numpy as np
import matplotlib.pyplot as plt

unopt = np.load(r'D:\Master Thesis\Bike py\Results\results_2017_6_unopt.npz')
dynamic = np.load(r'D:\Master Thesis\Bike py\Results\results_2017_6_1800_0.02.npz')
capacity_10 =np.load(r'D:\Master Thesis\Bike py\Results\results_2017_6_1800_0.02_10.npz')
capacity_20 =np.load(r'D:\Master Thesis\Bike py\Results\results_2017_6_1800_0.02_20.npz')
capacity_5 =np.load(r'D:\Master Thesis\Bike py\Results\results_2017_6_1800_0.02_5.npz')
total_full_unopt = unopt['total_full']
total_empty_unopt = unopt['total_empty']
total_full_dynamic = dynamic['total_full']
total_empty_dynamic = dynamic['total_empty']
total_full_capacity_10 = capacity_10['total_full']
total_empty_capacity_10 = capacity_10['total_empty']
total_full_capacity_20 = capacity_20['total_full']
total_empty_capacity_20 = capacity_20['total_empty']
total_full_capacity_5 = capacity_5['total_full']
total_empty_capacity_5 = capacity_5['total_empty']
total_rebalance_5 = capacity_5['total_rebalance']
total_rebalance_10 = capacity_10['total_rebalance']
total_rebalance_20 = capacity_20['total_rebalance']
total_time = 3600*24
full_failure_unopt = np.mean(total_full_unopt, axis = 1)/total_time
empty_failure_unopt = np.mean(total_empty_unopt, axis = 1)/total_time
total_failure_unopt = full_failure_unopt + empty_failure_unopt
full_failure_dynamic = np.mean(total_full_dynamic, axis = 1)/total_time
empty_failure_dynamic = np.mean(total_empty_dynamic, axis = 1)/total_time
total_failure_dynamic = full_failure_dynamic + empty_failure_dynamic
full_failure_10 = np.mean(total_full_capacity_10, axis = 1)/total_time
empty_failure_10 = np.mean(total_empty_capacity_10, axis = 1)/total_time
total_failure_capacity_10 = full_failure_10 + empty_failure_10
full_failure_20 = np.mean(total_full_capacity_20, axis = 1)/total_time
empty_failure_20 = np.mean(total_empty_capacity_20, axis = 1)/total_time
total_failure_capacity_20 = full_failure_20 + empty_failure_20
full_failure_5 = np.mean(total_full_capacity_5, axis = 1)/total_time
empty_failure_5 = np.mean(total_empty_capacity_5, axis = 1)/total_time
total_failure_capacity_5 = full_failure_5 + empty_failure_5

weekday = ['Monday', 'Tuesday', 'Wednsday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.plot(weekday, full_failure_unopt, label = 'Unoptimized')
plt.plot(weekday, full_failure_dynamic, label = 'Dynamic')
plt.plot(weekday, full_failure_10, label = 'Capacity 10')
plt.plot(weekday, full_failure_20, label = 'Capacity 20')
plt.plot(weekday, full_failure_5, label = 'Capacity 5')
plt.legend()
plt.xlabel('Weekdays')
plt.ylabel('Fraction of time in the full state')
plt.savefig('images/full.eps')
plt.show()

plt.plot(weekday, empty_failure_unopt, label = 'Unoptimized')
plt.plot(weekday, empty_failure_dynamic, label = 'Dynamic')
plt.plot(weekday, empty_failure_10, label = 'Capacity 10')
plt.plot(weekday, empty_failure_20, label = 'Capacity 20')
plt.plot(weekday, empty_failure_5, label = 'Capacity 5')
plt.legend()
plt.xlabel('Weekdays')
plt.ylabel('Fraction of time in the empty state')
plt.savefig('images/empty.eps')
plt.show()

plt.plot(weekday, total_failure_unopt, label = 'Unoptimized')
plt.plot(weekday, total_failure_dynamic, label = 'Dynamic')
plt.plot(weekday, total_failure_capacity_10, label = 'Capacity 10')
plt.plot(weekday, total_failure_capacity_20, label = 'Capacity 20')
plt.plot(weekday, total_failure_capacity_5, label = 'Capacity 5')
plt.legend()
plt.xlabel('Weekdays')
plt.ylabel('Fraction of time in the failure states')
plt.savefig('images/failure.eps')
plt.show()

weekdays = np.array([4,4,4,5,5,4,4])
distance_dynamic = dynamic['total_distance'] / weekdays
distance_capacity_5 = capacity_5['total_distance'] / weekdays
distance_capacity_10 = capacity_10['total_distance'] / weekdays
distance_capacity_20 = capacity_20['total_distance'] / weekdays
plt.plot(weekday, distance_dynamic, label = 'Dynamic')
plt.plot(weekday, distance_capacity_5, label = 'Capacity 5')
plt.plot(weekday, distance_capacity_10, label = 'Capacity 10')
plt.plot(weekday, distance_capacity_20, label = 'Capacity 20')
plt.xlabel('Weekdays')
plt.ylabel('Distance per rebalancing (meter)')
plt.legend()
plt.savefig('images/distance.eps')
plt.show()

station_positions = np.load(r'D:\Master Thesis\Bike py\station_positions.npz')
positions = station_positions['positions']
ids = station_positions['station_ids']
#print(ids)
count = dynamic['station_count']
another_count = count[:]
visited = np.nonzero(count)
another_count[visited] = 1
#print(count)
img = plt.imread(r'D:\Master Thesis\Bike py\images\NYC.png')
plt.figure(figsize = (10,10))
plt.imshow(img, extent = (-74.02, -73.92, 40.67, 40.81))
plt.scatter(positions[1], positions[0], c = another_count, marker = '.', cmap = 'rainbow')
plt.colorbar()
plt.xlim(-74.02, -73.92)
plt.ylim(40.67, 40.81)
plt.savefig('images/station_rebalanced.eps')
plt.show()

count = dynamic['station_count']
visited = np.nonzero(count)
plt.figure(figsize = (10,10))
plt.imshow(img, extent = (-74.02, -73.92, 40.67, 40.81))
plt.scatter(positions[1][visited], positions[0][visited], c = count[visited], marker = '.', cmap = 'rainbow')
plt.colorbar()
plt.xlim(-74.02, -73.92)
plt.ylim(40.67, 40.81)
plt.savefig('images/station_vsited.eps')
plt.show()

trip_count_5 = capacity_5['total_trip'] / weekdays / total_rebalance_5 + 1
trip_count_10 = capacity_10['total_trip'] / weekdays / total_rebalance_10 + 1
trip_count_20 = capacity_20['total_trip'] / weekdays / total_rebalance_20 + 1
plt.plot(weekday, trip_count_5, label = 'Capacity 5')
plt.plot(weekday, trip_count_10, label = 'Capacity 10')
plt.plot(weekday, trip_count_20, label = 'Capacity 20')
plt.xlabel('Weekdays')
plt.ylabel('Number of trucks per rebalancing operation')
plt.legend()
plt.savefig('images/Trips.eps')
plt.show()