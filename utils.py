import pandas as pd
import os

def load_export_data(filename):
    paths = [
        os.path.join('../data/exports', filename),
        os.path.join('data/exports', filename),
        os.path.join('../../data/exports', filename)
    ]
    for path in paths:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None