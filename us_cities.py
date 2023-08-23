import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st

file_path = 'data/uscities.csv'
df = pd.read_csv(file_path)
df_sorted = df.sort_values(by='population', ascending=False)
top_200_cities = df_sorted.head(200)

sample = top_200_cities.head(10)

st.write('top 10 US cities by Population')
st.dataframe(sample)
st.write('insert map here')