import os.path
import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
average_price = os.path.join(BASE_DIR, 'data/average_price.csv')
count_file = os.path.join(BASE_DIR, 'data/bedroom_count.csv')
dates_file = os.path.join(BASE_DIR, 'collection/dates.json')

with open(dates_file) as f:
    dates = json.load(f)

months = dates['months']
month_index = dates['month_ind']
avg_all = pd.read_csv(average_price)
count = pd.read_csv(count_file)
plt.style.use('seaborn')

def graph(df, col, y_axis, title, output=False):
    print(df)
    avg = df.plot.line(x='date', y=col, title=title)
    avg.set_xlabel('Date')
    avg.set_ylabel(y_axis)
    avg.set_xticks(month_index)
    avg.set_xticklabels(months, fontsize='small')
    if output:
        plt.savefig(output, dpi=400, bbox_inches='tight')
    plt.show()

graph(avg_all, ['median'], 'Price(£)', 'Average Price Per Week (£)', 'graphs/average.png')
graph(avg_all, ['max', 'median', 'min'], 'Price(£)', 'Maximum, Median, and Minimum Price Per Week', 'graphs/max_med_min.png')
graph(count, ['rooms_1', 'rooms_2', 'rooms_3', 'rooms_4', 'rooms_5', 'rooms_6'], 'Number of Properties', 'Properties Available', 'graphs/room_count.png')