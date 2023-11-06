from pymongo import MongoClient
import pandas as pd
import json
import geojson
import os
import requests
from dotenv import load_dotenv
import time
import geopandas as gpd
from cartoframes.viz import Map, Layer, popup_element
import folium
from folium.plugins import HeatMap
from shapely.geometry import Polygon
from folium import Icon
from folium import plugins


client = MongoClient("localhost:27017")
db = client["cities_project"]

def mongodb_to_df(name_collection):

    '''Function to get the collections from mongo and turn them to DF
    It takes 1 arg:
    - collection name.
    Also checks for duplicate columns and drops them, only based on lat and long. 
    '''

    df = pd.DataFrame(list(db[name_collection].find()))
    df_drop_duplicates = df.drop_duplicates(subset=df.columns.difference(["name"]))

    return df_drop_duplicates


def mongodb_to_df_geo(name_collection):

    '''Function to get the collections from mongo and turn them to DF
    It takes 1 arg:
    - collection name. 
    '''
    json = db.get_collection(name_collection) 

    return json

def read_geojson(relative_path):
    ''' Function to read geojson.
    It takes 1 arg:
    - Relative path of file.
    '''
    with open(relative_path) as f:
        return gpd.read_file(f)
    

def heat_map(name,loc,neigh_geojson, starbucks_df,stadium_df, schools_df, airport_df, trainstations_df, pet_grooming_df, dog_parks_df, bars_clubs_df,vegan_vegetarian_df):


    ''' Function to create heat maps with all the points of interest for each city.

    takes 12 arguments:
    - geojson of the city
    - the 9 dataframes of points of interests
    - name to save the heatmap
    - location.

    '''


    heatmap = folium.Map(location=loc, zoom_start=12)

    starbucks_coords = []
    stadium_coords = []
    school_coords = []
    trainstations_coords = []
    airport_coords = []
    pet_grooming_coords = []
    dog_parks_coords = []
    bars_clubs_coords = []
    vegan_vegetarian_coords = []


    geometry_starbucks = gpd.points_from_xy(starbucks_df['lon'], starbucks_df['lat'])
    starbucks_places = gpd.GeoDataFrame(starbucks_df, geometry=geometry_starbucks)

    for polygon in neigh_geojson.geometry:

        filtered_starbucks_places = starbucks_places[starbucks_places.geometry.within(polygon)]

        for _, row in filtered_starbucks_places.iterrows():
            starbucks_coords.append([row['lat'], row['lon']])

    geometry_stadium = gpd.points_from_xy(stadium_df['lon'], stadium_df['lat'])
    stadiums = gpd.GeoDataFrame(stadium_df, geometry=geometry_stadium)  

    for polygon in neigh_geojson.geometry:

        filtered_stadiums = stadiums[stadiums.geometry.within(polygon)]

        for _, row in filtered_stadiums.iterrows():
            stadium_coords.append([row['lat'], row['lon']])

    geometry_schools = gpd.points_from_xy(schools_df['lon'], schools_df['lat'])
    schools = gpd.GeoDataFrame(schools_df, geometry=geometry_schools)

    for polygon in neigh_geojson.geometry:

        filtered_schools = schools[schools.geometry.within(polygon)]

        for _, row in filtered_schools.iterrows():
            school_coords.append([row['lat'], row['lon']])

    geometry_airport = gpd.points_from_xy(airport_df['lon'], airport_df['lat'])
    airport = gpd.GeoDataFrame(airport_df, geometry=geometry_airport)

    for polygon in neigh_geojson.geometry:

        filtered_airport = airport[airport.geometry.within(polygon)]

        for _, row in filtered_airport.iterrows():
            school_coords.append([row['lat'], row['lon']])

    geometry_trainstations = gpd.points_from_xy(trainstations_df['lon'], trainstations_df['lat'])
    trainstations = gpd.GeoDataFrame(trainstations_df, geometry=geometry_trainstations)

    for polygon in neigh_geojson.geometry:

        filtered_trainstations = trainstations[trainstations.geometry.within(polygon)]

        for _, row in filtered_trainstations.iterrows():
            school_coords.append([row['lat'], row['lon']])

    geometry_pet_grooming = gpd.points_from_xy(pet_grooming_df['lon'], pet_grooming_df['lat'])
    pet_grooming = gpd.GeoDataFrame(pet_grooming_df, geometry=geometry_pet_grooming)

    for polygon in neigh_geojson.geometry:

        filtered_pet_grooming = pet_grooming[pet_grooming.geometry.within(polygon)]

        for _, row in filtered_pet_grooming.iterrows():
            school_coords.append([row['lat'], row['lon']])

    geometry_dog_parks = gpd.points_from_xy(dog_parks_df['lon'], dog_parks_df['lat'])
    dog_parks = gpd.GeoDataFrame(dog_parks_df, geometry=geometry_dog_parks)

    for polygon in neigh_geojson.geometry:

        filtered_dog_parks = dog_parks[dog_parks.geometry.within(polygon)]

        for _, row in filtered_dog_parks.iterrows():
            school_coords.append([row['lat'], row['lon']])

    geometry_bars_clubs = gpd.points_from_xy(bars_clubs_df['lon'], bars_clubs_df['lat'])
    bars_clubs = gpd.GeoDataFrame(bars_clubs_df, geometry=geometry_bars_clubs)

    for polygon in neigh_geojson.geometry:

        filtered_bars_clubs = bars_clubs[bars_clubs.geometry.within(polygon)]

        for _, row in filtered_bars_clubs.iterrows():
            school_coords.append([row['lat'], row['lon']])

    geometry_vegan_vegetarian = gpd.points_from_xy(vegan_vegetarian_df['lon'],vegan_vegetarian_df['lat'])
    vegan_vegetarian = gpd.GeoDataFrame(vegan_vegetarian_df, geometry=geometry_vegan_vegetarian)

    for polygon in neigh_geojson.geometry:

        filtered_vegan_vegetarian = vegan_vegetarian[vegan_vegetarian.geometry.within(polygon)]

        for _, row in filtered_vegan_vegetarian.iterrows():
            school_coords.append([row['lat'], row['lon']])

        HeatMap(starbucks_coords).add_to(heatmap)

        HeatMap(stadium_coords).add_to(heatmap)

        HeatMap(school_coords).add_to(heatmap)

        HeatMap(airport_coords).add_to(heatmap)

        HeatMap(trainstations_coords).add_to(heatmap)

        HeatMap(pet_grooming_coords).add_to(heatmap)

        HeatMap(dog_parks_coords).add_to(heatmap)

        HeatMap(bars_clubs_coords).add_to(heatmap)

        HeatMap(vegan_vegetarian_coords).add_to(heatmap)
    
        heatmap.save(f"figures/heatmap{name}.html")

        return heatmap
    

