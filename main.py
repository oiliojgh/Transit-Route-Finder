'''Code file'''
import src.loader as load
import pandas as pd
import numpy as np

route = load.load_gtfs_file(r'C:\COde\Transit-Route-Finder\data\main data\routes.txt')
stop_times = load.load_gtfs_file(r'C:\COde\Transit-Route-Finder\data\main data\stop_times.txt')
stops = load.load_gtfs_file(r'C:\COde\Transit-Route-Finder\data\main data\stops.txt')
trips = load.load_gtfs_file(r'C:\COde\Transit-Route-Finder\data\main data\trips.txt')

def test_load():
    '''forced'''
    print(route.shape)
    print(route.head(3))
    print(route.dtypes)

    print(stop_times.shape)
    print(stop_times.head(3))
    print(stop_times.dtypes)

    print(stops.shape)
    print(stops.head(3))
    print(stops.dtypes)

def load_sum(name: str, df: pd.DataFrame):
    '''summarize given DataFrame'''
    print(f'File name: {name}')
    print(f'\nshape: {df.shape}')
    print(f'\nhead: {df.head(4)}')
    print(f'\ndtypes: {df.dtypes}')
    print(f'\nnulls each column: {df.isna().sum()}\n')

#---------------------------------------------------------------------------------------------
'''
Archive:

load_sum('route', route)
load_sum('stop times', stop_times)
load_sum('trips', trips)
load_sum('stops', stops)

print(stop_times["trip_id"].isin(trips["trip_id"]))
print(stop_times["stop_id"].isin(stops["stop_id"]))

'''


print(f'{sum(stop_times["trip_id"].isin(trips["trip_id"])) - len(stop_times["trip_id"].isin(trips["trip_id"]))=}')
print(f'{sum(stop_times["stop_id"].isin(stops["stop_id"])) - len(stop_times["stop_id"].isin(stops["stop_id"]))=}')

print(stops['location_type'].value_counts())
print((pd.to_numeric(stop_times['arrival_time']).astype('Int64')).sort_values(ascending=False))
