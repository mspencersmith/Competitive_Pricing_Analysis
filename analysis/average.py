import os.path
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def avg_all(file, out_file=None):
    """Returns average price of all properties"""
    df = get_df(file)
    date = df.groupby(['date'])
    average_price = average(date['price_GBP'])
    if out_file:
        create_csv(out_file, average_price)

def avg_rooms(file, rooms, out_file=None):
    """Returns average price of properties of given room size"""
    df = get_df(file)
    df['rooms'] = df['rooms'].str.lower()
    filt = df['rooms'].str.contains(f'{rooms} bedrooms', na=False)
    rooms = df[filt]
    date = rooms.groupby(['date'])
    average_price = average(date['price_GBP'])
    if out_file:
        create_csv(out_file, average_price)

def get_df(file):
    """Joins path and opens csv file"""
    data = os.path.join(BASE_DIR, file)
    df = pd.read_csv(data)
    return df

def average(date):
    """Calcutes average and min max of data series"""
    average_price = date.agg(['min','max','mean', 'median'])
    average_price = average_price.round(2)
    print(average_price)
    return average_price

def create_csv(out_file, average_price):
    output = os.path.join(BASE_DIR, out_file)
    average_price.to_csv(output)