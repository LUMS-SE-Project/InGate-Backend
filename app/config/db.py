# connect mongodb
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

def connect_mongodb():
    try:
        client = MongoClient(os.getenv('MONGO_URL'))
        db = client["SEProj"]
        print('Connected to MongoDB')
    except ConnectionFailure as e:
        print('Connection to MongoDB failed: %s' % e)
    return client


client = connect_mongodb()
