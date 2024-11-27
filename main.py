import pandas as pd

df = pd.read_csv('test.csv')

df.rename(columns={
    'latitude_filled': 'lat',
    'longitude_filled': 'lng'
}, inplace=True)

df.to_csv('covid-eua.csv', index=False)