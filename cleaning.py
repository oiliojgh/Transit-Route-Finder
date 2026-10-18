'''Clean given txt file'''

import shutil
import src.loader as load
import pandas as pd
import numpy as np

route = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\routes.txt')
stop_times = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\stop_times.txt')
stops = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\stops.txt')
trips = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\trips.txt')
mod_stop_times = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\modified_stoptimes.txt')

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

mod_stop_times["stop_sequence"] = convert_num(stop_times['stop_sequence'], 'col_asd_sort')
mod_stop_times["stop_lat"] = convert_num(stop_times['stop_lat'], 'col_asd_sort')
mod_stop_times["stop_lon"] = convert_num(stop_times['stop_lon'], 'col_asd_sort')
mod_stop_times["stop_id"] = convert_num(stop_times['stop_id'], 'col_asd_sort')

max_time = (convert_num(stop_times['arrival_time'], conv_type='time_a')).max()
bad_time_val = (convert_num(stop_times['arrival_time'], conv_type='time_a')).isna().sum()

splitted_time = stop_times['arrival_time'].str.split(":", expand=True).apply(pd.to_numeric, errors="coerce")
a = hours × 3600 + minutes × 60 + seconds