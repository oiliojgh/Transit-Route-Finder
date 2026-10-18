'''Code file'''
import shutil
import src.loader as load
import pandas as pd
import numpy as np

route = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\routes.txt')
stop_times = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\stop_times.txt')
stops = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\stops.txt')
trips = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\trips.txt')
mod_stop_times = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\modified_stoptimes.txt')

shutil.copyfile(r'Transit-Route-Finder\data\main data\stop_times.txt',
                r'Transit-Route-Finder\data\main data\modified_stoptimes.txt')


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

def convert_num(s: pd.Series, conv_type: str ='col_asd') -> pd.Series[int]:
    """_summary_

    Args:
        s (pd.Series): A Pandas series
        type (str, optional): Type of conversion (col_asd, col_asd_sort, time_a). Defaults to 'col_asd'.

    Returns:
        pd.Series: A converted Pandas Series
    """
    if conv_type == 'time_a':
        return pd.to_numeric((s.str.split(':')).str[0], errors="coerce")
    elif conv_type == 'col_asd_sort':
        return (pd.to_numeric(s, errors="coerce")).sort_values(ascending=False)
    return pd.to_numeric(s, errors="coerce")
#---------------------------------------------------------------------------------------------
'''
Archive:

load_sum('route', route)
load_sum('stop times', stop_times)
load_sum('trips', trips)
load_sum('stops', stops)

print(stop_times["trip_id"].isin(trips["trip_id"]))
print(stop_times["stop_id"].isin(stops["stop_id"]))

print(f'{sum(stop_times["trip_id"].isin(trips["trip_id"])) - len(stop_times["trip_id"].isin(trips["trip_id"]))=}')
print(f'{sum(stop_times["stop_id"].isin(stops["stop_id"])) - len(stop_times["stop_id"].isin(stops["stop_id"]))=}')

print(stops['location_type'].value_counts())
print(convert_num(stop_times['stop_sequence']), conv_type='col_asd_sort')
print(convert_num(stop_times['stop_lat']), conv_type='col_asd_sort')
print(convert_num(stop_times['stop_lon'], conv_type='col_asd_sort'))
'''

max_time = (convert_num(stop_times['arrival_time'], conv_type='time_a')).max()
bad_time_val = (convert_num(stop_times['arrival_time'], conv_type='time_a')).isna().sum()

mod_stop_times["stop_sequence"] = convert_num(stop_times['stop_sequence'], 'col_asd_sort')
mod_stop_times["stop_lat"] = convert_num(stop_times['stop_lat'], 'col_asd_sort')
mod_stop_times["stop_lon"] = convert_num(stop_times['stop_lon'], 'col_asd_sort')
mod_stop_times["stop_id"] = convert_num(stop_times['stop_id'], 'col_asd_sort')

splitted_time = stop_times['arrival_time'].str.split(":", expand=True).apply(pd.to_numeric, errors="coerce")
a = hours × 3600 + minutes × 60 + seconds
