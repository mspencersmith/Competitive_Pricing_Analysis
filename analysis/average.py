import os.path
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def avg_all(file, out_file=None):
    """Returns average price of all properties"""
    df = get_df(file)
    date = df.groupby(['date'])
    average_price = average(date['price'])
    if out_file:
        create_csv(out_file, average_price)
    return average_price

def avg_rooms(file, num, out_file=None):
    """Returns average price of properties of given room size"""
    df = get_df(file)
    rooms = group_rooms(df, num)
    date = rooms.groupby(['date'])
    average_price = average(date['price'])
    if out_file:
        create_csv(out_file, average_price)

def count_rooms(file, out_file=None): 
    df = get_df(file)
    bed_count = pd.DataFrame(index=df['date'].unique())
    for i in range(1, 7):
        rooms = group_rooms(df, i)
        date = rooms.groupby(['date'])
        count = date['rooms'].count()
        bed_count = pd.merge(bed_count, count, left_index=True,
            right_index=True, how='outer', suffixes=(None, f'_{i}'))
    bed_count.rename(columns = {'rooms':'rooms_1'}, inplace=True)
    bed_count.index.name = 'date'
    bed_count.fillna(0, inplace=True)
    if out_file:
        create_csv(out_file, bed_count)
    return bed_count

def group_rooms(df, num):
    df['rooms'] = df['rooms'].str.lower()
    filt = df['rooms'].str.contains(f'{num} bedrooms', na=False)
    rooms = df[filt]
    return rooms

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