import os.path
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
average_price = os.path.join(BASE_DIR, 'data/average_price.csv')
dates_file = os.path.join(BASE_DIR, 'collection/dates.json')

with open(dates_file) as f:
    dates = json.load(f)

months = dates['months']
month_index = dates['month_ind']
avg_all = pd.read_csv(average_price)

plt.style.use('seaborn')

print(avg_all)

def graph(col, title, output=False):
    avg = avg_all.plot.line(x='date', y=col, title=title)
    avg.set_xlabel('Date')
    avg.set_ylabel('Price(£)')
    avg.set_xticks(month_index)
    avg.set_xticklabels(months, fontsize='small')
    if output:
        plt.savefig(output, dpi=400, bbox_inches='tight')
    plt.show()

graph(['median'], 'Average Price Per Week (£)', 'graphs/average.png')
graph(['max', 'median', 'min'], 'Maximum, Median, and Minimum Price Per Week', 'graphs/max_med_min.png')