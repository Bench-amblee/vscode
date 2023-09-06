import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import streamlit as st
import random
import math
import numpy as np

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

def miles_to_degrees(miles):
    # Earth radius in miles (approximately 3958.8 miles)
    earth_radius_miles = 3958.8

    # Convert miles to degrees
    degrees = (miles * earth_radius_miles)/80

    return degrees

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

    
    bbox = [-170, 10, -60, 80]  # (min_lon, min_lat, max_lon, max_lat)
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
        #ax.set_xlim(min_lon_f, max_lon_f)
        #ax.set_ylim(min_lat_f, max_lat_f)
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])

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

        radius_in_degrees = miles_to_degrees(distance)
        results_gdf.plot(ax=ax, color='blue', markersize=radius_in_degrees,alpha=0.2)

        #circle = plt.Circle((results_gdf.lon, results_gdf.lat), distance, fill=False, color='blue', alpha=0.5)
        #plt.gca().add_patch(circle)
        #ax.set_xlim(min_lon_f, max_lon_f)
        #ax.set_ylim(min_lat_f, max_lat_f)
        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])

        # Set title
        plt.title('City Guess')

        # Show the map
        plt.show()
        st.write(guess + ' is ' + str(distance) + ' miles away from the correct city')
        st.pyplot(fig)

x = random.randint(0,100)

# random number keeps changing - fix later 


def plot_city_guess(answer,guess):
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

    if guess == answer:
        results_gdf.plot(ax=ax, color='blue', markersize=20, label='City Guess')

    else:
        index_to_remove = results_gdf[results_gdf['city'] == answer].index[0]
        results_gdf.drop(index_to_remove, inplace=True)
        results_gdf.plot(ax=ax, color='red', markersize=20, label='City Guess')
        radius_in_degrees = miles_to_degrees(distance)
        results_gdf.plot(ax=ax, color='blue', markersize=radius_in_degrees,alpha=0.2)

correct_city = top_100_cities['city'][53]
user_guess = 'Austin'

# Title
st.title("Guess the US City Game")
st.write('You have five attempts to guess the random US city. You can only guess cities from the top 100 us cities by population. Good Luck!')
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

fig, ax = plt.subplots(figsize=(12, 8))
world.boundary.plot(ax=ax, linewidth=1)
bbox = [-170, 10, -60, 80]  # (min_lon, min_lat, max_lon, max_lat)
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])




i = 1
key_counter = 0
def get_unique_key():
    global key_counter
    key_counter += 1
    return key_counter

game = True
user_guesses = []
click_count = 0

xxxxxxxxx = '''user_guess = st.selectbox(
            'Guess a City in the US',top_100_cities['city'])
user_guess_submit = st.button('Submit Guess')
'''
# Define a Streamlit nction with caching
@st.cache_data
def add_point(point):
    data_points.append(point)
    return data_points
# Initialize a list to store data points
data_points = []

#session state:
#https://github.com/streamlit/release-demos/blob/0.84/0.84/demos/todo_list.py


# Streamlit runs from top to bottom on every iteraction so
# we check if `count` has already been initialized in st.session_state.

# If no, then initialize count to 0
# If count is already initialized, don't do anything
if 'count' not in st.session_state:
	st.session_state.count = 0

# Create a button which will increment the counter
increment = st.button('Increment')
if increment:
    st.session_state.count += 1
    new_point = np.random.rand()
    updated_data = add_point(new_point)

st.write('Count = ', st.session_state.count)
st.write(data_points)

def front():

    if "city" not in st.session_state:
        st.session_state.map = [
           {"description": "Cities Guessing Game", "done": True}
        ]

    def add_user_guess():
        if st.session_state.new_guess:

            st.session_state.map.append(
            {
                    "description:": st.session_state.new_guess,
                    "done": False
            }
        )
    st.text_input("Guess a City", onchange=add_user_guess, key="new_guess")

    st.write(st.session_state.map)





# Create a Matplotlib figure
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Create an empty line

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Matplotlib Plot with Streamlit')

xyxz = '''while click_count < 6:

    if user_guess_submit:
        user_guesses.append(user_guess)
        click_count +=1

    for city in user_guesses:
        plot_city_guess(correct_city,city)

    st.pyplot(fig)
    st.write(user_guesses)

try:
    while click_count: 

        widget_key_1 = get_unique_key()
        widget_key_2 = get_unique_key()

        user_guess = st.selectbox(
            'Guess a City in the US',top_100_cities['city'],
        key=widget_key_1)
        user_guess_submit = st.button('Submit Guess',
                                          key = widget_key_2)

        if user_guess_submit:
            guess_city_map(correct_city,user_guess)
            user_guesses.append(user_guess)
            click_count +=1
            continue

        if click_count > 5:
            break

            if len(user_guesses) > 5:
                st.write("no more guesses")
                st.write(user_guesses)
                break
            game = True

     '''   
       
xyz = '''
        if i <= 6:
            widget_key_1 = get_unique_key()
            widget_key_2 = get_unique_key()
            user_guess = st.selectbox(
            'Guess a City in the US',top_100_cities['city'],
            key=widget_key_1)
            user_guess_submit = st.button('Submit Guess',
                                          key = widget_key_2)
            

            if user_guess and user_guess_submit:
                guess_city_map(correct_city,user_guess)
                if user_guess == correct_city:
                    game = False
                    i=0
                    break

                #widget_key = get_unique_key()
                #if st.button('Submit Guess',
                         #key = widget_key):
                    #guess_city_map(correct_city,user_guess)
                    #i += 1

           '''
xxxxxx = '''
except TypeError:
    st.warning(
        "Waiting for input. Please refresh the page if you feel something is wrong."
    )

except SystemExit:
    pass
'''