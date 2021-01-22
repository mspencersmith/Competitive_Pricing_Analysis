import os.path
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data = os.path.join(BASE_DIR, 'data/cleaned_pricing_data.csv')

df = pd.read_csv(data)

date = df.groupby(['date'])

average_price = date['price_GBP'].agg(['min','max','mean', 'median'])

average_price = average_price.round(2)

print(average_price)

output = os.path.join(BASE_DIR, 'data/average_price.csv')
average_price.to_csv(output)




