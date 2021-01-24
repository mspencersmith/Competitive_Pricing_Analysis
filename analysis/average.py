import os.path
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def avg_all(file, out_file=None):

    df = get_data(file)
    date = df.groupby(['date'])

    average_price = date['price_GBP'].agg(['min','max','mean', 'median'])

    average_price = average_price.round(2)

    print(average_price)

    if out_file:
        output = os.path.join(BASE_DIR, out_file)
        average_price.to_csv(output)

def get_df(file):
    data = os.path.join(BASE_DIR, file)
    df = pd.read_csv(data)
    return df

avg_all('data/cleaned_pricing_data.csv','data/average_price.csv')