def travel(map_name, loc, geojson_data, airports_df, train_stations_df):

    ''' Function to get airports and train stations with markers in a city.
    It takes 5 arg:
    - map name
    - location
    - geo json
    - arport df
    - train df.
    '''

    map = folium.Map(location= loc, zoom_start=12)

    airports = gpd.GeoDataFrame(airports_df, geometry=gpd.points_from_xy(airports_df['lon'], airports_df['lat']))
    train_stations = gpd.GeoDataFrame(train_stations_df, geometry=gpd.points_from_xy(train_stations_df['lon'], train_stations_df['lat']))

    for polygon in geojson_data.geometry:

        airports_f = airports[airports.geometry.within(polygon)]

        for _, row in airports_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          icon=folium.Icon(icon='fa-plane', prefix='fa',color='white', icon_color='darkblue'),
                          popup=row['name']).add_to(map) 

    for polygon in geojson_data.geometry:

        train_stations_f = train_stations[train_stations.geometry.within(polygon)]

        for _, row in train_stations_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          tooltip=["station"], 
                          icon=folium.Icon(icon='fa-train', prefix='fa',color='white', icon_color='black'),
                          popup=row['name']).add_to(map) 

    map.save(f"figures/{map_name}.html")

    return map


def NY_complete(map_name, loc, geojson_data, starbucks_df,stadium_df, schools_df, airport_df, trainstations_df, pet_grooming_df, dog_parks_df, bars_clubs_df,vegan_vegetarian_df):

    ''' Function to get all the requirements in THE city.
    It takes 12 arg:
    - map name
    - location
    - geo json
    - the 9 df with requirements.
    '''

    map = folium.Map(location= loc, zoom_start=12)

    marker_group_1 = folium.FeatureGroup(name='Starbucks')
    marker_group_2 = folium.FeatureGroup(name='Stadiums')
    marker_group_3 = folium.FeatureGroup(name='Schools')
    marker_group_4 = folium.FeatureGroup(name='airports')
    marker_group_5 = folium.FeatureGroup(name='train stations')
    marker_group_6 = folium.FeatureGroup(name='pet grooming')
    marker_group_7 = folium.FeatureGroup(name='dog parks')
    marker_group_8 = folium.FeatureGroup(name='night clubs')
    marker_group_9 = folium.FeatureGroup(name='vegan restaurants')


    starbucks = gpd.GeoDataFrame(starbucks_df, geometry=gpd.points_from_xy(starbucks_df['lon'], starbucks_df['lat']))
    stadium = gpd.GeoDataFrame(stadium_df, geometry=gpd.points_from_xy(stadium_df['lon'], stadium_df['lat']))
    schools = gpd.GeoDataFrame(schools_df, geometry=gpd.points_from_xy(schools_df['lon'], schools_df['lat']))
    airports = gpd.GeoDataFrame(airport_df, geometry=gpd.points_from_xy(airport_df['lon'], airport_df['lat']))
    train_stations = gpd.GeoDataFrame(trainstations_df, geometry=gpd.points_from_xy(trainstations_df['lon'], trainstations_df['lat']))
    pet_grooming = gpd.GeoDataFrame(pet_grooming_df, geometry=gpd.points_from_xy(pet_grooming_df['lon'], pet_grooming_df['lat']))
    dog_parks = gpd.GeoDataFrame(dog_parks_df, geometry=gpd.points_from_xy(dog_parks_df['lon'], dog_parks_df['lat']))
    bars_clubs = gpd.GeoDataFrame(bars_clubs_df, geometry=gpd.points_from_xy(bars_clubs_df['lon'], bars_clubs_df['lat']))
    vegan_vegetarian = gpd.GeoDataFrame(vegan_vegetarian_df, geometry=gpd.points_from_xy(vegan_vegetarian_df['lon'], vegan_vegetarian_df['lat']))


    for polygon in geojson_data.geometry:

        starbucks_f = starbucks[starbucks.geometry.within(polygon)]

        for _, row in starbucks_f.iterrows():
            folium.Marker([row['lat'], row['lon']],
                            tooltip=["Starbucks"],
                            icon=folium.Icon(icon='fa-coffee', prefix='fa',color='darkgreen', icon_color='white'),
                            popup=row['name']).add_to(marker_group_1)
        
    for polygon in geojson_data.geometry:

        stadium_f = stadium[stadium.geometry.within(polygon)]

        for _, row in stadium_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                            icon=folium.Icon(icon='fa-trophy', prefix='fa',color='darkpurple', icon_color='white'),
                            popup=row['name']).add_to(marker_group_2)
        
    for polygon in geojson_data.geometry:

        schools_f = schools[schools.geometry.within(polygon)]

        for _, row in schools_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                            icon=folium.Icon(icon='fa-graduation-cap', prefix='fa',color='lightblue', icon_color='cadetblue'),
                            popup=row['name']).add_to(marker_group_3)

    for polygon in geojson_data.geometry:

        airports_f = airports[airports.geometry.within(polygon)]

        for _, row in airports_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          icon=folium.Icon(icon='fa-plane', prefix='fa',color='white', icon_color='darkblue'),
                          popup=row['name']).add_to(marker_group_4) 

    for polygon in geojson_data.geometry:

        train_stations_f = train_stations[train_stations.geometry.within(polygon)]

        for _, row in train_stations_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          tooltip=["station"], 
                          icon=folium.Icon(icon='fa-train', prefix='fa',color='white', icon_color='black'),
                          popup=row['name']).add_to(marker_group_5) 
            
    for polygon in geojson_data.geometry:

        pet_grooming_f = pet_grooming[pet_grooming.geometry.within(polygon)]

        for _, row in pet_grooming_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          icon=folium.Icon(icon='fa-paw', prefix='fa',color='white', icon_color='orange'),
                          popup=row['name']).add_to(marker_group_6) 
            
    for polygon in geojson_data.geometry:

        dog_parks_f = dog_parks[dog_parks.geometry.within(polygon)]

        for _, row in dog_parks_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          tooltip=["dog park"], 
                          icon=folium.Icon(icon='fa-thumb-tack', prefix='fa',color='orange', icon_color='white'),
                          popup=row['name']).add_to(marker_group_7) 
            
    for polygon in geojson_data.geometry:

        bars_clubs_f = bars_clubs[bars_clubs.geometry.within(polygon)]

        for _, row in bars_clubs_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          icon=folium.Icon(icon='fa-id-card', prefix='fa',color='black', icon_color='pink'),
                          popup=row['name']).add_to(marker_group_8) 
            
    for polygon in geojson_data.geometry:

        vegan_vegetarian_f = vegan_vegetarian[vegan_vegetarian.geometry.within(polygon)]

        for _, row in vegan_vegetarian_f.iterrows():
            folium.Marker([row['lat'], row['lon']], 
                          tooltip=["vegan restaurant"], 
                          icon=folium.Icon(icon='fa-cutlery', prefix='fa',color='lightgreen', icon_color='white'),
                          popup=row['name']).add_to(marker_group_9) 

    
    marker_group_1.add_to(map)
    marker_group_2.add_to(map)
    marker_group_3.add_to(map)
    marker_group_4.add_to(map)
    marker_group_5.add_to(map)
    marker_group_6.add_to(map)
    marker_group_7.add_to(map)
    marker_group_8.add_to(map)
    marker_group_9.add_to(map)
    
    
    folium.LayerControl(collapsed=False).add_to(map)
    map.save(f"figures/{map_name}.html")

    return map


