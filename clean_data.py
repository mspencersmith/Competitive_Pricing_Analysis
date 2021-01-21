import pandas as pd
from clean import Clean as cd

filename = 'data/pricing_data.csv'
df = pd.read_csv(filename, encoding='unicode_escape')


clean = df.applymap(cd.remove_non_ascii, na_action='ignore')

clean['price'] = clean['price'].map(cd.only_digits, na_action='ignore')

clean.to_csv('data/cleaned_pricing_data.csv', index=False)
