import os.path
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

class Bedrooms:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent

for i in range(2, 6):
    file = os.path.join(BASE_DIR, f'data/average_{i}bed_price.csv')
    df = pd.read_csv(file)
    setattr(Bedrooms, f'df{i}', df)

dates_file = os.path.join(BASE_DIR, 'collection/dates.json')
with open(dates_file) as f:
    dates = json.load(f)

months = dates['months']
month_index = dates['month_ind']

plt.style.use('seaborn')

fig1 = plt.figure()
ax1 = fig1.add_subplot(1,1,1)

ax1.plot(Bedrooms.df2['date'], Bedrooms.df2['median'], label='2 Bedrooms')
ax1.plot(Bedrooms.df3['date'], Bedrooms.df3['median'], label='3 Bedrooms')
ax1.plot(Bedrooms.df4['date'], Bedrooms.df4['median'], label='4 Bedrooms')
ax1.plot(Bedrooms.df5['date'], Bedrooms.df5['median'], label='5 Bedrooms')

ax1.legend()

ax1.set_title('Median Price of 2-5 Bedroom Accommodation')
ax1.set_xlabel('Date')
ax1.set_ylabel('Price(£)')
ax1.set_xticks(month_index)
ax1.set_xticklabels(months, fontsize='small')

plt.savefig('graphs/average_bedrooms.png', dpi=400, bbox_inches='tight')

fig2 = plt.figure()
ax2 = fig2.add_subplot(1,1,1)

ax2.plot(Bedrooms.df2['date'], Bedrooms.df2['min'], label='2 Bedrooms')
ax2.plot(Bedrooms.df3['date'], Bedrooms.df3['min'], label='3 Bedrooms')
ax2.plot(Bedrooms.df4['date'], Bedrooms.df4['min'], label='4 Bedrooms')
ax2.plot(Bedrooms.df5['date'], Bedrooms.df5['min'], label='5 Bedrooms')

ax2.legend()

ax2.set_title('Minimum Price of 2-5 Bedroom Accommodation')
ax2.set_xlabel('Date')
ax2.set_ylabel('Price(£)')
ax2.set_xticks(month_index)
ax2.set_xticklabels(months, fontsize='small')

plt.savefig('graphs/minimum_bedrooms.png', dpi=400, bbox_inches='tight')

plt.show()