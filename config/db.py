from pymongo import MongoClient

MONGO_URI  = "mongodb+srv://shanmukharaopandraki:iVuXwCKNA9f8L3AD@cluster0.hgrw68t.mongodb.net/"

conn = MongoClient(MONGO_URI)
def get_user_collection():
    return conn["users"]