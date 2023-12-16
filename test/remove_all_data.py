from pymongo import MongoClient
from pydantic import BaseModel

CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client["microblog"]

def delete_messages():
    collection = db["Messages"]
    collection.drop()

def delete_users():
    collection = db["UserAccount"]
    collection.drop()

delete_users()
delete_messages()