import pandas as pd
import numpy as np

def load_gtfs_file(file_path):
    df = pd.read_csv(file_path, dtype=str)
    return df
