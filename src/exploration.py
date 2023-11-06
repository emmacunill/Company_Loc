import requests
import json
import pandas as pd
from getpass import getpass
import os
import time
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()


client = MongoClient("localhost:27017")
db = client["ironhack"]
c = db.get_collection("companies")


def find_design_companies(collection):

    ''' Function to filter the companies that are into design.
    Takes 1 ar:
    - collection'''

    projection = {"_id": 0, "total_money_raised": 1, "name": 1, "category_code": 1, "offices.city": 1}
    design_companies = list(collection.find({"category_code": "design"}, projection = projection).sort("total_money_raised", -1))
    return design_companies

def find_successful_startups(collection):

    ''' Function to filter the startup companies, found with the number of employees and money raised.
    Takes 1 ar:
    - collection'''

    condition_1 = {"total_money_raised": {"$regex": "M"}}
    condition_2 = {"number_of_employees": {"$lte": 100}}
    projection = {"_id": 0, "total_money_raised": 1, "name": 1, "category_code": 1, "offices.city": 1}
    suc_startups = list(collection.find({"$and": [condition_1,condition_2]}, projection = projection).sort("number_of_employees", -1))
    return suc_startups

def oc_city_counts(collection,arg, arg2):

    ''' Function to get items inside a nested list of dictionaries and count the times an item appears repeated.
    Takes 3 arg:
    - collection
    - 2 arg to get info from inside dictionaires.
    '''


    city_counts = defaultdict(int)

    for item in collection:
        for office in item[arg]:
            city = office.get(arg2, '')
            if city:  
                city_counts[city] += 1

    sorted_city_counts = {k: v for k, v in sorted(city_counts.items(), key=lambda item: item[1], reverse=True)}

    cc = cc = pd.DataFrame(sorted_city_counts.values(), index=sorted_city_counts.keys(), columns=['Count'])
    return cc

