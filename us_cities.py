import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import random
import math

file_path = 'data/uscities.csv'
df = pd.read_csv(file_path)
df_sorted = df.sort_values(by='population', ascending=False)
top_100_cities = df_sorted.head(100)

# distance calculator

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the Haversine distance between two points in 
    latitude and longitude in miles.
    """
    earth_radius = 3958.8

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

def guess_city_map(answer, guess):
    answer_rows = top_100_cities[top_100_cities['city']==answer]
    guess_rows = top_100_cities[top_100_cities['city']==guess]

    if answer_rows.empty or guess_rows.empty:
        st.write('')
        return None


    answer_lat = top_100_cities[top_100_cities['city']==answer]['lat'].iloc[0]
    answer_lon = top_100_cities[top_100_cities['city']==answer]['lng'].iloc[0]
    guess_lat = top_100_cities[top_100_cities['city']==guess]['lat'].iloc[0]
    guess_lon = top_100_cities[top_100_cities['city']==guess]['lng'].iloc[0]

    distance = distance = haversine_distance(answer_lat, answer_lon, guess_lat, guess_lon)

    cities_data = [
        {'city':answer,'lat':answer_lat,'lon':answer_lon},
        {'city':guess,'lat':guess_lat,'lon':guess_lon}
    ]

    results_df = pd.DataFrame(cities_data)
    results_gdf = gpd.GeoDataFrame(results_df, geometry=gpd.points_from_xy(results_df.lon, results_df.lat))

    
    # Set max x and y for map output
    min_lon = min(results_gdf['geometry'].bounds['minx'])
    max_lon = max(results_gdf['geometry'].bounds['maxx'])
    min_lat = min(results_gdf['geometry'].bounds['miny'])
    max_lat = max(results_gdf['geometry'].bounds['maxy'])

    # Calculate the center point of the two cities
    center_lon = (min_lon + max_lon) / 2
    center_lat = (min_lat + max_lat) / 2

    # Set a level of zoom
    extent_range = round(distance/100)

    min_lon_ex = center_lon - extent_range
    max_lon_ex = center_lon + extent_range
    min_lat_ex = center_lat - extent_range
    max_lat_ex = center_lat + extent_range

    # Ensure that the bounding box stays within valid range
    min_lon_f = max(min_lon_ex, -180)
    max_lon_f = min(max_lon_ex, 180)
    min_lat_f = max(min_lat_ex, -90)
    max_lat_f = min(max_lat_ex, 90)

    if guess == answer:
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        fig, ax = plt.subplots(figsize=(12, 8))
        world.boundary.plot(ax=ax, linewidth=1)
        results_gdf.plot(ax=ax, color='blue', markersize=20, label='City Guess')
        ax.set_xlim(min_lon_f, max_lon_f)
        ax.set_ylim(min_lat_f, max_lat_f)

        # Set title
        plt.title('City Guess')

        # Show the map
        plt.show()
        st.write(guess + ' is correct!')
        st.pyplot(fig)

    else:

        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        fig, ax = plt.subplots(figsize=(12, 8))
        world.boundary.plot(ax=ax, linewidth=1)

        index_to_remove = results_gdf[results_gdf['city'] == answer].index[0]
        results_gdf.drop(index_to_remove, inplace=True)
        results_gdf.plot(ax=ax, color='red', markersize=20, label='City Guess')
        ax.set_xlim(min_lon_f, max_lon_f)
        ax.set_ylim(min_lat_f, max_lat_f)

        # Set title
        plt.title('City Guess')

        # Show the map
        plt.show()
        st.write(guess + ' is ' + str(distance) + ' miles away from the correct city')
        st.pyplot(fig)

x = random.randint(0,100)

# random number keeps changing - fix later 


correct_city = top_100_cities['city'][50]
user_guess = 'Austin'

# Title
st.title("Guess the US City Game")
st.write('You have five attempts to guess the random US city. You can only guess cities from the top 100 us cities by population. Good Luck!')


i = 1

try:
    while user_guess:

        if i < 6:

            user_guess = st.text_input(
            'Guess a City in the US',
            key=i)
        
            # Result validation
            if user_guess.lower() not in [city.lower() for city in top_100_cities['city']]:
                st.warning(
                    f"Please only choose from the top 100 US cities by population"
                )

            #if st.button('Submit Guess',key=i+10):
            guess_city_map(correct_city,user_guess)
            i += 1

            if user_guess == correct_city:
                break

        else:
            st.write("Too many guesses, the correct answer was " + correct_city + " - refresh and try again!")
            break
except TypeError:
    st.warning(
        "Waiting for input. Please refresh the page if you feel something is wrong."
    )

except SystemExit:
    pass
