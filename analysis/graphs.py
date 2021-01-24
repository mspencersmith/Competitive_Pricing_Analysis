import os.path
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data = os.path.join(BASE_DIR, 'data/average_price.csv')

df = pd.read_csv(data)

months = []
month_index = []
get_months = lambda x: [months.append(x), month_index.append(df['month'][df['month']==x].index[0])]
df['month'].map(get_months, na_action='ignore')


print(df)
plt.style.use('seaborn')
avg = df.plot.line(x='date', y=['mean', 'median'], title='Average Price Per Week (£)')

avg.set_xlabel('Date')
avg.set_ylabel('Price(£)')

avg.set_xticks(month_ind)
avg.set_xticklabels(months, fontsize='small')

plt.savefig('graphs/average.png', dpi=400, bbox_inches='tight')

minp = df.plot.line(x='date', y=['min'], title='Average Price Per Week (£)')

minp.set_xlabel('Date')
minp.set_ylabel('Price(£)')

minp.set_xticks(month_ind)
minp.set_xticklabels(months, fontsize='small')

plt.savefig('graphs/min.png', dpi=400, bbox_inches='tight')
plt.show()


