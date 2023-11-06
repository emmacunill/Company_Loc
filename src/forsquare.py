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

load_dotenv()

client = MongoClient("localhost:27017")
db = client["cities_project"]

def load_geo_json(path):

    ''' Function to load geo json.
    takes 1 arg:
    - Path
    '''

    with open(path) as f:
        geo_json = json.load(f)
    return geo_json


def upload_geo_mongo(geojson, name_col):
    
    ''' Function to upload geo json to mongo.
    Takes 2 arg:
    - geojson
    - name you want to give to the collection'''

    c = db.get_collection(name_col)

    for i in geojson["features"]:
        c.insert_one({"geo": i["geometry"]["geometries"][0], "name": i["properties"]})


def upload_geo_mongo_variable(geojson, name_col):
    
    ''' Function to upload geo json to mongo.'''

    c = db.get_collection(name_col)

    for i in geojson["features"]:
        c.insert_one({"geo": i["geometry"], "name": i["properties"]})


def get_coordinates(where):

    ''' Function to get coordinates of cities.
    takes 1 arg, Direction'''

    url_geocode = f"https://geocode.xyz/{where}?json=1"
    res = requests.get(url_geocode)
    san_francisco_loc = res.json()
    lat = san_francisco_loc["latt"]
    lon = san_francisco_loc["longt"]
    coordinates = lat+","+lon
    return coordinates


def upload_category_mongo(json, name_cat):
    
    ''' Function to upload category json into mongo.
    It takes 2 args:
        - json
        - name of the category.'''

    c = db.get_collection(name_cat)

    for i in json:
        c.insert_one(i)


token = os.getenv("token")


def requests_for_foursquare (venue, lat, lon, radius, sort = "DISTANCE" ,limit = 50):

    ''' Function to get places I'm looking for in a specific location'''

    url = f"https://api.foursquare.com/v3/places/search?query={venue}&ll={lat}%2C{lon}&radius={radius}&sort={sort}&limit={limit}"

    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    
    try:
        return requests.get(url, headers=headers).json()
    except:
        print("te has pasado")


def foursquare_places (venue,coordinates,name_cat):
    
    ''' Function to create dictionaries with only the needed information.'''

    lat, lon = str(coordinates).split(',')

    res = requests_for_foursquare (venue, lat, lon, radius=2000, sort = "DISTANCE" ,limit = 50)
    venue = res["results"]
    print(venue)
    results = []

    for i in venue:
        name = i["name"]
        lon = i["geocodes"]["main"]["longitude"]
        lat = i["geocodes"]["main"]["latitude"]

        results.append( {
            "name": name,
            "lat": lat,
            "lon": lon
            })
    
    upload_category_mongo(results, name_cat)

    return results

