import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

file_path = 'data/uscities.csv'
df = pd.read_csv(file_path)
df_sorted = df.sort_values(by='population', ascending=False)
top_200_cities = df_sorted.head(200)

print('top 200 us cities')