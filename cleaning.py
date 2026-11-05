'''Clean given txt file'''

import src.loader as load
import numpy as np
import pandas as pd

route = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\routes.txt')
stop_times = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\stop_times.txt')
stops = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\stops.txt')
trips = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\trips.txt')
cleaned_stop_times = load.load_gtfs_file(r'Transit-Route-Finder\data\main data\cleaned_stop_times.txt')

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

def time_parser(s: str) -> int | float:
    '''
    _summary_

    Args:
        s (str): a Datetime string in H:M:S format

    Returns:
        int | float: _description_
    '''
    if not isinstance(s, str):
        return np.nan

    splitted_s = s.split(":")
    if (len(splitted_s) != 3) or (not splitted_s[0].isdigit()) or (not splitted_s[1].isdigit()) or (not splitted_s[2].isdigit()):
        return np.nan

    a = list(map(int, splitted_s))
    hours = a[0]
    minutes = a[1]
    seconds = a[2]

    if (minutes >= 60) or (seconds >= 60):
        return np.nan

    return hours * 3600 + minutes * 60 + seconds

cleaned_stop_times["stop_sequence"] = convert_num(stop_times['stop_sequence'], 'col_asd_sort')
cleaned_stop_times["drop_off_type"] = convert_num(stop_times['drop_off_type'], 'col_asd_sort')
cleaned_stop_times["arrival_seconds"] = stop_times['arrival_time'].map(time_parser)
cleaned_stop_times["departure_seconds"] = stop_times['departure_time'].map(time_parser)

max_time = (convert_num(stop_times['arrival_time'], conv_type='time_a')).max()
bad_time_val = (convert_num(stop_times['arrival_time'], conv_type='time_a')).isna().sum()

cleaned_stop_times.to_csv(r'Transit-Route-Finder\data\main data\cleaned_stop_times.txt', index=False)
print(cleaned_stop_times.info())