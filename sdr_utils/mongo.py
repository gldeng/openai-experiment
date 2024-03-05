import pymongo
from .constants import *


def get_collection(db_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client[db_name][COLLECTION_NAME]