def chelsea_select(geojson_data, map_name,starbucks_df, stadium_df, schools_df, airport_df, trainstations_df, pet_grooming_df, dog_parks_df, bars_clubs_df, vegan_vegetarian_df):

    '''Function to get a map with option of selecting markers for Chelsea.
    It takes 11 arg:
    - geo json
    - map name
    - 9 dataframes of requirements.
    '''

    chelsea_neighborhood = geojson_data[geojson_data['neighborhood'] == 'Chelsea']

    map = folium.Map(location=[chelsea_neighborhood.geometry.centroid.y.mean(), chelsea_neighborhood.geometry.centroid.x.mean()], zoom_start=14)

    marker_group_1 = folium.FeatureGroup(name='Starbucks')
    marker_group_2 = folium.FeatureGroup(name='Stadiums')
    marker_group_3 = folium.FeatureGroup(name='Schools')
    marker_group_4 = folium.FeatureGroup(name='airports')
    marker_group_5 = folium.FeatureGroup(name='train stations')
    marker_group_6 = folium.FeatureGroup(name='pet grooming')
    marker_group_7 = folium.FeatureGroup(name='dog parks')
    marker_group_8 = folium.FeatureGroup(name='night clubs')
    marker_group_9 = folium.FeatureGroup(name='vegan restaurants')


    starbucks = gpd.GeoDataFrame(starbucks_df, geometry=gpd.points_from_xy(starbucks_df['lon'], starbucks_df['lat']))
    stadium = gpd.GeoDataFrame(stadium_df, geometry=gpd.points_from_xy(stadium_df['lon'], stadium_df['lat']))
    schools = gpd.GeoDataFrame(schools_df, geometry=gpd.points_from_xy(schools_df['lon'], schools_df['lat']))
    airports = gpd.GeoDataFrame(airport_df, geometry=gpd.points_from_xy(airport_df['lon'], airport_df['lat']))
    train_stations = gpd.GeoDataFrame(trainstations_df, geometry=gpd.points_from_xy(trainstations_df['lon'], trainstations_df['lat']))
    pet_grooming = gpd.GeoDataFrame(pet_grooming_df, geometry=gpd.points_from_xy(pet_grooming_df['lon'], pet_grooming_df['lat']))
    dog_parks = gpd.GeoDataFrame(dog_parks_df, geometry=gpd.points_from_xy(dog_parks_df['lon'], dog_parks_df['lat']))
    bars_clubs = gpd.GeoDataFrame(bars_clubs_df, geometry=gpd.points_from_xy(bars_clubs_df['lon'], bars_clubs_df['lat']))
    vegan_vegetarian = gpd.GeoDataFrame(vegan_vegetarian_df, geometry=gpd.points_from_xy(vegan_vegetarian_df['lon'], vegan_vegetarian_df['lat']))

    starbucks.crs = chelsea_neighborhood.crs
    stadium.crs = chelsea_neighborhood.crs
    schools.crs = chelsea_neighborhood.crs
    airports.crs = chelsea_neighborhood.crs
    train_stations.crs = chelsea_neighborhood.crs
    pet_grooming.crs = chelsea_neighborhood.crs
    dog_parks.crs = chelsea_neighborhood.crs
    bars_clubs.crs = chelsea_neighborhood.crs
    vegan_vegetarian.crs = chelsea_neighborhood.crs


    starbucks_f = starbucks[starbucks.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in starbucks_f.iterrows():
        folium.Marker([row['lat'], row['lon']],
                        tooltip=["Starbucks"],
                        icon=folium.Icon(icon='fa-coffee', prefix='fa',color='darkgreen', icon_color='white'),
                        popup=row['name']).add_to(marker_group_1)
    


    stadium_f = stadium[stadium.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in stadium_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        icon=folium.Icon(icon='fa-trophy', prefix='fa',color='darkpurple', icon_color='white'),
                        popup=row['name']).add_to(marker_group_2)
    


    schools_f = schools[schools.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in schools_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        icon=folium.Icon(icon='fa-graduation-cap', prefix='fa',color='white', icon_color='lightblue'),
                        popup=row['name']).add_to(marker_group_3)



    airports_f = airports[airports.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in airports_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        icon=folium.Icon(icon='fa-plane', prefix='fa',color='white', icon_color='darkblue'),
                        popup=row['name']).add_to(marker_group_4) 



    train_stations_f = train_stations[train_stations.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in train_stations_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        tooltip=["station"], 
                        icon=folium.Icon(icon='fa-train', prefix='fa',color='white', icon_color='black'),
                        popup=row['name']).add_to(marker_group_5) 
        


    pet_grooming_f = pet_grooming[pet_grooming.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in pet_grooming_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        icon=folium.Icon(icon='fa-paw', prefix='fa',color='orange', icon_color='white'),
                        popup=row['name']).add_to(marker_group_6) 
        


    dog_parks_f = dog_parks[dog_parks.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in dog_parks_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        tooltip=["dog park"], 
                        icon=folium.Icon(icon='fa-thumb-tack', prefix='fa',color='white', icon_color='orange'),
                        popup=row['name']).add_to(marker_group_7) 
        


    bars_clubs_f = bars_clubs[bars_clubs.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in bars_clubs_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        icon=folium.Icon(icon='fa-id-card', prefix='fa',color='black', icon_color='pink'),
                        popup=row['name']).add_to(marker_group_8) 
        


    vegan_vegetarian_f = vegan_vegetarian[vegan_vegetarian.geometry.within(chelsea_neighborhood.unary_union)]

    for _, row in vegan_vegetarian_f.iterrows():
        folium.Marker([row['lat'], row['lon']], 
                        tooltip=["vegan restaurant"], 
                        icon=folium.Icon(icon='fa-cutlery', prefix='fa',color='lightgreen', icon_color='white'),
                        popup=row['name']).add_to(marker_group_9) 
        
    icon = folium.Icon(
                color = "red",
                icon_color = "white",
                icon = "fa-location-arrow",
                prefix = "fa"
            )
    new_marker = folium.Marker(location = [40.74739,-73.99325], icon=icon, z_index_offset=1000)
    new_marker.add_to(map)

    
    marker_group_1.add_to(map)
    marker_group_2.add_to(map)
    marker_group_3.add_to(map)
    marker_group_4.add_to(map)
    marker_group_5.add_to(map)
    marker_group_6.add_to(map)
    marker_group_7.add_to(map)
    marker_group_8.add_to(map)
    marker_group_9.add_to(map)
    
    folium.Circle(location=[40.74739,-73.99325], fill_color='purple', radius=750, weight=2, color='purple', popup='Desired Area').add_to(map)
    folium.LayerControl(collapsed=False).add_to(map)
    map.save(f"figures/{map_name}.html")

    return map

