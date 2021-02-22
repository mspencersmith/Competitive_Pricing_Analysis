import json
import os.path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from clean import Clean as cd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
pricing = os.path.join(BASE_DIR,'data/pricing_data.csv')
df = pd.read_csv(pricing, encoding='unicode_escape')

# Returns the string without non ASCII characters
clean = df.applymap(cd.remove_non_ascii, na_action='ignore')

# Finds pounds, or pounds and pence and returns as a float
clean['price'] = clean['price'].map(cd.pounds_and_pence, na_action='ignore') 

clean.boxplot('price')
# plt.savefig('graphs/price_boxplot.png', dpi=400, bbox_inches='tight')
plt.show()

checkin_dates = os.path.join(BASE_DIR,'collection/dates.json')
with open(checkin_dates) as f:
    checkins = json.load(f)
dates = checkins['checkin']

"""Calculates interquartile range and removes outliers"""
for date in dates:
    date_group = clean.groupby(['date']).get_group(date)
    LL, UL = cd.outlier_limits(date_group['price'])
    outliers = date_group['price'][(date_group['price'] < LL) | (date_group['price'] > UL)]
    clean.drop(outliers.index, axis=0, inplace=True)

output = os.path.join(BASE_DIR,'data/cleaned_pricing_data.csv')
clean.to_csv(output, index=False)
