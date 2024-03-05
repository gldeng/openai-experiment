import pymongo
from .constants import *

def get_db(db_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client[db_name]


def get_collection(db_name):
    db = get_db(db_name)
    return db[COLLECTION_NAME]


def create_collection_if_not_exists(db_name):
    db = get_db(db_name)

    if COLLECTION_NAME not in db.list_collection_names():
        db.create_collection(COLLECTION_NAME)

    # Access the collection
    coll = db[COLLECTION_NAME]

    # Step 4: Create Index
    # This creates an index on the 'prompt' field
    coll.create_index([('prompt', 1)])  # 1 for ascending order
