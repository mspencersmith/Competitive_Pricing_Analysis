import json
import pandas as pd
from clean import Clean as cd

filename = 'data/cleaned_pricing_data.csv'

df = pd.read_csv(filename)

date = df.groupby(['date'])

price = date['price_GBP'].agg(['mean', 'median'])

print(price)




