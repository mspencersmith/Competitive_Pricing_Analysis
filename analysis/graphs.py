import os.path
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data = os.path.join(BASE_DIR, 'data/average_price.csv')

df = pd.read_csv(data)

print(df)

df.plot.line(x='date', y='median')

plt.show()


