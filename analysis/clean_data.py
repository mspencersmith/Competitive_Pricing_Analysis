import os.path
import pandas as pd
import numpy as np
from clean import Clean as cd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
filename = os.path.join(BASE_DIR,'data/pricing_data.csv')

df = pd.read_csv(filename, encoding='unicode_escape')

clean = df.applymap(cd.remove_non_ascii, na_action='ignore')

clean['price'] = clean['price'].map(cd.pounds_and_pence, na_action='ignore')

outliers = clean['price'][clean['price']=='35000']

clean.drop(outliers.index, axis=0, inplace=True) # Deletes rows with outliers

output = os.path.join(BASE_DIR,'data/cleaned_pricing_data.csv')

clean.to_csv(output, index=False)
